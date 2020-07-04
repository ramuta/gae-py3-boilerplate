import os

from flask import url_for

from utils.check_environment import is_local
from utils.task_helper import run_background_task
from utils.translations import render_template_with_translations


def send_email(recipient_email, email_template, email_params, email_subject, sender_email=None, sender_name=None,
               unsubscribe_group=None, attachment_content_b64=None, attachment_filename=None, attachment_filetype=None):
    if not sender_email:
        sender_email = os.environ.get("MY_APP_EMAIL")  # set this in app.yaml

    if not sender_name:
        sender_name = os.environ.get("MY_APP_NAME")  # set this in app.yaml

    # send web app URL data by default to every email template
    if is_local():
        email_params["app_root_url"] = "http://localhost:8080"
    else:
        email_params["app_root_url"] = os.environ.get("MY_APP_URL")  # set this in app.yaml

    email_params["my_app_name"] = os.environ.get("MY_APP_NAME")

    # render the email HTML body
    email_body = render_template_with_translations(email_template, **email_params)

    # params sent to the background task
    payload = {"recipient_email": recipient_email, "email_subject": email_subject, "sender_email": sender_email,
               "email_body": email_body, "unsubscribe_group": unsubscribe_group, "sender_name": sender_name,
               "attachment_content_b64": attachment_content_b64, "attachment_filename": attachment_filename,
               "attachment_filetype": attachment_filetype}

    run_background_task(relative_path=url_for("tasks.send_email_task.send_email_via_sendgrid"),
                        payload=payload, queue="email", project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
                        location=os.environ.get("MY_GAE_REGION"))
