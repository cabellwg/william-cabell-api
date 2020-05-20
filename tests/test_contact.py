import unittest
from unittest.mock import patch

import flask_app


class TestContact(unittest.TestCase):
    """Tests the contact API."""

    @patch("flask_app.sentry_sdk", autospec=True)
    def setUp(self, _):
        """Runs before each test method."""
        self.client = flask_app.create_app(test_env="test").test_client()

    @patch("flask_app.contact.sendgrid", autospec=True)
    def test_contact_normal(self, _):
        """Tests the contact API with complete data."""
        test_data_normal = {
            "name": "Eratosthenes",
            "organization": "Library of Alexandria",
            "email": "bequietwhenyoure@thelibrary.please",
            "message": "Hey man – you want some primes for real cheap? I got "
                       "some, real good, too – you don't need to know how – "
                       "listen, don't worry about it man, totally safe – yeah, "
                       "I promise – had some myself last week – alright, always"
                       " happy to do business with you."
        }
        r = self.client.post("/contact", json=test_data_normal)
        self.assertEqual(200, r.status_code)

    @patch("flask_app.contact.sendgrid", autospec=True)
    def test_contact_partially_empty(self, _):
        """Tests the contact API with normal (partially empty) contact data."""
        test_data_without_org = {
            "name": "Pierre de Fermat",
            "email": "pfermat@univ-orleans.fr",
            "message": "I have a wonderful message which the memory buffer of "
                       "this process is too small to contain."
        }

        r = self.client.post("/contact", json=test_data_without_org)
        self.assertEqual(200, r.status_code)

    @patch("flask_app.contact.sendgrid", autospec=True)
    def test_contact_dirty(self, _):
        """Tests the contact API with an attempted injection."""
        test_data_dirty_input = {
            "name": "\" raise Exception(\"We are Legion.\") #",
            "email": "test@test"
        }

        r = self.client.post("/contact", json=test_data_dirty_input)
        self.assertEqual(400, r.status_code)


if __name__ == "__main__":
    unittest.main()
