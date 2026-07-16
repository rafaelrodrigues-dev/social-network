from django.test import TestCase
from django.contrib.auth import get_user_model
from publications.models import Publication
from django.urls import reverse

User = get_user_model()


class PublicationHome(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='master',password='123')
        self.user2 = User.objects.create_user(username='user2',password='passworduser2')

    def test_publications_home_loads_publications(self):
        needed ='This is a publication'
        Publication.objects.create(text=needed,author=self.user)
        response = self.client.get(reverse('publications:home'))
        content = response.content.decode('utf-8')
        self.assertIn(needed, content)

    def test_publications_following_loads_publications(self):
        needed = 'This is a pubication created by user2'
        Publication.objects.create(text=needed,author=self.user2)
        self.user.profile.follow.add(self.user2.profile)
        self.client.login(username='master', password='123')
        response = self.client.get(reverse('publications:following'))
        content = response.content.decode('utf-8')
        self.assertIn(needed, content)
    
    def test_publications_following_dont_loads_unfollowed_user_publications(self):
        needed = 'This is a pubication created by user2'
        Publication.objects.create(text=needed,author=self.user2)
        self.client.login(username='master', password='123')
        response = self.client.get(reverse('publications:following'))
        content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(needed, content)

    def test_publications_saved_loads_publications(self):
        needed = 'This is a pubication created by user2'
        publication = Publication.objects.create(text=needed,author=self.user2)
        self.user.saved.add(publication)
        self.client.login(username='master', password='123')
        response = self.client.get(reverse('publications:saved'))
        content = response.content.decode('utf-8')
        self.assertIn(needed, content)

    def test_publications_saved_dont_loads_publications_not_saved(self):
        needed = 'This is a pubication created by user2'
        Publication.objects.create(text=needed,author=self.user2)
        self.client.login(username='master', password='123')
        response = self.client.get(reverse('publications:saved'))
        content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(needed, content)