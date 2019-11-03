import logging

from utils.check_environment import is_local
from utils.translations import render_template_with_translations


def send_email(recipient_email, email_template, email_params, email_subject, sender_email=None, unsubscribe_group=None,
               attachment_content_b64=None, attachment_filename=None, attachment_filetype=None):
    if not sender_email:
        sender_email = "info@your.webapp"

    email_body = render_template_with_translations(email_template, **email_params)

    if not is_local():
        # production
        # TODO: send email via SendGrid
        pass
    else:
        # localhost
        logging.warning("SEND EMAIL: Not really sending email because we're on localhost.")
        logging.warning("Recipient: {}".format(recipient_email))
        logging.warning("Sender: {}".format(sender_email))
        logging.warning("Subject: {}".format(email_subject))
        logging.warning("Body: {}".format(email_body))
