from django.test import TestCase
from django.contrib.auth import get_user_model
from publications.models import Publication
from django.urls import reverse

User = get_user_model()


class PublicationTest(TestCase):
    # homepage
    def test_publication_home_template_loads_publications(self):
        needed ='This is a publication'
        user = User.objects.create_user(username='master',password='123')
        Publication.objects.create(text=needed,author=user)
        url = reverse('publications:home')
        response = self.client.get(url)
        content =response.content.decode('utf-8')
        self.assertIn(needed,content)
    
    # detail page
    def test_publication_detal_template_loads_publication(self):
        needed ='This is a publication'
        user = User.objects.create_user(username='master',password='123')
        Publication.objects.create(text=needed,author=user)
        url = reverse('publications:publication-detail',args=(1,))
        response = self.client.get(url)
        content =response.content.decode('utf-8')
        self.assertIn(needed,content)
