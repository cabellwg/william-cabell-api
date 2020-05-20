class ContactInfoException(Exception):
    """An exception relating to the information sent through the contact form."""

    def __init__(self, msg):
        self.msg = msg
