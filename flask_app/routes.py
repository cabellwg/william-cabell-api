from flask import request, make_response, jsonify
from flask_cors import cross_origin

from flask_app.contact import send_contact_email
from flask_app.errors import *


def apply_routes(app):
    """Applies URL routes to the Flask app.

    :param app: The Flask app to which to apply the routes.
    """

    @app.route("/contact", methods=["POST"])
    @cross_origin(origins=["https://williamcabell.me",
                           "https://www.williamcabell.me"],
                  allow_headers=["Content-Type"],
                  methods=["POST"])
    def contact():
        """Route for the contact form."""
        try:
            send_contact_email(request.get_json())
        except FormValidationException:
            return jsonify_response(app,
                                    400,
                                    "Invalid form data")
        except APIKeyReadException:
            return jsonify_response(app,
                                    500,
                                    "Encountered unexpected server error f")
        except SendGridConnectionException:
            return jsonify_response(app,
                                    500,
                                    "Encountered unexpected server error s")
        return jsonify_no_content(app, 200)

    @app.route("/healthcheck", methods=["GET"])
    def healthcheck():
        """Route for the healthcheck."""
        return b"", 200


def jsonify_no_content(app, status):
    """Creates a response with no content with MIME type application/json.

    :param app: The Flask app
    :param status: The status code to give the response
    :return: An empty JSON response
    """
    response = make_response("", status)
    response.mimetype = app.config["JSONIFY_MIMETYPE"]

    return response


def jsonify_response(app, status, message):
    """Creates a response with MIME type application/json with a message.

    :param app: The Flask app
    :param status: The status code to give the response
    :param message: The message to include with the response
    :return: A JSON response of the form { "message": %message% }
    """
    response = jsonify({"message": message})
    response.status_code = status

    return response
