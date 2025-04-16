from django.test import TestCase
from publications.models import Publication
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class TestSearch(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password='testpassword')
        self.publication = Publication.objects.create(text='A publication',author=self.user)
        self.publication2 = Publication.objects.create(text='bla bla',author=self.user)

    def test_search_by_text_publication(self):
        search_term = 'A publication'
        response = self.client.get(
            reverse('publications:search') + f'?q={search_term}',
            data={'q':search_term}
        )
        self.assertIn(self.publication,response.context['results'])
        self.assertNotIn(self.publication2,response.context['results'])
    
    def test_search_by_author_publication(self):
        search_term = 'testuser'
        response = self.client.get(
            reverse('publications:search') + f'?q={search_term}',
            data={'q':search_term}
        )
        self.assertIn(self.publication,response.context['results'])
        self.assertIn(self.publication2,response.context['results'])
        