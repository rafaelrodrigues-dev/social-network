from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from publications.models import Publication
from notifications.models import Notification

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
        # Response shows is_following = true
        self.assertIn('{"is_following": true}',response.content.decode('utf-8'))

    def test_unfollow_user(self):
        # Create a seconde user to follow
        user2 = User.objects.create_user(username='testuser2', password='password')
        # Follow the second user
        url = reverse('profiles:follow', kwargs={'username':user2.username})
        self.client.post(url,follow=True)
        # Unffolow the second user
        response =self.client.post(url,follow=True)
        # Response shows is_following = false
        self.assertIn('{"is_following": false}',response.content.decode('utf-8'))

    def test_follow_if_method_is_not_post(self):
        url = reverse('profiles:follow', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_follow_user_cannot_follow_themself(self):
        url = reverse('profiles:follow', kwargs={'username': self.user.username})
        response = self.client.post(url)
        self.assertContains(response, 'You cannot follow yourself', status_code=403)

    def test_profile_detail_not_found(self):
        url = reverse('profiles:profile', kwargs={'username': 'nonexistentuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_profile_detail_posts_tab(self):
        # Create some publications
        pub1 = Publication.objects.create(text='Publication 1', author=self.user)
        user2 = User.objects.create_user(username='testuser2', password='password')
        pub2 = Publication.objects.create(text='Publication 2', author=user2)

        url = reverse('profiles:profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['active_tab'], 'posts')
        self.assertIn(pub1, response.context['page_obj'])
        self.assertNotIn(pub2, response.context['page_obj'])

    def test_profile_detail_saved_tab(self):
        pub1 = Publication.objects.create(text='Publication 1', author=self.user)
        user2 = User.objects.create_user(username='testuser2', password='password')
        pub2 = Publication.objects.create(text='Publication 2', author=user2)
        # self.user saves pub2
        pub2.saved.add(self.user)

        url = reverse('profiles:profile', kwargs={'username': self.user.username})
        response = self.client.get(url + '?tab=saved')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['active_tab'], 'saved')
        self.assertIn(pub2, response.context['page_obj'])
        self.assertNotIn(pub1, response.context['page_obj'])

    def test_profile_detail_pagination(self):
        # Create 8 publications for the user
        for i in range(8):
            Publication.objects.create(text=f'Publication {i}', author=self.user)

        url = reverse('profiles:profile', kwargs={'username': self.user.username})
        
        # First page should contain 6 publications
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 6)

        # Second page should contain 2 publications
        response = self.client.get(url + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 2)

    def test_follow_creates_notification(self):
        user2 = User.objects.create_user(username='testuser2', password='password')
        url = reverse('profiles:follow', kwargs={'username': user2.username})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify that a notification is created
        self.assertTrue(
            Notification.objects.filter(
                recipient=user2,
                sender=self.user,
                notification_type='follow'
            ).exists()
        )
