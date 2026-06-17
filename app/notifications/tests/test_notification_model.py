from django.test import TestCase
from django.contrib.auth import get_user_model
from publications.models import Publication
from notifications.models import Notification

User = get_user_model()


class NotificationModelTest(TestCase):
    def setUp(self):
        self.recipient = User.objects.create_user(
            username='recipient', password='testpassword'
        )
        self.sender = User.objects.create_user(
            username='sender', password='testpassword'
        )
        self.publication = Publication.objects.create(
            text='Test publication', author=self.sender
        )
        self.notification = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type='like',
            text='Sender liked your publication',
            publication=self.publication,
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.recipient, self.recipient)
        self.assertEqual(self.notification.sender, self.sender)
        self.assertEqual(self.notification.notification_type, 'like')
        self.assertEqual(self.notification.text, 'Sender liked your publication')
        self.assertEqual(self.notification.publication, self.publication)

    def test_notification_is_read_default_false(self):
        self.assertFalse(self.notification.is_read)

    def test_notification_created_at_auto(self):
        self.assertIsNotNone(self.notification.created_at)

    def test_notification_str(self):
        expected = (
            f"Notification {self.notification.id} "
            f"from {self.sender} to {self.recipient}"
        )
        self.assertEqual(str(self.notification), expected)

    def test_notification_without_sender(self):
        notification = Notification.objects.create(
            recipient=self.recipient,
            notification_type='system',
            text='System notification',
        )
        self.assertIsNone(notification.sender)

    def test_notification_without_publication(self):
        notification = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type='follow',
            text='Sender started following you',
        )
        self.assertIsNone(notification.publication)

    def test_notification_recipient_related_name(self):
        notifications = self.recipient.notifications.all()
        self.assertIn(self.notification, notifications)

    def test_notification_sender_related_name(self):
        notifications = self.sender.sender.all()
        self.assertIn(self.notification, notifications)

    def test_notification_publication_related_name(self):
        notifications = self.publication.notifications.all()
        self.assertIn(self.notification, notifications)

    def test_cascade_delete_recipient(self):
        notification_id = self.notification.id
        self.recipient.delete()
        self.assertFalse(Notification.objects.filter(id=notification_id).exists())

    def test_cascade_delete_sender(self):
        notification_id = self.notification.id
        self.sender.delete()
        self.assertFalse(Notification.objects.filter(id=notification_id).exists())

    def test_cascade_delete_publication(self):
        notification_id = self.notification.id
        self.publication.delete()
        self.assertFalse(Notification.objects.filter(id=notification_id).exists())
