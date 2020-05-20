import datetime

import sendgrid

from flask import (
    Blueprint, jsonify, request
)
from flask_cors import cross_origin
from pytz import timezone
from sendgrid.helpers.mail import Content, Email, To, Mail
from sentry_sdk import capture_exception

from .errors import ContactInfoException


def build_bp(app):
    """Factory wrapper for contact blueprint.

    :param app: The app, to get configuration settings.
    :return: A blueprint for the contact API.
    """
    bp = Blueprint("contact", __name__)

    # Begin route definitions

    @bp.route("/contact", methods=["POST"])
    @cross_origin(origins=app.config["CORS_ALLOWED_ORIGINS"],
                  allow_headers=["Content-Type"],
                  methods=["POST"])
    def send_contact_email():
        """Emails me with the information someone has sent me.

        :return: One of the following:
            200 if the message was sent,
            400 if the message was invalid,
            500 if the server had a problem sending the email.
        """
        try:
            email = construct_email({
                "name": request.json.get("name"),
                "org": request.json.get("organization") or "Not given",
                "email": request.json.get("email"),
                "msg": request.json.get("message")
            }, app.config["SERVER_EMAIL_ADDR"], app.config["MY_EMAIL_ADDR"])
        except ContactInfoException as e:
            return jsonify({"msg": "{}".format(e.msg)}), 400

        sg = sendgrid.SendGridAPIClient(api_key=app.config["SENDGRID_API_KEY"])

        # Send email
        try:
            sg.send(email)
        except Exception as e:
            capture_exception(e)
            return jsonify({"msg": "Encountered unexpected server error"}), 500

        return jsonify({}), 200

    # End route definitions

    return bp


def construct_email(primitives, server_addr, my_addr):
    """Tries to build an email from the information in the request.

    :param primitives: The raw request information.
    :param server_addr: The email address of the server.
    :param my_addr: My email address.
    :return
    """
    # Validate input
    for (key, item) in primitives.items():
        if item is None:
            raise ContactInfoException(msg="Missing attribute: \"{}\"".format(key))
        if not isinstance(item, str) or not len(item) > 0:
            raise ContactInfoException(msg="Attribute \"{}\" must be a nonempty string".format(key))

    # Construct body of message
    tz = timezone("EST")
    text = "Name: {}\n".format(primitives["name"])
    text += "Organization: {}\n".format(primitives["org"])
    text += "Email: {}\n".format(primitives["email"])
    text += "{}UTC\n".format(datetime.datetime.utcnow())
    text += "{}EST\n".format(datetime.datetime.now(tz))
    text += "---------------------\n"
    text += "Message: {}\n".format(primitives["msg"])

    # Construct email
    body = Content("text/plain", text)
    subj = "Someone used the form!"
    server_email = Email(server_addr)
    my_email = To(my_addr)
    return Mail(server_email, my_email, subj, body)
