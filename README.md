# GAE Py3 Boilerplate

A web application starter for Google App Engine Python 3 runtime.

> **WORK IN PROGRESS:** This template is not completed yet.
>
> TODO:
> - registration system
> - login system
> - suspend user

## Features

- Different types of authentication system:
  - Email-only auth (password-less, login is via emailed magic link)
  - Email/password authentication
- Translations
  - In-built simple translation system
  - Each language has its own templates folder

## How to run the web app using run.py

The best way to run the web app is using the `run.py` file. There are two ways to do it:

- A) Right-click in PyCharm on the `run.py` file and select Run.
- B) Run in the terminal using `python run.py` (make sure you use Python 3).

The `run.py` script will ask you whether to run the web app or tests.

Alternatively, you can select app vs. tests already in the command line:

    python run.py app

or

    python run.py test

## A better way to run tests

The problem with running tests via run.py is that the emulator restarts every time you run run.py.

There's a better approach: running the datastore emulator in a separate terminal tab using this command:

    gcloud beta emulators datastore start --consistency=1 --no-store-on-disk --project test --host-port "localhost:8002"

and then you can run tests in a separate Terminal tab:

    # mac & linux:
    export TESTING=yes && pytest -p no:warnings

    # windows
    set TESTING=yes && pytest -p no:warnings

## See the data in Datastore visually on localhost

If you'd like to see what data are stored in the localhost Datastore emulator, install 
[Datastore Viewer](https://github.com/gumo-py/datastore-viewer):

    pip install datastore-viewer

Then you can run the Datastore Viewer using this command:

    # mac & linux:
    export DATASTORE_EMULATOR_HOST=localhost:8001 && datastore-viewer
    
    # windows
    set DATASTORE_EMULATOR_HOST=localhost:8001 && datastore-viewer

Datastore Viewer will run on [http://127.0.0.1:8082/](http://127.0.0.1:8082/). Enter `test` as the project name and 
you'll see the data in your Datastore.
