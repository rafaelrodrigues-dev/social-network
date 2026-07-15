from django.test import TestCase
from django.contrib.auth import get_user_model
from publications.models import Publication
from django.urls import reverse

User = get_user_model()


from publications.models import Comment

class PublicationDetailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='master', password='123')

    def test_publication_detail_template_loads_publication(self):
        needed = 'This is a publication'
        publication = Publication.objects.create(text=needed, author=self.user)
        url = reverse('publications:publication-detail', args=(publication.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publications/pages/publication-detail.html')
        content = response.content.decode('utf-8')
        self.assertIn(needed, content)

    def test_publication_detail_nonexistent(self):
        url = reverse('publications:publication-detail', args=(999,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_publication_detail_comments_pagination(self):
        publication = Publication.objects.create(text='Detail post', author=self.user)
        # Create 6 comments (comments pagination is 5)
        for i in range(6):
            Comment.objects.create(publication=publication, text=f'Comment {i}', author=self.user)

        url = reverse('publications:publication-detail', args=(publication.id,))
        
        # Check first page comments count is 5
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['comments']), 5)

        # Check second page comments count is 1
        response = self.client.get(url + '?comments_page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['comments']), 1)