from .base import AuthorsTestBase
from selenium.webdriver.common.by import By
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class AuthorsLoginTest(AuthorsTestBase):
    def setUp(self):
        super().setUp()
        self.driver.get(self.live_server_url + '/a/login/')
    
    def test_if_user_can_login(self):
        # Needed
        username = 'testuser'
        password = '12345678'

        # Create user in database
        User.objects.create_user(username=username,password=password)

        # Fill out the form
        self.fill_field('//*[@id="id_username"]',username)
        self.fill_field('//*[@id="id_password"]',password)

        # Submit the form
        self.driver.find_element(By.XPATH,'/html/body/main/section/form/button',).click()

        # Check if the user was logged in successfully
        self.assertIn(
            str(_('Login successful')),
            self.driver.find_element(By.TAG_NAME,'body').text
        )
