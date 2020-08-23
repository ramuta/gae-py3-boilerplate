# Configure Google Cloud Build

In order to set up CI via `cloudbuild-develop.yaml` and `cloudbuild-production.yaml`, you need to configure a few things.

## Make sure Cloud Build API is enabled

Find Cloud Build API via the Cloud Console search and make sure it's enabled.

## IAM

- Go to the Google Cloud Console -> IAM & admin -> IAM.
- Locate the service account (`[PROJECT_NUMBER]@cloudbuild.gserviceaccount.com`) and click the pencil icon.
- Add the role "Project > Editor" to the service account.

## Trigger: Connect your GitHub or BitBucket account

Create a trigger which would monitor your repository on GitHub or BitBucket and trigger a build whenever something is 
uploaded to the develop or master branch (you can have two triggers, one for each branch).

Make sure to set up the correct branch in the trigger (`^develop$` or `^master$` or something else) and to enter the 
Cloud Build configuration file location (`cloudbuild-develop.yaml` or `cloudbuild-production.yaml`)