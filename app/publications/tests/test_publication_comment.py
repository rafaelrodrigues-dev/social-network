from django.test import TestCase
from publications.models import Publication
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class CommentTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1',password='passworduser1')
        self.user2 = User.objects.create_user(username='user2',password='passworduser2')
        self.publication = Publication.objects.create(text='This is a post',author=self.user1)
        self.client.login(username='user2',password='passworduser2')
        
    def test_comment_http_method_is_not_post(self):
        response = self.client.get(reverse('publications:comment',kwargs={'pk':self.publication.pk}))
        self.assertEqual(response.status_code,404)
    
    def test_comment_publication(self):
        data = {
            'text':'This is a test comment',
            'author':self.user2
        }
        response = self.client.post(
            reverse('publications:comment',kwargs={'pk':self.publication.pk}),
            data=data,
            follow=True
        )
        self.assertIn(data.get('text'),response.content.decode('utf-8'))
