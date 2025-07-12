from django.test import TestCase
from django.urls import reverse
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationsViewTest(TestCase):
    def setUp(self):
        self.url = reverse('notifications')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.notification = Notification.objects.create(
            sender=None,
            recipient=self.user,
            title='System',
            message='This is a test notification.'
        )

    def test_notifications_view_show_notifications(self):
        response = self.client.get(self.url)

        self.assertIn('This is a test notification.', response.content.decode('utf-8'))
    
    def test_notifications_view_mark_as_read(self):
        # Ensure the notification is unread before the request
        self.assertFalse(Notification.objects.filter(recipient=self.user, is_read=True).exists())
        # Access the notifications view
        response = self.client.get(self.url)
        # Check that the response is successful
        self.assertTrue(Notification.objects.filter(recipient=self.user, is_read=True).exists())

    def test_notifications_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('authors:login') + '?next=' + self.url)