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
    User.create(email_address="testman@test.man", password="test123")

    data = {"registration-first-name": "Testman", "registration-last-name": "Testovian",
            "registration-email": "testman@test.man"}

    response = client.post('/register', data=data, follow_redirects=True)

    assert b'Registration error' in response.data
    assert b'User with this email address is already registered' in response.data

    user = User.get_user_by_email(email_address="testman@test.man")
    assert user is not None


def test_login_get(client):
    response = client.get('/login')
    assert b'Login' in response.data
    assert b"After you click submit, you'll receive an email" in response.data


def test_login_post_success(client):
    User.create(email_address="testman@test.man", password="test123")

    data = {"login-email": "testman@test.man"}
    response = client.post('/login', data=data, follow_redirects=True)
    assert b'Magic Login Link sent to your email address' in response.data
    assert 200 == response.status_code


def test_login_post_fail(client):
    User.create(email_address="testman@test.man", password="test123")

    data = {"login-email": "testman23@test.man"}  # WRONG EMAIL!!!
    response = client.post('/login', data=data, follow_redirects=True)
    assert 403 == response.status_code
    assert b'User with this email is not registered yet' in response.data
