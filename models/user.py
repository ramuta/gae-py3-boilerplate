import bcrypt
import datetime

from google.cloud import ndb
from models import get_db

client = get_db()


class EmailAddress(ndb.Model):
    email_address = ndb.StringProperty()
    primary = ndb.BooleanProperty(default=False)  # primary email for app notifications

    # email address verification fields
    verified = ndb.BooleanProperty(default=False)
    verification_token = ndb.StringProperty()
    verification_token_expiration = ndb.DateTimeProperty(default=(datetime.datetime.now() + datetime.timedelta(days=5)))


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

    username = ndb.StringProperty()
    email_addresses = ndb.StructuredProperty(EmailAddress, repeated=True)  # user can have multiple email addresses
    password_hash = ndb.StringProperty()

    admin = ndb.BooleanProperty(default=False)
    suspended = ndb.BooleanProperty(default=False)  # if user is suspended, they cannot login

    # standard model fields
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def is_there_any_admin(cls):
        with client.context():
            admin = cls.query(cls.admin == True, cls.deleted == False).get()

            if admin:
                return True
            else:
                return False

    @classmethod
    def create(cls, username=None, email_address=None, password=None, admin=False):
        with client.context():
            user = None

            if username:
                # check if there's any user with the same name already
                user = cls.query(cls.username == username).get()

            if email_address:
                # check if there's any user with the same email address already
                some_user = cls.query(cls.email_addresses.email_address == email_address).get()

                # also check if the email was verified (you CANNOT do that in the query above!!! Because if there's
                # some other email address that was verified, it would return a user, even though the email address
                # that you wanted to check was not really verified)
                if some_user:
                    for email in some_user.email_addresses:
                        if email.email_address == email_address and email.verified == True:
                            user = some_user

            if not user:  # if user does not yet exist, create one
                hashed = None
                if password:
                    # use bcrypt to hash the password
                    hashed = bcrypt.hashpw(password=str.encode(password), salt=bcrypt.gensalt(12))

                # create the user object and store it into Datastore
                user = cls(username=username, password_hash=hashed, admin=admin)

                # add email address if there is one
                if email_address:
                    user.email_addresses = [EmailAddress(email_address=email_address, primary=True)]

                user.put()  # save the user object in Datastore

            return user

    @classmethod
    def get_by_username(cls, username):
        with client.context():
            user = cls.query(cls.username == username).get()
            return user

    @classmethod
    def add_email_address(cls, user, email_address, primary=False):
        with client.context():
            user.email_addresses.append(EmailAddress(email_address=email_address, primary=primary))
            user.put()

        return user
