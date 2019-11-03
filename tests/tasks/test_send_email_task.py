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


def test_send_email(client):
    # create the first user and admin
    data = {"recipient_email": "receiver@test.man", "sender_email": "sender@test.man", "email_subject": "Hey hey hey",
            "email_body": "<html>My cool email template</html>"}

    response = client.post('/tasks/send-email', json=data)

    assert b'sender@test.man' in response.data
    assert b'Hey hey hey' in response.data
