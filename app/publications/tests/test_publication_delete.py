from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from publications.models import Publication

User = get_user_model()

class DeletePublicationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.publication = Publication.objects.create(
            author=self.user,
            text='Test publication text'
        )
        self.delete_url = reverse('publications:delete-publication', kwargs={'pk': self.publication.pk})
        self.login_url = reverse('authors:login')
        self.home_url = reverse('publications:home')

    def test_delete_publication_authenticated_author(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertRedirects(response, self.home_url)
        self.assertFalse(Publication.objects.filter(pk=self.publication.pk).exists())

    def test_delete_publication_authenticated_not_author(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 403)  # Forbidden
        self.assertTrue(Publication.objects.filter(pk=self.publication.pk).exists())

    def test_delete_publication_unauthenticated(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, f'{self.login_url}?next={self.delete_url}')
        self.assertTrue(Publication.objects.filter(pk=self.publication.pk).exists())

    def test_delete_publication_nonexistent(self):
        self.client.login(username='testuser', password='testpassword')
        nonexistent_url = reverse('publications:delete-publication', kwargs={'pk': 999})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)  # Not Found