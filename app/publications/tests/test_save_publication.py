from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from publications.models import Publication

User = get_user_model()


class SavePublicationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = User.objects.create_user(username='author', password='authorpassword')
        self.publication = Publication.objects.create(
            text='Test publication to save',
            author=self.author
        )
        self.save_url = reverse('publications:save', kwargs={'pk': self.publication.pk})
        self.login_url = reverse('authors:login')

    def test_save_publication_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(self.save_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'saved': True
        })
        self.assertIn(self.publication, self.user.saved.all())

    def test_unsave_publication_authenticated(self):
        # Pre-save the publication
        self.user.saved.add(self.publication)
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(self.save_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'saved': False
        })
        self.assertNotIn(self.publication, self.user.saved.all())

    def test_save_publication_unauthenticated(self):
        response = self.client.post(self.save_url)
        
        # Check redirect to login since login_required decorator is applied
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.save_url}')
        self.assertNotIn(self.publication, self.user.saved.all())

    def test_save_publication_invalid_method(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(self.save_url)
        
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
        self.assertNotIn(self.publication, self.user.saved.all())

    def test_save_nonexistent_publication(self):
        self.client.login(username='testuser', password='testpassword')
        nonexistent_url = reverse('publications:save', kwargs={'pk': 9999})
        
        response = self.client.post(nonexistent_url)
        
        self.assertEqual(response.status_code, 404)
