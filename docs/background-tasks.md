# Background tasks

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

## Links:

- [Index](/README.md#documentation)
