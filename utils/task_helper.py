import json
import os

import requests
from google.cloud import tasks_v2

from utils.check_environment import is_local


def run_background_task(relative_path, payload, project=None, queue=None, location=None):
    if is_local():
        if os.environ.get("TESTING") != "yes":  # pytest has issues with running requests
            requests.post("http://localhost:8080{relative_path}".format(relative_path=relative_path),
                          data=json.dumps(payload).encode(),
                          headers={"Content-type": "application/octet-stream"})
    else:
        # production
        if not project:
            project = os.environ.get("GOOGLE_CLOUD_PROJECT")  # this is a default environment variable on GAE

        if not queue:
            queue = "default"

        if not location:
            location = os.environ.get("MY_GAE_REGION")

        # make sure you have Cloud Tasks API enabled via the Google Cloud Console
        client = tasks_v2.CloudTasksClient()

        # Construct the fully qualified queue name.
        parent = client.queue_path(project, location, queue)

        task = {
            'app_engine_http_request': {
                'http_method': 'POST',
                'relative_uri': relative_path,
                'body': json.dumps(payload).encode(),
            }
        }

        client.create_task(parent, task)
