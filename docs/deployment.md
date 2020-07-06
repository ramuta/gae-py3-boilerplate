# Deployment

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

### 5) Enable Cloud Tasks API

Cloud Tasks are not enabled by default, so you'll have to enable it by yourself on the Google Cloud Console, the same 
way as Cloud Build API was enabled in the previous step.

### 6) Enable App Engine Admin API

This is needed if you'd like to do automated deployments via some CI service.

### 7) Deploy your code to GAE

The next step is to deploy your code to Google Cloud:

    gcloud app deploy app.yaml cron.yaml queue.yaml --version production

You could do it without the version flag, but it's a good practice so that GAE does not create a new version for each of 
your deployments. You can also name versions after your Git branches (for example: master, develop).

### 8) Check if Datastore is enabled

If it's not enabled automatically, just type "Datastore" in the Search box on Google Cloud Platform. Once you click on 
the selection, the Datastore will be automatically enabled.

## Links:

- [Index](/README.md#documentation)
