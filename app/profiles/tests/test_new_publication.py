from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from profiles.forms import PublicationForm
from profiles.models import Profile
from publications.models import Publication

User = get_user_model()


class PublicationUnitTest(TestCase):
    def test_publication_form_fields(self):
        form = PublicationForm()
        self.assertEqual(form['text'].field.label, _('Text publication'))
        self.assertEqual(form['img'].field.label, _('Image'))


class NewPublicationIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_new_publication_view_renders_form(self):
        url = reverse('profiles:new_publication', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/create_publication.html')
        self.assertIn('form', response.context)

    def test_new_publication_create_valid_data(self):
        url = reverse('profiles:new_publication_create', kwargs={'username': self.user.username})
        data = {'text': 'Test publication text'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Publication.objects.filter(author=self.user, text='Test publication text').exists())

    def test_new_publication_create_invalid_data(self):
        url = reverse('profiles:new_publication_create', kwargs={'username': self.user.username})
        data = {'text': ''} 
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Publication.objects.filter(author=self.user).exists())