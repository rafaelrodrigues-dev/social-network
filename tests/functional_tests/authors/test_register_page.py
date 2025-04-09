from .base import AuthorsTestBase
from selenium.webdriver.common.by import By
from django.utils.translation import gettext_lazy as _

class AuthorsRegisterTest(AuthorsTestBase):
    def setUp(self):
        super().setUp()
        self.driver.get(self.live_server_url + '/a/register/')

    def test_authors_register_if_user_can_sing_in(self):
        # Fill out the form
        self.fill_field('//*[@id="id_username"]','testuser')
        self.fill_field('//*[@id="id_first_name"]','Test')
        self.fill_field('//*[@id="id_email"]','test@email.com')
        self.fill_field('//*[@id="id_password"]','testpassword')

        # Submit the form
        self.driver.find_element(By.XPATH,'/html/body/main/section/form/button',).click()
        # Check if the user was registered and logged in successfully
        self.assertIn(
            str(_('User registered successfully')),
            self.driver.find_element(By.TAG_NAME,'body').text
        )

    def test_link_to_login(self):
        self.driver.find_element(By.XPATH,'/html/body/main/section/p/a').click()
        self.assertIn(
            'Login',
            self.driver.find_element(By.TAG_NAME,'body').text
        )