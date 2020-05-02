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


def test_profile_change_email_get(client):
    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None

    response = client.get('/profile/change-email')

    assert b'Change my email address' in response.data


def test_profile_change_email_post(client):
    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None

    # POST
    params = {
        "csrf": User.set_csrf_token(user=user),
        "email-address": "testman22@test.man",
    }
    response_post = client.post('/profile/change-email', data=params, follow_redirects=True)
    assert b'Confirmation needed' in response_post.data


def test_profile_edit_get(client):
    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None

    response = client.get('/profile/edit')

    assert b'Edit profile' in response.data


def test_profile_edit_post(client):
    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None

    # POST
    params = {
        "csrf": User.set_csrf_token(user=user),
        "first-name": "Neo",
        "last-name": "Anderson",
    }
    response_post = client.post('/profile/edit', data=params, follow_redirects=True)
    assert b'Neo' in response_post.data
    assert b'Anderson' in response_post.data


def test_profile_my_details(client):
    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None

    response = client.get('/profile')

    assert b'My profile' in response.data
