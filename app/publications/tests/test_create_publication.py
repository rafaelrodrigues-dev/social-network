from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from publications.models import Publication
import tempfile
import shutil

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CreatePublicationTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('authors:login')
        self.home_url = reverse('publications:home')
        self.create_url = reverse('publications:create-publication')

    def test_create_publication_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {'text': 'Test content for publication'}

        response = self.client.post(self.create_url, post_data)

        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

        # Check database
        self.assertEqual(Publication.objects.count(), 1)
        publication = Publication.objects.first()
        self.assertEqual(publication.text, 'Test content for publication')
        self.assertEqual(publication.author, self.user)
        self.assertFalse(publication.img)  # no image uploaded

    def test_create_publication_with_image(self):
        self.client.login(username='testuser', password='testpassword')

        # Create a small valid GIF image
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9'
            b'\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00'
            b'\x00\x02\x02\x4c\x01\x00\x3b'
        )
        uploaded_file = SimpleUploadedFile(
            'test_image.gif',
            small_gif,
            content_type='image/gif'
        )

        post_data = {
            'text': 'Publication with image',
            'img': uploaded_file
        }

        response = self.client.post(self.create_url, post_data)

        # Check redirect
        self.assertEqual(response.status_code, 302)

        # Check database
        self.assertEqual(Publication.objects.count(), 1)
        publication = Publication.objects.first()
        self.assertEqual(publication.text, 'Publication with image')
        self.assertEqual(publication.author, self.user)
        self.assertTrue(publication.img)
        self.assertTrue(publication.img.name.endswith('test_image.gif'))

    def test_create_publication_unauthenticated(self):
        post_data = {'text': 'Unauthenticated publication'}

        response = self.client.post(self.create_url, post_data)

        # Check redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.create_url}')

        # Check database (no publication should be created)
        self.assertEqual(Publication.objects.count(), 0)

    def test_create_publication_invalid_method(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.create_url)

        self.assertEqual(response.status_code, 405)  # Method Not Allowed
        self.assertEqual(Publication.objects.count(), 0)
