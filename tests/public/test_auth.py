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


def test_registration_get(client):
    response = client.get('/registration')
    assert b'Registration' in response.data


def test_init_get(client):
    response = client.get('/init')
    assert b'initialization' in response.data


def test_init_post(client):
    # create the first user and admin
    data = {"init-username": "testman", "init-password": "test123", "init-repeat": "test123",
            "init-sendgrid": "456test", "init-email": "testman@test.man"}
    response = client.post('/init', data=data)
    assert b'successful' in response.data

    # find the user in the database, assert it exists
    testman = User.get_by_username(username="testman")
    assert testman is not None
    assert testman.admin is True
    assert testman.email_addresses[0].email_address == "testman@test.man"

    # assert the sendgrid API key has been stored
    app_settings = AppSettings.get()
    assert app_settings.sendgrid_api_key == "456test"


def test_user_create(client):
    # Let's say some user created an account with the testman@test.man email, but never verified that email.
    # Then another user registered with the same email.
    # When the User.create() function is called, the second user should get a separate User object created (otherwise
    # someone could block another person from creating an account by just adding their unverified email under their
    # own email addresses).
    user_1 = User.create(username="user_1", email_address="testman@test.man", password="user1test")

    user_2 = User.create(username="user_2", email_address="testman@test.man", password="user2test")

    assert user_2.username == "user_2"
