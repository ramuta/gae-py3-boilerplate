# Cron jobs

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

## Links:

- [Index](/README.md#documentation)
