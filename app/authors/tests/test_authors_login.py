from unittest import TestCase
from authors.forms import LoginForm
from django.utils.translation import gettext_lazy as _
from django.test import TestCase as DjangoTestCase
from django.urls import reverse


class AuthorsLoginUnitTest(TestCase):
    def test_login_form_fields_labels(self):
        form = LoginForm()
        self.assertEqual(form['username'].field.label, _('Username'))
        self.assertEqual(form['password'].field.label, _('Password'))

class AuthorsLoginIntegrationtest(DjangoTestCase):
    def test_login_create_if_method_is_not_post(self):
        response =self.client.get(reverse('authors:login_create'))
        self.assertEqual(response.status_code,404)
    
    def test_login_invalid_form(self):
        data = {'username':'','password':''}

        response = self.client.post(reverse('authors:login_create'),data=data,follow=True)
        self.assertIn(str(_('Invalid username or password')),response.content.decode('utf-8'))
        self.assertRedirects(response,reverse('authors:login'))

    def test_login_invalid_credentials(self):
        data = {'username':'invaliduser','password':'invalidpassword'}

        response = self.client.post(reverse('authors:login_create'),data=data,follow=True)
        self.assertIn(str(_('Invalid credentials')),response.content.decode('utf-8'))
        self.assertRedirects(response,reverse('authors:login'))