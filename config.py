import os
import sys


def read_secret(secret_name):
    if secret_name is None:
        print("Missing secret definition", file=sys.stderr)
        return None
    with open("/run/secrets/" + secret_name) as s:
        secret = s.read().strip()
        if secret == "":
            print("Empty secret {}".format(secret_name))
        return secret


class Config:
    """Settings for all environments"""
    DEBUG = True
    TESTING = True
    CORS_ALLOWED_ORIGINS = ["*"]
    SENTRY_DSN = "https://6a4146160300401b89cd1d16adb13237@o395084.ingest.sentry.io/5246345"
    MY_EMAIL_ADDR = "william16180@gmail.com"
    SERVER_EMAIL_ADDR = "contact-form@williamcabell.me"
    SENDGRID_API_KEY = "test-sendgrid-key"


class ProdConfig(Config):
    """Production settings"""
    DEBUG = False
    TESTING = False
    CORS_ALLOWED_ORIGINS = ["https://williamcabell.me",
                            "https://www.williamcabell.me"]
    SENDGRID_API_KEY = read_secret(os.environ.get("SENDGRID_API_KEY_SECRET"))


class TestConfig(Config):
    """Test settings"""
    pass


class DevConfig(Config):
    """Development settings"""
    pass
