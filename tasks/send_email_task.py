import json
import logging

from flask import request

from utils.check_environment import is_local


def send_email_via_sendgrid():
    if is_local():
        # localhost
        data = json.loads(request.get_data(as_text=True))

        recipient_email = data.get("recipient_email")
        sender_email = data.get("sender_email")
        email_subject = data.get("email_subject")
        email_body = data.get("email_body")

        logging.warning("SEND EMAIL: Not really sending email because we're on localhost.")
        logging.warning("Recipient: {}".format(recipient_email))
        logging.warning("Sender: {}".format(sender_email))
        logging.warning("Subject: {}".format(email_subject))
        logging.warning("Body: {}".format(email_body))
    else:
        # production
        if request.headers.get("X-AppEngine-QueueName"):
            # If the request has this header (X-AppEngine-QueueName), then it really came from Google Cloud Tasks.
            # Third-party requests that contain headers started with X are stripped of these headers once they hit GAE
            # servers. That's why no one can fake these headers.

            data = json.loads(request.get_data(as_text=True))

            recipient_email = data.get("recipient_email")
            sender_email = data.get("sender_email")
            email_subject = data.get("email_subject")
            email_body = data.get("email_body")

            # TODO: send via SendGrid

    return "true"
