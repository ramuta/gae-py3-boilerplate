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


def test_profile_sessions(client):
    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None

    response = client.get('/profile/sessions')

    assert b'Sessions' in response.data
    assert b'Delete' in response.data  # if there's at least one session on the list, there's also a Delete button
    # check if session token hash (first five chars) is in the sessions list (as session ID)
    assert str.encode("{}".format(user.sessions[0].token_hash[:5])) in response.data


def test_profile_session_delete(client):
    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None

    params = {
        "csrf": User.set_csrf_token(user=user),
        "delete-session-token": user.sessions[0].token_hash[:5],  # send the last 5 digits of the session token hash
    }

    response = client.post('/profile/session/delete', data=params, follow_redirects=True)

    user = User.get_user_by_email(email_address="testman@test.man")  # needs to be called again due to Datastore context
    assert user.sessions == []
