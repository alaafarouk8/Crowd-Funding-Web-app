from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, users, timestamp):
        return (
            six.text_type(users.pk) + six.text_type(timestamp) +
            six.text_type(users.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()
