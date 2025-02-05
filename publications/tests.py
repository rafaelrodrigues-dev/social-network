from django.test import TestCase
from django.contrib.auth.models import User
from publications.models import Publication
from django.urls import reverse

class PublicationHomePageTest(TestCase):
    def test_publication_home_template_loads_publicarions(self):

        needed ='This is a publication'
        user = User.objects.create_user(username='master',password='123')
        Publication.objects.create(text=needed,author=user)
        url = reverse('publications:home')
        response = self.client.get(url)
        content =response.content.decode('utf-8')
        self.assertIn(needed,content)

