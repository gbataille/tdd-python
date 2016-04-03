from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.test import TestCase

from accounts.authentication import (
        PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
        )

User = get_user_model()


@patch('accounts.authentication.requests.post')
class AuthenticationTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        user = User(email='other@user.com')
        user.username = 'otheruser'
        user.save()

    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('an assertion')
        mock_post.assert_called_once_with(
                PERSONA_VERIFY_URL,
                data={'assertion': 'an assertion', 'audience': DOMAIN}
                )

    def test_returns_none_if_requests_errors(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}

        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_returns_none_if_status_not_okay(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'not okay!'}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        user = User.objects.create(email='a@b.com')
        mock_post.return_value.json.return_value = {
                'status': 'okay',
                'email': 'a@b.com'
                }
        found_user = self.backend.authenticate('an assertion')
        self.assertEqual(user, found_user)
