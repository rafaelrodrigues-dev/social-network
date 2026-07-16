from django.test import TestCase
from django.urls import reverse

class InfoPagesTest(TestCase):
    def test_about_view_loads_correct_template(self):
        response = self.client.get(reverse('authors:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authors/pages/about.html')
        
    def test_privacy_policy_view_loads_correct_template(self):
        response = self.client.get(reverse('authors:privacy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authors/pages/privacy.html')