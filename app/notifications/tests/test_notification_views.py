from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from publications.models import Publication
from notifications.models import Notification

User = get_user_model()


class NotificationListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', password='testpassword'
        )
        self.publication = Publication.objects.create(
            text='Test publication', author=self.other_user
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            sender=self.other_user,
            notification_type='like',
            text='Someone liked your post',
            publication=self.publication,
        )
        self.url = reverse('notifications:notifications-list')
        self.login_url = reverse('authors:login')

    def test_list_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')

    def test_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'notifications/pages/notifications.html')

    def test_list_view_shows_only_user_notifications(self):
        other_notification = Notification.objects.create(
            recipient=self.other_user,
            sender=self.user,
            notification_type='comment',
            text='Someone commented on your post',
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        notifications = response.context['notifications']
        self.assertIn(self.notification, notifications)
        self.assertNotIn(other_notification, notifications)

    def test_list_view_context_object_name(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('notifications', response.context)

    def test_list_view_pagination(self):
        for i in range(15):
            Notification.objects.create(
                recipient=self.user,
                sender=self.other_user,
                notification_type='like',
                text=f'Notification {i}',
            )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['notifications']), 10)

    def test_list_view_pagination_page_two(self):
        for i in range(15):
            Notification.objects.create(
                recipient=self.user,
                sender=self.other_user,
                notification_type='like',
                text=f'Notification {i}',
            )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url + '?page=2')
        self.assertEqual(response.status_code, 200)
        # 15 created + 1 from setUp = 16 total, page 2 should have 6
        self.assertEqual(len(response.context['notifications']), 6)


class MarkNotificationAsReadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            text='Test notification',
        )
        self.url = reverse(
            'notifications:mark-as-read', kwargs={'id': self.notification.id}
        )

    def test_mark_as_read_post_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_mark_as_read_get_returns_404(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_mark_as_read_nonexistent_notification(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('notifications:mark-as-read', kwargs={'id': 9999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_mark_as_read_already_read(self):
        self.notification.is_read = True
        self.notification.save()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)


class DeleteNotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            text='Test notification to delete',
        )
        self.url = reverse(
            'notifications:delete', kwargs={'id': self.notification.id}
        )

    def test_delete_notification_post_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Notification.objects.filter(id=self.notification.id).exists()
        )

    def test_delete_notification_get_returns_404(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_delete_notification_nonexistent(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('notifications:delete', kwargs={'id': 9999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
