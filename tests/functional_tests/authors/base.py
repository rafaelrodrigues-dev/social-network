from django.test import LiveServerTestCase
from utils.driver import get_driver
from selenium.webdriver.common.by import By


class AuthorsTestBase(LiveServerTestCase):
    def setUp(self):
        self.driver = get_driver()

    def tearDown(self):
        self.driver.quit()

    def fill_field(self,xpath, value):
        self.driver.find_element(By.XPATH, xpath).send_keys(value)