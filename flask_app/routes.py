from flask import request, make_response
from flask_cors import cross_origin

from flask_app.contact import send_contact_email


def apply_routes(app):
    """Applies URL routes to the Flask app.

    :param app: The Flask app to which to apply the routes.
    """

    @app.route("/contact")
    @cross_origin(origins=["https://williamcabell.me"],
                  allow_headers=["Content-Type"],
                  methods=["POST"])
    def contact():
        """Route for the contact form."""
        if send_contact_email(request.get_json()):
            return jsonify_no_content(app, 200)
        return jsonify_no_content(app, 400)


def jsonify_no_content(app, status):
    """Creates a response with no content with MIME type application/json.

    :param app: The Flask app
    :param status: The status code to give the response
    :return: An empty JSON response
    """
    response = make_response("", status)
    response.mimetype = app.config["JSONIFY_MIMETYPE"]

    return response
