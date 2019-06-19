import datetime

import yagmail


def send_contact_email(contact):
    """Sends me an email with the information someone has sent me.

    :param contact: The information to send.
    """
    name = contact.get("name") or ""
    org = contact.get("organization") or ""
    email = contact.get("email") or ""
    msg = contact.get("message") or ""

    # Construct message
    text = "+===========================\n+\n+ "
    text += str(datetime.datetime.utcnow()) + "\n+ "
    text += "Name: " + name + "\n+ "
    text += "Organization: " + org + "\n+ "
    text += "Email: " + email + "\n+ "
    text += "---------------------------\n+ "
    text += "Message: " + msg + "\n+ "
    text += "\n+\n+===========================\n"

    yag = yagmail.SMTP("william16180@gmail.com", oauth2_file="/run/secrets/gmail-keys")
    yag.send("william16180@gmail.com", "Someone used the form!", text)
