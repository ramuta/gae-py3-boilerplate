from urllib.request import Request, urlopen

import pytest

from main import app
from models.user import User


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    # create User model and log it in
    # login is required for all handlers in this file
    success, user, message = User.create(email_address="testman@test.man", password="test123")
    User._test_mark_email_verified(user=user)
    session_token = User.generate_session_token(user=user)
    client.set_cookie(server_name="localhost", key="my-web-app-session", value=session_token)

    yield client


def cleanup():
    # clean up/delete the database (reset Datastore)
    urlopen(Request("http://localhost:8002/reset", data={}))  # this sends an empty POST request


def test_profile_logout(client):
    response = client.post('/logout', follow_redirects=True)

    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None

    # check if session token is deleted from the User object
    assert user.sessions == []
