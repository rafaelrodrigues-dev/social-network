from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from publications.models import Publication

User = get_user_model()

class CreatePublicationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('publications:create-publication')
        self.home_url = reverse('publications:home')
        self.login_url = reverse('authors:login')

    def test_create_publication_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'text': 'This is a test publication text.'
        }
        # Initially there are no publications
        self.assertEqual(Publication.objects.count(), 0)

        response = self.client.post(self.url, data=data)
        
        # Verify redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

        # Verify creation in database
        self.assertEqual(Publication.objects.count(), 1)
        publication = Publication.objects.first()
        self.assertEqual(publication.text, 'This is a test publication text.')
        self.assertEqual(publication.author, self.user)

    def test_create_publication_unauthenticated(self):
        data = {
            'text': 'Unauthenticated publication text.'
        }
        response = self.client.post(self.url, data=data)
        
        # Verify redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')
        
        # Verify no database record was created
        self.assertEqual(Publication.objects.count(), 0)

    def test_create_publication_invalid_method(self):
        self.client.login(username='testuser', password='testpassword')
        # GET request should be blocked (405)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Publication.objects.count(), 0)
