from django.test import TestCase
from django.contrib.auth import get_user_model
from publications.models import Publication
from django.urls import reverse

User = get_user_model()


class PublicationHome(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='master', password='123')
        self.url = reverse('publications:home')

    def test_publication_home_template_loads_publications(self):
        needed = 'This is a publication'
        Publication.objects.create(text=needed, author=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publications/pages/home.html')
        content = response.content.decode('utf-8')
        self.assertIn(needed, content)

    def test_publication_home_pagination(self):
        # Create 5 publications (per_page is 4)
        for i in range(5):
            Publication.objects.create(text=f'Publication {i}', author=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Check first page context has 4 items
        self.assertEqual(len(response.context['page_obj']), 4)

        # Check second page has 1 item
        response = self.client.get(self.url + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 1)