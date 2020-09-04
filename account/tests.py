from django.test import TestCase

from django.test import TestCase, client
from unittest.mock import patch, MagicMock

from .models import (
    Account,
    SocialMedia
)

class GoogleLoginTest(TestCase):
    def setUp(self):
        Account(
            email_account = 'soheonlee@gmail.com',
            social_media_id = 3
        ).save()

    def tearDown(self):
        Account.objects.all().delete()

    def test_google_login_success(self)
