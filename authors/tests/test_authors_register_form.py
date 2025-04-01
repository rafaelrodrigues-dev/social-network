from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from authors.forms import RegisterForm
from django.utils.translation import gettext as _


class AuthorsRegisterUnitTest(TestCase):
    def test_register_form_fields_labels(self):
        form = RegisterForm()
        self.assertEqual(form['date_of_birth'].field.label, _('Date of birth'))
        self.assertEqual(form['gender'].field.label, _('Gender'))
    

class AuthorsRegisterIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.form_data = {
            'username': 'validuser123',
            'password': 'validpassword',
            'first_name': 'Valid',
            'last_name': 'User',
            'email': 'valid@email.com',
            'date_of_birth': '2000-01-01', 
            'gender': 'M'
        }
        return super().setUp()
    
    def test_clean_username_with_existing_username(self):
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data,follow=True)
        response = self.client.post(url, data=self.form_data,follow=True)

        msg = _('This username is already in use')
        self.assertIn(msg,response.content.decode('utf-8'))

    def test_clean_username_with_non_alphanumeric(self):
        url = reverse('authors:register_create')
        self.form_data['username'] = 'invaliduser!@#'
        response = self.client.post(url, data=self.form_data,follow=True)

        msg = _('Username must be alphanumeric')
        
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_clean_email_with_existing_email(self):
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data,follow=True)
        response = self.client.post(url, data=self.form_data,follow=True)

        msg = _('This email is already in use')
        self.assertIn(msg,response.content.decode('utf-8'))
    
    def test_register_create_if_http_method_is_not_post(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)