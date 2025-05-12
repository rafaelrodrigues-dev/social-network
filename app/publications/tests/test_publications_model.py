from django.test import TestCase
from django.contrib.auth import get_user_model
from publications.models import Publication
from publications.models import Comment

User = get_user_model()


class PublicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password='testpassword')
        self.publication = Publication.objects.create(
            text='This is a publication',
            author=self.user
        )

    def test_publication_creation(self):
        self.assertCountEqual(self.publication.text,'This is a publication')

    def test_like_publication(self):
        self.publication.like.add(self.user)
        self.assertEqual(self.publication.like.count(), 1)
        self.assertIn(self.user, self.publication.like.all())

    def test_unlike_publication(self):
        self.publication.like.add(self.user)
        self.publication.like.remove(self.user)
        self.assertEqual(self.publication.like.count(), 0)
        self.assertNotIn(self.user, self.publication.like.all())

    def test_publication_str_class(self):
        self.assertEqual(self.publication.__str__(),f'{self.publication.author.username} publication id:{self.publication.id}')

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='commentuser', password='testpassword')
        self.publication = Publication.objects.create(
            text='Publication for comment',
            author=self.user
        )
        self.comment = Comment.objects.create(
            text='This is a comment',
            author=self.user,
            publication=self.publication
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, 'This is a comment')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.publication, self.publication)

    def test_like_comment(self):
        self.comment.like.add(self.user)
        self.assertEqual(self.comment.like.count(), 1)
        self.assertIn(self.user, self.comment.like.all())

    def test_unlike_comment(self):
        self.comment.like.add(self.user)
        self.comment.like.remove(self.user)
        self.assertEqual(self.comment.like.count(), 0)
        self.assertNotIn(self.user, self.comment.like.all())

    def test_comment_str_class(self):
        self.assertEqual(
            self.comment.__str__(),
            f'comment from publication id:{self.publication.id}'
        )