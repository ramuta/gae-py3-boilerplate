from urllib.request import Request, urlopen
import pytest

from main import app
from models.app_settings import AppSettings
from models.user import User


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    yield client


def cleanup():
    # clean up/delete the database (reset Datastore)
    urlopen(Request("http://localhost:8002/reset", data={}))  # this sends an empty POST request


# INIT
def test_init_get(client):
    response = client.get('/init')
    assert b'initialization' in response.data


def test_init_post(client):
    # create the first user and admin
    data = {"init-sendgrid": "456test", "init-email": "testman@test.man"}
    response = client.post('/init', data=data)
    assert b'successful' in response.data

    # find the user in the database, assert it exists
    testman = User.get_user_by_email(email_address="testman@test.man")
    assert testman is not None
    assert testman.admin is True

    # assert the sendgrid API key has been stored
    app_settings = AppSettings.get()
    assert app_settings.sendgrid_api_key == "456test"


# REGISTRATION
def test_register_get(client):
    response = client.get('/register')
    assert b'Enter your email address' in response.data


def test_register_post_success(client):
    data = {"registration-first-name": "Testman", "registration-last-name": "Testovian",
            "registration-email": "testman@test.man"}

    response = client.post('/register', data=data, follow_redirects=True)

    assert b'Registration successful' in response.data
    assert b'Please verify your email address' in response.data

    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None


def test_register_post_fail(client):
    User.create(email_address="testman@test.man")

    data = {"registration-first-name": "Testman", "registration-last-name": "Testovian",
            "registration-email": "testman@test.man"}

    response = client.post('/register', data=data, follow_redirects=True)

    assert b'Registration error' in response.data
    assert b'User with this email address is already registered' in response.data

    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None


# LOGIN WITH JUST EMAIL
def test_login_email_get(client):
    response = client.get('/login')
    assert b'Login' in response.data
    assert b"After you click submit, you'll receive an email" in response.data


def test_login_email_post_success(client):
    User.create(email_address="testman@test.man")

    data = {"login-email": "testman@test.man"}
    response = client.post('/login', data=data, follow_redirects=True)
    assert b'Magic Login Link sent to your email address' in response.data
    assert 200 == response.status_code


def test_login_email_post_fail(client):
    User.create(email_address="testman@test.man")

    data = {"login-email": "testman23@test.man"}  # WRONG EMAIL!!!
    response = client.post('/login', data=data, follow_redirects=True)
    assert 403 == response.status_code
    assert b'User with this email is not registered yet' in response.data


# LOGIN WITH PASSWORD
def test_login_password_get(client):
    response = client.get('/login-password')
    assert b'Login with password' in response.data


def test_login_password_success_post(client):
    # correct password
    success, user, message = User.create(email_address="testman@test.man", password="test123")
    User._test_mark_email_verified(user=user)

    data = {
        "login-email": "testman@test.man",
        "login-password": "test123",
    }
    response = client.post('/login-password', data=data, follow_redirects=True)
    assert b'My profile' in response.data


def test_login_password_fail_post(client):
    # wrong password
    success, user, message = User.create(email_address="testman@test.man", password="test123")
    User._test_mark_email_verified(user=user)

    data = {
        "login-email": "testman@test.man",
        "login-password": "wrongpassword123",
    }
    response = client.post('/login-password', data=data, follow_redirects=True)
    assert 403 == response.status_code
    assert b'Forbidden' in response.data
    assert b'The entered password is incorrect.' in response.data


# RESET PASSWORD
def test_reset_password_enter_email_get(client):
    response = client.get('/password-reset-enter-email')
    assert b'Reset password' in response.data
    assert b"Submit your email address and we'll send you a link to (re)set your password." in response.data


def test_reset_password_enter_email_post_success(client):
    User.create(email_address="testman@test.man")

    data = {"reset-password-email": "testman@test.man"}
    response = client.post('/password-reset-enter-email', data=data, follow_redirects=True)

    assert b'Password Reset Link sent!' in response.data
    assert b"Password Reset Link sent to your email address" in response.data


def test_reset_password_enter_email_post_fail(client):
    User.create(email_address="testman@test.man")

    data = {"reset-password-email": "some@other.email"}  # this email does not exist in the database
    response = client.post('/password-reset-enter-email', data=data, follow_redirects=True)

    assert 403 == response.status_code
    assert b'User with this email is not registered yet!' in response.data


def test_reset_password_enter_password_get(client):
    # correct token (GET)
    success, user, message = User.create(email_address="testman@test.man")
    User._test_set_password_reset_token(user, token="abc123def")

    response = client.get('/password-reset-token/abc123def')
    assert b'Reset password' in response.data
    assert b"Enter your NEW password" in response.data


def test_reset_password_enter_password_wrong_token_get(client):
    # wrong token (GET)
    success, user, message = User.create(email_address="testman@test.man")
    User._test_set_password_reset_token(user, token="abc123correct")

    response = client.get('/password-reset-token/abc123wrong')  # wrong token
    assert b'Forbidden' in response.data
    assert b"The password reset link is not valid or is expired." in response.data


def test_reset_password_enter_password_post(client):
    # correct token (POST)
    success, user, message = User.create(email_address="testman@test.man")
    User._test_set_password_reset_token(user, token="abc123def")

    assert user.password_hash is None  # assert that user does not have a password yet

    # set a password
    data = {
        "reset-password-new-password": "abc123",
        "reset-password-repeat-password": "abc123",
    }
    response = client.post('/password-reset-token/abc123def', data=data, follow_redirects=True)
    assert b'Success!' in response.data
    assert b"Your password has been successfully (re)set." in response.data

    user = User.get_user_by_email(email_address="testman@test.man")
    assert user.password_hash is not None  # assert that the user now has a password
