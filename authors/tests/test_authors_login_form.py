from unittest import TestCase
from authors.forms import LoginForm
from django.utils.translation import gettext_lazy as _


class AuthorsLoginUnitTest(TestCase):
    def test_login_form_fields_labels(self):
        form = LoginForm()
        self.assertEqual(form['username'].field.label, _('Username'))
        self.assertEqual(form['password'].field.label, _('Password'))
