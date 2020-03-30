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


def test_admin_user_delete(client):
    user = User.get_user_by_email(email_address="testman@test.man")
    assert user.deleted is False

    # POST
    params = {
        "csrf": User.set_csrf_token(user=user),
    }
    response_post = client.post('/admin/user/{}/delete-toggle'.format(user.get_id), data=params, follow_redirects=True)

    user = User.get_user_by_email(email_address="testman@test.man")  # needed to be called again due to DB context
    assert user.deleted is True


def test_admin_user_details(client):
    user = User.get_user_by_email(email_address="testman@test.man")

    response = client.get('/admin/user/{}'.format(user.get_id))

    assert b'testman@test.man' in response.data
    assert b'Admin' in response.data


def test_admin_user_edit(client):
    user = User.get_user_by_email(email_address="testman@test.man")

    # GET
    response_get = client.get('/admin/user/{}/edit'.format(user.get_id))
    assert b'Edit' in response_get.data
    assert b'Testing Person' not in response_get.data

    # POST
    params = {
        "csrf": User.set_csrf_token(user=user),
        "first-name": "Testing",
        "last-name": "Person",
    }
    response_post = client.post('/admin/user/{}/edit'.format(user.get_id), data=params, follow_redirects=True)
    assert b'Testing Person' in response_post.data


def test_admin_user_suspend(client):
    user = User.get_user_by_email(email_address="testman@test.man")
    assert user.suspended is False

    # POST
    params = {
        "csrf": User.set_csrf_token(user=user),
    }
    response_post = client.post('/admin/user/{}/suspend-toggle'.format(user.get_id), data=params, follow_redirects=True)

    user = User.get_user_by_email(email_address="testman@test.man")  # needed to be called again due to DB context
    assert user.suspended is True


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
    assert b'Load more active users' in response.data  # load more users button


def test_admin_users_list_deleted(client):
    # create multiple users via Fake Data Loader
    client.get('/load-fake-data')

    # go to admin/users/deleted and see if users were created
    response = client.get('/admin/users/deleted')
    assert b'Deleted users' in response.data
    assert b'user_4@my.webapp' in response.data
    assert b'Damian Dante' in response.data


def test_admin_users_list_suspended(client):
    # create multiple users via Fake Data Loader
    client.get('/load-fake-data')

    # go to admin/users/suspended and see if users were created
    response = client.get('/admin/users/suspended')
    assert b'Deleted users' in response.data
    assert b'user_4@my.webapp' in response.data
    assert b'Damian Dante' in response.data
