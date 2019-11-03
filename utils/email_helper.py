from flask import url_for

from models.app_settings import AppSettings
from utils.check_environment import is_local
from utils.task_helper import run_background_task
from utils.translations import render_template_with_translations


def send_email(recipient_email, email_template, email_params, email_subject, sender_email=None, unsubscribe_group=None,
               attachment_content_b64=None, attachment_filename=None, attachment_filetype=None):
    if not sender_email:
        sender_email = "info@your.webapp"

    # send web app URL data by default to every email template
    if is_local():
        email_params["app_root_url"] = "http://localhost:8080"
    else:
        email_params["app_root_url"] = AppSettings.gc_url

    # render the email HTML body
    email_body = render_template_with_translations(email_template, **email_params)

    # params sent to the background task
    payload = {"recipient_email": recipient_email, "email_subject": email_subject, "sender_email": sender_email,
               "email_body": email_body}

    run_background_task(relative_path=url_for("tasks.send_email_task.send_email_via_sendgrid"),
                        payload=payload, queue="email", project=AppSettings.gc_project_name,
                        location=AppSettings.gc_region)
