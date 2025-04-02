from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorsLogoutTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('authors:login')
        self.logout_url = reverse('authors:logout')

    def test_logout_redirects_to_home(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Perform logout
        response = self.client.get(self.logout_url)
        
        # Check if the user is redirected to the home page
        self.assertRedirects(response, reverse('publications:home'))

    def test_logout_clears_session(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Perform logout
        self.client.get(self.logout_url)
        
        # Check if the user is logged out
        response = self.client.get(reverse('authors:profile'))  # Assuming 'profile' requires login
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_logout_without_login(self):
        # Attempt to logout without being logged in
        response = self.client.get(self.logout_url)
        
        # Check if the user is redirected to the home page
        self.assertRedirects(response, reverse('authors:login') + '?next=/a/logout/')