from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_if_profile_detail_shows_correct_profile(self):
        url = reverse('profiles:profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_follow_user(self):
        # Create a seconde user to follow
        user2 = User.objects.create_user(username='testuser2', password='password')
        # Follow the second user
        url = reverse('profiles:follow', kwargs={'username':user2.username})
        response = self.client.post(url,follow=True)
        # Response shows a 'Unfollow' button
        self.assertIn('unfollow',response.content.decode('utf-8'))

    def test_unfollow_user(self):
        # Create a seconde user to follow
        user2 = User.objects.create_user(username='testuser2', password='password')
        # Follow the second user
        url = reverse('profiles:follow', kwargs={'username':user2.username})
        self.client.post(url,follow=True)
        # Unffolow the second user
        response =self.client.post(url,follow=True)
        # Response shows a 'Follow' button
        self.assertIn('follow',response.content.decode('utf-8'))

    def test_follow_if_method_is_not_post(self):
        url = reverse('profiles:follow', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_follow_user_cannot_follow_themself(self):
        url = reverse('profiles:follow', kwargs={'username': self.user.username})
        response = self.client.post(url)
        self.assertContains(response, 'You cannot follow yourself', status_code=403)