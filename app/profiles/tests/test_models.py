from django.test import TestCase
from django.contrib.auth import get_user_model
from profiles.models import Profile
from django.urls import reverse

User = get_user_model()

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        Profile.objects.filter(user=self.user1).update(bio='Bio user1')
        self.profile1 = Profile.objects.get(user=self.user1)
        Profile.objects.filter(user=self.user2).update(bio='Bio user2')
        self.profile2 = Profile.objects.get(user=self.user2)

    def test_profile_creation(self):
        self.assertEqual(self.profile1.user, self.user1)
        self.assertEqual(self.profile1.bio, 'Bio user1')

    def test_profile_str(self):
        self.assertEqual(str(self.profile1), f'{self.user1} profile')

    def test_profile_get_absolute_url(self):
        expected_url = reverse("profiles:profile", kwargs={"username": self.user1.username})
        self.assertEqual(self.profile1.get_absolute_url(), expected_url)

    def test_following(self):
        self.profile1.follow.add(self.profile2)
        self.assertIn(self.profile2, self.profile1.follow.all())
        self.assertIn(self.profile1, self.profile2.followers.all())
        self.assertNotIn(self.profile1, self.profile1.follow.all())

    def test_unfollow(self):
        self.profile1.follow.add(self.profile2)
        self.profile1.follow.remove(self.profile2)
        self.assertNotIn(self.profile2, self.profile1.follow.all())