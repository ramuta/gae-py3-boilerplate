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
