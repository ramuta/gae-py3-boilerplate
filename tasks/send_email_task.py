import json
import logging
from flask import request
from sendgrid import SendGridAPIClient, Asm, Mail, Attachment
from sendgrid.helpers import mail
from models.app_settings import AppSettings
from utils.check_environment import is_local


def send_email_via_sendgrid():
    """A background task that sends an email via SendGrid."""
    data = json.loads(request.get_data(as_text=True))

    recipient_email = data.get("recipient_email")
    sender_email = data.get("sender_email")
    sender_name = data.get("sender_name")
    email_subject = data.get("email_subject")
    email_body = data.get("email_body")
    unsubscribe_group = data.get("unsubscribe_group")
    attachment_content_b64 = data.get("attachment_content_b64")
    attachment_filename = data.get("attachment_filename")
    attachment_filetype = data.get("attachment_filetype")

    if is_local():
        # localhost (not really sending the email)
        logging.warning("SEND EMAIL: Not really sending email because we're on localhost.")
        logging.warning("Recipient: {}".format(recipient_email))
        logging.warning("Sender: {0}, {1}".format(sender_name, sender_email))
        logging.warning("Subject: {}".format(email_subject))
        logging.warning("Body: {}".format(email_body))

        return "{sender_email} {email_subject}".format(sender_email=sender_email, email_subject=email_subject)
    else:
        # production (sending the email via SendGrid)
        if request.headers.get("X-AppEngine-QueueName"):
            # If the request has this header (X-AppEngine-QueueName), then it really came from Google Cloud Tasks.
            # Third-party requests that contain headers started with X are stripped of these headers once they hit GAE
            # servers. That's why no one can fake these headers.

            # SendGrid setup
            sg = SendGridAPIClient(api_key=AppSettings.get().sendgrid_api_key)

            # Set up email message
            email_message = Mail(from_email=mail.Email(email=sender_email, name=sender_name),
                                 to_emails=recipient_email, subject=email_subject, html_content=email_body)

            if attachment_content_b64 and attachment_content_b64 is not None and attachment_content_b64 != "":
                attachment = Attachment()
                attachment.content = attachment_content_b64
                attachment.type = "text/{}".format(attachment_filetype)
                attachment.filename = attachment_filename
                attachment.disposition = "attachment"

                email_message.add_attachment(attachment)

            # Unsubscribe group (ASM)
            if unsubscribe_group:
                try:
                    email_message.asm(Asm(group_id=int(unsubscribe_group)))
                except Exception as e:
                    pass

            try:
                response = sg.send(email_message)
                logging.info(response.status_code)
                logging.info(response.body)
                logging.info(response.headers)
            except Exception as e:
                logging.error(str(e))

        return "true"
