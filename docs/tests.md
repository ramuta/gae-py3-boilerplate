# Tests

## How to run tests

While you could run tests by right-clicking on run.py and then writing "yes" in the Terminal, there's a drawback to 
this - you'll need to reload the whole Datastore emulator every time you need to restart tests.

There's a better approach, though: running the datastore emulator in a separate terminal tab using this command:

    gcloud beta emulators datastore start --consistency=1 --no-store-on-disk --project test --host-port "localhost:8002"

and then you can run tests in a separate Terminal tab:

    # mac & linux:
    export TESTING=yes && pytest -p no:warnings

    # windows
    set TESTING=yes && pytest -p no:warnings

## How to write tests

Examine how existing tests are done.

Every test Python file (and test function) starts with `test_`. This is a **mandatory** prefix!

The other two mandatory things are two functions that need to exist in every test file:

- `client()`
- `cleanup()`

The best approach is to copy them from one of the existing files. Just make sure to think before if you need to add 
creating a user in the `client()` function, or not. And if you'll create a user there, does it need to be admin, or not?

A simple GET request test looks something like this:

```python
def test_hello(client):
    response = client.get('/')
    assert b'Hello' in response.data
    assert 200 == response.status_code
```

For a POST request do something like this:

```python
def test_contact(client):
    data = {"sender_name": "Testman", "sender_email": "testman@test.man", "sender_message": "Hello everyone!"}

    response = client.post('/contact', data=data, follow_redirects=True)
    
    assert b'Thank you for contacting us!' in response.data
```

## Links:

- [Index](/README.md#documentation)
