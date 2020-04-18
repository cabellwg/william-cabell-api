import datetime
import json
import os

import sendgrid

from pytz import timezone
from sendgrid.helpers.mail import *

from flask_app.errors import FormValidationException, \
    APIKeyReadException, \
    SendGridConnectionException

MY_EMAIL_ADDR = "william16180@gmail.com"
SERVER_EMAIL_ADDR = "contact-form@williamcabell.me"


def send_contact_email(contact):
    """Writes a new message on the system with the information someone has sent me.

    :param contact: The information to send.
    :returns: True if there were no errors, false if there were validation
    errors.
    """
    name = contact.get("name")
    org = contact.get("organization") or "Not given"
    email_addr = contact.get("email")
    msg = contact.get("message")

    # Validate input
    if name is None or email_addr is None or msg == "" or msg is None:
        raise FormValidationException("Invalid form data")

    # Construct body of message
    tz = timezone("EST")
    text = "Name: {}\n".format(name)
    text += "Organization: {}\n".format(org)
    text += "Email: {}\n".format(email_addr)
    text += "{}UTC\n".format(datetime.datetime.utcnow())
    text += "{}EST\n".format(datetime.datetime.now(tz))
    text += "---------------------\n"
    text += "Message: {}\n".format(msg)

    # Construct email
    body = Content("text/plain", text)
    subj = "Someone used the form!"
    server_email = Email(SERVER_EMAIL_ADDR)
    my_email = To(MY_EMAIL_ADDR)
    email_msg = Mail(server_email, my_email, subj, body)

    # Get API key
    api_key_file = ".auth_keys.json"
    if not os.path.exists(api_key_file):
        raise APIKeyReadException("API key file does not exist")
    with open(api_key_file, 'r') as auth_file:
        sendgrid_api_key = json.loads(auth_file.read())["sendgrid"]
        if len(sendgrid_api_key) == 0:
            raise APIKeyReadException("Length is 0")
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)

        # Send email
        try:
            sg.send(email_msg)
        except Exception as e:
            print(e)
            raise SendGridConnectionException("Connection to SendGrid failed")
