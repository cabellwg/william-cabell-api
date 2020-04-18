import os
import unittest
from unittest.mock import patch

import flask_app


def true_util():
    return True


class TestContact(unittest.TestCase):
    """Tests the contact API."""

    def setUp(self):
        """Runs before each test method."""
        self.client = flask_app.create_app({'TESTING': True}).test_client()
        with open(".auth_keys.json", 'w') as mock_auth_file:
            mock_auth_file.truncate(0)
            mock_auth_file.write("{\"sendgrid\": \"mock_api_key_string\"}")

    def tearDown(self):
        """Runs after each test method."""
        os.remove(".auth_keys.json")

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
        r = self.client.post('/contact', json=test_data_normal)
        print(r.data)
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

        self.assertEqual(200, self.client.post('/contact',
                                               json=test_data_without_org
                                               ).status_code)

    @patch("flask_app.contact.sendgrid", autospec=True)
    def test_contact_dirty(self, _):
        """Tests the contact API with an attempted injection."""
        test_data_dirty_input = {
            "name": "\" raise Exception(\"We are Legion.\") #",
            "email": "test@test"
        }

        self.assertEqual(400, self.client.post('/contact',
                                               json=test_data_dirty_input
                                               ).status_code)


if __name__ == '__main__':
    unittest.main()
