import datetime
import hashlib
import logging
import secrets
from operator import attrgetter

import bcrypt
from google.cloud import ndb
from models import get_db
from translations.loader import get_translation
from utils.check_environment import is_local
from utils.email_helper import send_email

client = get_db()


class Session(ndb.Model):
    token_hash = ndb.StringProperty()
    ip = ndb.StringProperty()
    platform = ndb.StringProperty()
    browser = ndb.StringProperty()
    country = ndb.StringProperty()
    user_agent = ndb.StringProperty()
    expired = ndb.DateTimeProperty()


class CSRFToken(ndb.Model):
    """CSRF token (also called XSRF) is a mechanism that prevents CSRF attacks."""
    token = ndb.StringProperty()
    expired = ndb.DateTimeProperty()


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email_address = ndb.StringProperty()

    # auth
    email_address_verified = ndb.BooleanProperty(default=False)
    password_hash = ndb.StringProperty()
    sessions = ndb.StructuredProperty(Session, repeated=True)
    csrf_tokens = ndb.StructuredProperty(CSRFToken, repeated=True)  # there should be max 10 CSRF tokens stored

    # magic login link
    magic_link_token_hash = ndb.StringProperty()
    magic_link_token_expired = ndb.DateTimeProperty()

    # status
    admin = ndb.BooleanProperty(default=False)
    suspended = ndb.BooleanProperty(default=False)  # if user is suspended, they cannot login

    # standard model fields
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)
    deleted_date = ndb.DateTimeProperty()  # note that if the object gets "un-deleted", this date will stay here

    # properties (ordered by alphabet)
    @property
    def get_id(self):
        return self.key.id()

    # class methods (ordered by alphabet)
    @classmethod
    def create(cls, email_address, password=None, admin=False, first_name=None, last_name=None):
        with client.context():
            # check if there's any user with the same email address already
            user = cls.query(cls.email_address == email_address).get()

            if not user:  # if user does not yet exist, create one
                hashed = None
                if password:
                    # use bcrypt to hash the password
                    hashed = bcrypt.hashpw(password=str.encode(password), salt=bcrypt.gensalt(12))

                # create the user object and store it into Datastore
                user = cls(email_address=email_address, password_hash=hashed, admin=admin, first_name=first_name,
                           last_name=last_name)
                user.put()

                return True, user, "Success"  # succes, user, message
            else:
                return False, user, "User with this email address is already registered. Please go to the " \
                                    "Login page and try to log in."

    @classmethod
    def delete_session(cls, user, token_hash_five_chars):
        with client.context():
            valid_sessions = []
            for session in user.sessions:
                # delete session that has token hash that starts with these 5 characters
                # (delete by not including in the new sessions list)
                if not session.token_hash.startswith(token_hash_five_chars):
                    valid_sessions.append(session)

            user.sessions = valid_sessions
            user.put()

        return user

    @classmethod
    def delete(cls, user, permanently=False):
        with client.context():
            if permanently:
                user.key.delete()  # this deletes user from Datastore
            else:
                user.deleted = True  # this does NOT delete user from Datastore (just marks it as "deleted")
                user.deleted_date = datetime.datetime.now()
                user.put()

        return True

    @classmethod
    def fetch(cls, email_address_verified=True, suspended=False, deleted=False, limit=None, cursor=None):
        with client.context():
            users, next_cursor, more = cls.query(cls.email_address_verified == email_address_verified,
                                                 cls.suspended == suspended,
                                                 cls.deleted == deleted).fetch_page(limit, start_cursor=cursor)

            # this fixes the pagination bug which returns more=True even if less users than limit or if next_cursor is
            # the same as the cursor
            logging.warning("More:")
            logging.warning(more)
            logging.warning(type(more))
            if limit and len(users) < limit:
                return users, None, False

            logging.warning("More 2:")
            logging.warning(more)
            logging.warning(type(more))

            try:
                return users, next_cursor.urlsafe().decode(), more
            except AttributeError as e:  # if there's no next_cursor, an AttributeError will occur
                return users, None, False

    @classmethod
    def generate_session_token(cls, user, request=None):
        with client.context():
            # generate session token and its hash
            token = secrets.token_hex()
            token_hash = hashlib.sha256(str.encode(token)).hexdigest()

            # create a session
            session = Session(token_hash=token_hash, expired=(datetime.datetime.now() + datetime.timedelta(days=30)))
            if request:  # this separation is needed for tests which don't have the access to "request" variable
                session.ip = request.access_route[-1]
                session.platform = request.user_agent.platform
                session.browser = request.user_agent.browser
                session.user_agent = request.user_agent.string
                session.country = request.headers.get("X-AppEngine-Country")

            # store the session in the User model
            if not user.sessions:
                user.sessions = [session]
            else:
                valid_sessions = [session]
                for item in user.sessions:  # loop through sessions and remove the expired ones
                    if item.expired > datetime.datetime.now():
                        valid_sessions.append(item)

                user.sessions = valid_sessions  # now only non-expired sessions are stored in the User object

            user.put()

            return token

    @classmethod
    def get_user_by_email(cls, email_address):
        with client.context():
            user = cls.query(cls.email_address == email_address).get()
            return user

    @classmethod
    def get_user_by_id(cls, user_id):
        with client.context():
            user = User.get_by_id(int(user_id))

            return user

    @classmethod
    def get_user_by_session_token(cls, session_token):
        """

        :param session_token:
        :return: success boolean (True/False), user object, message
        """
        with client.context():
            token_hash = hashlib.sha256(str.encode(session_token)).hexdigest()

            user = cls.query(cls.sessions.token_hash == token_hash).get()

            if not user:
                return False, None, "A user with this session token does not exist. Try to log in again."

            if user.deleted:
                logging.warning("Deleted user {} wanted to login.".format(user.email_address))
                return False, None, "This user has been deleted. Please contact website administrators for more info."

            if user.suspended:
                logging.warning("Suspended user {} wanted to login.".format(user.email_address))
                return False, None, "This user has been suspended. Please contact website administrators for more info."

            if not user.email_address_verified:
                logging.warning("User with unverified email address {} wanted to login.".format(user.email_address))
                return False, None, "This user's email address hasn't yet been verified. Please contact website " \
                                    "administrators for more info."

            # important: you can't check for expiration in the cls.query() above, because it wouldn't only check the
            # expiration date of the session in question, but any expiration date which could give a false result
            for session in user.sessions:
                if session.token_hash == token_hash:
                    if session.expired > datetime.datetime.now():
                        return True, user, "Success"

            return False, None, "Unknown error."

    @classmethod
    def is_csrf_token_valid(cls, user, csrf_token):
        with client.context():
            token_validity = False

            unused_tokens = []
            for csrf in user.csrf_tokens:  # loop through user's CSRF tokens
                if csrf.token == csrf_token:  # if tokens match, set validity to True
                    token_validity = True
                else:
                    unused_tokens.append(csrf)  # if not, add CSRF token to the unused_tokens list

            if unused_tokens != user.csrf_tokens:
                user.csrf_tokens = unused_tokens
                user.put()

            return token_validity

    @classmethod
    def is_there_any_admin(cls):
        with client.context():
            admin = cls.query(cls.admin == True, cls.deleted == False).get()

            if admin:
                return True
            else:
                return False

    @classmethod
    def permanently_batch_delete(cls):
        # Permanently delete users that were marked as deleted=True more than 30 days ago
        with client.context():
            users_keys = cls.query(cls.deleted == True,
                                   cls.deleted_date < (datetime.datetime.now() - datetime.timedelta(days=30))).fetch(keys_only=True)

            ndb.delete_multi(keys=users_keys)
            return True

    @classmethod
    def send_magic_login_link(cls, email_address, locale="en"):
        # generate magic link token and its hash
        token = secrets.token_hex()

        user = cls.get_user_by_email(email_address=email_address)

        with client.context():
            if user:
                user.magic_link_token_hash = hashlib.sha256(str.encode(token)).hexdigest()
                user.magic_link_token_expired = datetime.datetime.now() + datetime.timedelta(hours=3)
                user.put()

                # send email with magic link to user
                send_email(recipient_email=email_address, email_template="emails/login-magic-link.html",
                           email_params={"magic_login_token": token},
                           email_subject=get_translation(locale=locale,
                                                         translation_function="magic_link_email_subject"))

                return True, "Success"
            else:
                return False, "User with this email is not registered yet!"

    @classmethod
    def set_csrf_token(cls, user):
        with client.context():
            # first delete expired tokens from the CSRF tokens list in the user object
            valid_tokens = []
            for csrf in user.csrf_tokens:
                if csrf.expired > datetime.datetime.now():
                    valid_tokens.append(csrf)

            # check how many csrf tokens are still left in the User object (should be 10 or less)
            # if more than 10, delete the oldest one (with the closest expired date)
            if len(valid_tokens) >= 10:
                oldest_token = min(valid_tokens, key=attrgetter("expired"))
                valid_tokens.remove(oldest_token)

            # then create a new CSRF token and enter it in the tokens list
            token = secrets.token_hex()
            csrf_object = CSRFToken(token=token, expired=(datetime.datetime.now() + datetime.timedelta(hours=8)))
            valid_tokens.append(csrf_object)

            # finally, store the new tokens list back in the user model
            user.csrf_tokens = valid_tokens
            user.put()

            return token

    @classmethod
    def validate_magic_login_token(cls, magic_token, request=None):
        user = None

        with client.context():
            # convert token to hash
            magic_link_token_hash = hashlib.sha256(str.encode(magic_token)).hexdigest()

            # find user by this token
            user = cls.query(cls.magic_link_token_hash == magic_link_token_hash).get()

            # check if token hasn't expired yet
            if user and user.magic_link_token_expired > datetime.datetime.now():
                # if email_address is not verified yet, mark it as verified
                user.email_address_verified = True
                user.magic_link_token_expired = datetime.datetime.now()  # make the token expired
                user.put()
            else:
                # if error, return False and message describing the problem
                return False, "The magic link is not valid or is expired. Please request a new one."

        # create session (this must be outside the "with client.context()", because context is already created in the
        # generate_session_token() method)
        session_token = cls.generate_session_token(user=user, request=request)

        # return True and session token for storing into cookie (in handler)
        return True, session_token


    # METHODS FOR TESTING PURPOSES ONLY!
    @classmethod
    def _test_mark_email_verified(cls, user):
        """
        FOR TESTING PURPOSES ONLY!
        :param user:
        :return:
        """
        with client.context():
            if is_local():
                user.email_address_verified = True
                user.put()

    @classmethod
    def _test_change_deleted_date(cls, user, new_date):
        """
        FOR TESTING PURPOSES ONLY!
        :param user:
        :param new_date:
        :return:
        """
        with client.context():
            if is_local():
                user.deleted_date = new_date
                user.put()
