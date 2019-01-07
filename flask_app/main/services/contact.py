import datetime
import smtplib
import json
import os
import flask_app


def add_contact(contact):
    path = os.path.dirname(flask_app.__file__) + "/"

    name = contact["name"] or ""
    org = contact["organization"] or ""
    email = contact["email"] or ""
    msg = contact["message"] or ""

    # Construct message
    text  = "+===========================\n+\n+ "
    text += str(datetime.datetime.utcnow()) + "\n+ "
    text += "Name: "         + name  + "\n+ "
    text += "Organization: " + org   + "\n+ "
    text += "Email: "        + email + "\n+ "
    text += "---------------------------\n+ "
    text += "Message: "      + msg   + "\n+ "
    text += "\n+\n+===========================\n"

    # Write to log
    with open(path + "logs/contact.txt", "r") as original:
        data = original.read()
    with open(path + "logs/contact.txt", "w") as modified:
        modified.write(text + data)
