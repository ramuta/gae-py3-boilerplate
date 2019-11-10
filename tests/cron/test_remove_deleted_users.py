import datetime
from urllib.request import Request, urlopen
import pytest

from main import app
from models.user import User


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    yield client


def cleanup():
    # clean up/delete the database (reset Datastore)
    urlopen(Request("http://localhost:8002/reset", data={}))  # this sends an empty POST request


def test_remove_deleted_users(client):
    # create a user
    success, user, message = User.create(email_address="testman@test.man", password="test123")

    # delete the user and mark deleting date at 35 days ago (because cron job only removes users that were marked as
    # deleted more than 30 days ago
    User.delete(user=user, permanently=False)
    User._test_mark_email_verified(user=user)
    User._test_change_deleted_date(user=user, new_date=datetime.datetime.now()-datetime.timedelta(days=35))

    assert user is not None
    assert user.deleted == True

    deleted_users_list_1, next_cursor, more = User.fetch(deleted=True)
    assert len(deleted_users_list_1) == 1

    # run the cron job
    response = client.get('/cron/remove-deleted-users')

    # assert user is really deleted
    deleted_users_list_2, next_cursor, more = User.fetch(deleted=True)
    assert len(deleted_users_list_2) == 0
