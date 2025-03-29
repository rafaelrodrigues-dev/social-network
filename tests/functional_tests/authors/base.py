from django.test import LiveServerTestCase
from utils.driver import get_driver

class AuthorsTestBase(LiveServerTestCase):
    def setUp(self):
        self.driver = get_driver()

    def tearDown(self):
        self.driver.quit()