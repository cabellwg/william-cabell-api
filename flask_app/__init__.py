import os

import sentry_sdk

from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration


def create_app(test_env="prod"):
    """Builds the Flask app.

    :param test_env: An optional test configuration for testing.
    :return: The application.
    """
    app = Flask(__name__)

    env = test_env if test_env is not None else os.environ["ENV"]

    if env == "prod":
        app.config.from_object("config.ProdConfig")
    elif env == "test":
        app.config.from_object("config.TestConfig")
    else:
        app.config.from_object("config.DevConfig")

    sentry_sdk.init(
            dsn=app.config["SENTRY_DSN"],
            integrations=[FlaskIntegration()]
    )

    @app.route("/healthcheck", methods=["GET"])
    def healthcheck():
        """Route for the healthcheck."""
        return b"", 200

    from . import contact
    app.register_blueprint(contact.build_bp(app))

    return app


if __name__ == "__main__":
    application = create_app()
    application.run()
