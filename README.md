# GAE Py3 Boilerplate

A web application starter for Google App Engine Python 3 runtime.

> **WORK IN PROGRESS:** This template is not completed yet.
>
> TODO:
> - suspend user
> - delete user (marking user as deleted=True - this does not really delete the user from the Datastore)
> - edit password
> - login with password
> - translation system for email subjects
> - Slovene translations (all HTML templates)

## Features

- **Different types of authentication system:**
  - Email-only auth (password-less, login is via emailed magic link)
  - Email/password authentication
- **Translations:**
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

## IMPORTANT: auto reloading

When you make a change in any Python file, the Flask app will automatically reload so that the changes are recognized.

But unfortunately, this auto reloading only works for Python files, not for other files such as HTML, CSS, JS etc.

So how to solve this problem?

When you make a change in the HTML file, also make a simple space in the main.py file (or some other Python file). You 
can make the space after this line:

    app = Flask(__name__)

The space itself is harmless and it will not hurt your web app. After you make it, save the changes (CTRL+S or CMD+S) 
and the web app will automatically reload.

You are able to see that the web app has reloaded if you see this line popping up in the terminal:

     * Restarting with stat

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

## init

You'll need to initialize the web app in order to make yourself the admin. You can do this by going to the `/init` URL 
in this web app.

### SendGrid

At initialization you'll be required to enter a SendGrid API key. On localhost you can enter a fake API key (just a 
random string) because you'll be able to read emails in the Terminal. But on production use the real API key. For this 
you'll need to first create yourself a SendGrid account (their free tier would do).

## Background tasks

Background tasks are done using Cloud Tasks. There's one example (sending emails) of how to do it in this project 
template. See the following files for more detail:

- utils/task_helper.py
- tasks/send_email_task.py

Whenever you'll want to create a background task, use this function from utils/task_helper.py:

    run_background_task(relative_path, payload)

Make sure you have environment variables `MY_GAE_REGION` and `MY_APP_URL` set in `app.yaml`.

The task queues are set in `queue.yaml`. Currently two queues are set, `default` and `email`. If you need additional 
ones, edit the `queue.yaml` file.

P.S.: When you'll do a deployment to Google Cloud, you need to include all your yaml files in the command:

    gcloud app deploy app.yaml queue.yaml --version production

The same goes for other YAML files, such as `cron.yaml` or `index.yaml`, if you'll use them.

## Cron jobs

At some point you'll want to run your own cron jobs. Google App Engine has a really nice support for running cron 
jobs - read more about it here: 
[Scheduling Jobs with cron.yaml](https://cloud.google.com/appengine/docs/standard/python3/scheduling-jobs-with-cron-yaml).

In terms of the web app structure, the best option is to have each cron job in a separate Python file inside the "cron" 
folder. A cron job is just a normal handler that accepts GET requests (it doesn't accept other types of requests, like 
POST).

One **example** of a cron job is already created in this starter template. It's a cron job that permanently removes a 
user object from the Datastore once it has been marked as "deleted".

> Since a cron job is a normal handler with its own route (URL is set up in main.py), anyone can call it. But to prevent 
> random people from triggering your cron job handlers, make sure you check each in the beginning of each cron job 
> whether the request has the `X-Appengine-Cron: true` HTTP header (cannot be faked) and whether it comes from the 
> `10.0.0.1` ip address. Read more about that [here](https://cloud.google.com/appengine/docs/standard/python3/scheduling-jobs-with-cron-yaml#validating_cron_requests).

In addition, you'll need to add each cron job also in the file called `cron.yaml` in your root where you'll define when 
the cron jobs are to be run.

## Deployment

## Deployment to Google App Engine

In order to deploy the web app on Google Cloud, you will probably need to connect your credit card to it. But this 
doesn't mean Google will start charging you right away - the free quota is pretty generous and you can also set a 
daily spending limit to 0 USD (see step 4 below in the "Deployment to GAE" section).

### 1) gcloud init

Open the Terminal in the root of the project and type in:

    gcloud init

If this is a new project, select the choice no.2: **Create a new configuration.** Then enter a name for this 
configuration (it needs to be unique only on your computer, not globally).

If this is an already existing project with an existing configuration, select it and skip some of the next steps.

After this step you'll need to log in with your Google account.

### 2) Select the cloud project or create a new one

If you already have a Google Cloud project for this repository, select it. If not, create a new one.

### 3) Create the App Engine instance

Now it's time to create a Google App Engine instance and select the region where it will run (See the 
[list of possible regions here](https://cloud.google.com/appengine/docs/locations)).

> Important: The region cannot be changed later.

Once you've chosen the region, enter the following command:

    gcloud app create --region=europe-west

In this case we chose the "europe-west" region, but replace it with some other if you want.

### 4) Enable Cloud Build API

Go to Google Cloud Console, open your project and type this in the Search box: **Cloud Build API**. Then enable it.

You will probably need to enable billing for your project, but don't worry - this does not mean Google will start 
charging you. Google has a very generous **free quota** and you will very likely stay within that quote.

But it doesn't hurt to set up the daily limit for your GAE app on Google Cloud Console (type "App Engine settings" in 
the Search box and then enter the daily spending limit (it can be 0).

### 5) Deploy your code to GAE

The next step is to deploy your code to Google Cloud:

    gcloud app deploy app.yaml cron.yaml queue.yaml --version production

You could do it without the version flag, but it's a good practice so that GAE does not create a new version for each of 
your deployments. You can also name versions after your Git branches (for example: master, develop).

### 6) Check if Datastore is enabled

If it's not enabled automatically, just type "Datastore" in the Search box on Google Cloud Platform. Once you click on 
the selection, the Datastore will be automatically enabled.
