from google.cloud import ndb
from models import get_db

client = get_db()


class AppSettings(ndb.Model):
    sendgrid_api_key = ndb.StringProperty(default="")

    # static data (change into your real Google Cloud project data)
    gc_project_name = "test"
    gc_region = "europe-west1"  # if your region is europe-west, you need to 1 at the end (same for us-central1)
    gc_url = "https://mysuper.webapp"

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
        with client.context():
            app_settings = cls.get()

            if sendgrid_api_key:
                app_settings.sendgrid_api_key = sendgrid_api_key

            app_settings.put()

            return app_settings
