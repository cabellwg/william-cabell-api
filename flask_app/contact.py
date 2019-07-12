import datetime

import yagmail
from pytz import timezone


def send_contact_email(contact):
    """Sends me an email with the information someone has sent me.

    :param contact: The information to send.
    :returns: True if there were no errors, false if there were validation
    errors.
    """
    name = contact.get("name")
    org = contact.get("organization") or "Not given"
    email = contact.get("email")
    msg = contact.get("message")

    if name is None or email is None or msg == "":
        return False

    tz = timezone('EST')

    # Construct message
    text = str(datetime.datetime.utcnow()) + "\n"
    text += str(datetime.datetime.now(tz)) + "\n"
    text += "Name: " + name + "\n"
    text += "Organization: " + org + "\n"
    text += "Email: " + email + "\n"
    text += "---------------------------\n"
    text += "Message: " + msg + "\n"

    yag = yagmail.SMTP("william16180@gmail.com", oauth2_file="/run/secrets/gmail-keys")
    yag.send("william16180@gmail.com", "Someone used the form!", text)

    return True
