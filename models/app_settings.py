from google.cloud import ndb
from models import get_db

client = get_db()


class AppSettings(ndb.Model):
    sendgrid_api_key = ndb.StringProperty()

    # types of authentication
    auth_username_password = ndb.StringProperty(default="no")
    auth_email_password = ndb.StringProperty(default="no")
    auth_email_only = ndb.StringProperty(default="no")  # passwordless login, via email magic link

    @classmethod
    def get(cls):
        with client.context():
            app_settings = cls.query().get()

            if not app_settings:
                app_settings = cls()
                app_settings.put()

            return app_settings

    @classmethod
    def update(cls, sendgrid_api_key=None, auth_username_password=None, auth_email_password=None,
               auth_email_only=None):
        with client.context():
            app_settings = cls.get()

            if sendgrid_api_key:
                app_settings.sendgrid_api_key = sendgrid_api_key

            if auth_email_only:
                app_settings.auth_email_only = auth_email_only

            if auth_email_password:
                app_settings.auth_email_password = auth_email_password

            if auth_username_password:
                app_settings.auth_username_password = auth_username_password

            app_settings.put()

            return app_settings
