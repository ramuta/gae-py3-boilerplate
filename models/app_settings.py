from google.cloud import ndb
from models import get_db

client = get_db()


class AppSettings(ndb.Model):
    sendgrid_api_key = ndb.StringProperty(default="")

    @classmethod
    def get(cls):
        with client.context():
            app_settings = cls.query().get()  # you can use TinyDB (with in-memory storage) for caching

            if not app_settings:
                app_settings = cls()
                app_settings.put()

            return app_settings

    @classmethod
    def update(cls, sendgrid_api_key=None):
        app_settings = cls.get()

        with client.context():
            if sendgrid_api_key:
                app_settings.sendgrid_api_key = sendgrid_api_key

            app_settings.put()

            return app_settings
