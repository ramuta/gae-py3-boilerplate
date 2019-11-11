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
    success, user, message = User.create(email_address="testman@test.man", password="test123", admin=True)
    User._test_mark_email_verified(user=user)
    session_token = User.generate_session_token(user=user)
    client.set_cookie(server_name="localhost", key="my-web-app-session", value=session_token)

    yield client


def cleanup():
    # clean up/delete the database (reset Datastore)
    urlopen(Request("http://localhost:8002/reset", data={}))  # this sends an empty POST request


def test_admin_users_list_1(client):
    # only one user on the list (the admin)
    response = client.get('/admin/users')
    assert b'Active users' in response.data
    assert b'testman@test.man' in response.data
    assert b'Admin' in response.data


def test_admin_users_list_2(client):
    # create multiple users via Fake Data Loader
    client.get('/load-fake-data')

    # go to admin/users and see if users were created
    response = client.get('/admin/users')
    assert b'Active users' in response.data
    assert b'testman@test.man' in response.data
    assert b'Admin' in response.data

    assert b'Jim Jones' in response.data
    assert b'user_2@my.webapp' in response.data
    assert b'Load more users' in response.data  # load more users button


def test_admin_user_details(client):
    user = User.get_user_by_email(email_address="testman@test.man")

    response = client.get('/admin/user/{}'.format(user.get_id))

    assert b'testman@test.man' in response.data
    assert b'Admin' in response.data
