from django.test import TestCase
from django.contrib.auth import get_user_model
from publications.models import Publication
from django.urls import reverse


User = get_user_model()

class LikeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.publication = Publication.objects.create(text='Test publication', author=self.user)

    def test_like_publication(self):
        url = reverse('publications:like', args=(self.publication.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'liked': True,
            'likes_count': '1',
        })
        self.assertIn(self.user, self.publication.like.all())

    def test_unlike_publication(self):
        self.publication.like.add(self.user)  # Pre-like the publication
        url = reverse('publications:like', args=(self.publication.pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'liked': False,
            'likes_count': '0',
        })
        self.assertNotIn(self.user, self.publication.like.all())

    def test_like_invalid_request_method(self):
        url = reverse('publications:like', args=(self.publication.pk,))
        response = self.client.get(url)  # Sending GET instead of POST
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode('utf-8'), {
            'error': 'Invalid request',
        })