from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from publications.models import Publication, Comment

User = get_user_model()

class DeleteCommentTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.publication = Publication.objects.create(text='Test pub', author=self.user1)
        self.comment = Comment.objects.create(text='Test comment', author=self.user2, publication=self.publication)
        self.delete_url = reverse('publications:delete-comment', kwargs={'pk': self.comment.pk})
        self.detail_url = reverse('publications:publication-detail', kwargs={'pk': self.publication.pk})

    def test_delete_comment_method_not_post(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 405)

    def test_delete_comment_by_author(self):
        self.client.login(username='user2', password='pass2')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.detail_url)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_by_publication_author(self):
        self.client.login(username='user1', password='pass1')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.detail_url)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_unauthorized(self):
        User.objects.create_user(username='user3', password='pass3')
        self.client.login(username='user3', password='pass3')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_comment_nonexistent(self):
        self.client.login(username='user1', password='pass1')
        nonexistent_url = reverse('publications:delete-comment', kwargs={'pk': 999})
        response = self.client.post(nonexistent_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_comment_unauthenticated(self):
        self.client.logout()
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        login_url = reverse('authors:login')
        self.assertRedirects(response, f'{login_url}?next={self.delete_url}')
