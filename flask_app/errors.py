class FormValidationException(Exception):
    """Thrown when form validation fails."""
    pass


class APIKeyReadException(Exception):
    """Thrown when the API key cannot be read."""
    pass


class SendGridConnectionException(Exception):
    """Thrown when connection to SendGrid fails."""
    pass
