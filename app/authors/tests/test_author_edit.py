import datetime
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from authors.forms import EditAuthorForm
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()


class AuthorsEditUnitTest(TestCase):
    def test_edit_form_fields_labels(self):
        form = EditAuthorForm()
        self.assertEqual(form['date_of_birth'].field.label, _('Date of birth'))
        self.assertEqual(form['gender'].field.label, _('Gender'))


class AuthorsEditIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.data = {
            'username':'testuser',
            'password':'testpassword',
            'first_name':'testuser',
            'last_name':'lastuser',
            'date_of_birth':'1971-01-01',
        }
        self.user = User.objects.create_user(**self.data)
        Profile.objects.filter(user=self.user).update(bio='This is a bio')
        self.client.login(username='testuser',password='testpassword')

    def test_edit_author_page_loads_correct_data(self):
        response = self.client.get(reverse('authors:edit_author'))
        self.assertIn('testuser',response.content.decode('utf-8'))
        self.assertIn('This is a bio',response.content.decode('utf-8'))
        self.assertIn('lastuser',response.content.decode('utf-8'))

    def test_edit_author_form_redirects_to_home(self):
        response = self.client.post(reverse('authors:edit_author'), {
            'username': self.user.username,
            'first_name': self.user.first_name,
            'date_of_birth': self.user.date_of_birth,
        })
        self.assertRedirects(response, reverse('publications:home'))

    def test_edit_author_first_name(self):
        needed = 'newfirstname'

        self.client.post(reverse('authors:edit_author'), {
            'first_name': needed,
            'date_of_birth': self.user.date_of_birth,
        })
        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, needed)

    def test_edit_author_date_of_birth(self):
        self.client.post(reverse('authors:edit_author'), {
            'first_name': self.user.first_name,
            'date_of_birth': '2000-01-01'
        })
        self.user.refresh_from_db()

        self.assertEqual(self.user.date_of_birth, datetime.date(2000, 1, 1))

    def test_edit_author_last_name(self):
        needed = 'newlastname'

        self.client.post(reverse('authors:edit_author'), {
            'first_name': self.user.first_name,
            'date_of_birth': self.user.date_of_birth,
            'last_name': needed
        })
        self.user.refresh_from_db()

        self.assertEqual(self.user.last_name, needed)

    def test_edit_author_bio(self):
        needed = 'newbio'

        self.client.post(reverse('authors:edit_author'), {
            'first_name': self.user.first_name,
            'date_of_birth': self.user.date_of_birth,
            'bio': needed
        })
        self.user.refresh_from_db()

        self.assertEqual(self.user.profile.bio, needed)

    def test_edit_author_gender(self):
        needed = 'M'
        self.client.post(reverse('authors:edit_author'), {
            'first_name': self.user.first_name,
            'date_of_birth': self.user.date_of_birth,
            'gender': needed
        })
        self.user.refresh_from_db()

        self.assertEqual(self.user.gender, needed)