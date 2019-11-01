from urllib.request import Request, urlopen
import pytest

from main import app


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
