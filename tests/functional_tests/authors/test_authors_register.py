from .base import AuthorsTestBase
from selenium.webdriver.common.by import By

class AuthorsRegisterTest(AuthorsTestBase):
    def fill_field(self,xpath, value):
        self.driver.find_element(By.XPATH, xpath).send_keys(value)

    def setUp(self):
        super().setUp()
        self.driver.get(self.live_server_url + '/a/register/')

    def test_authors_register_if_user_can_sing_in(self):
        # Get form
        form = self.driver.find_element(By.XPATH,'/html/body/main/section/form')
        # Fill out the form
        self.fill_field('//*[@id="id_username"]','testuser')
        self.fill_field('//*[@id="id_first_name"]','Test')
        self.fill_field('//*[@id="id_email"]','test@email.com')
        self.fill_field('//*[@id="id_password"]','testpassword')

        # Submit the form
        form.submit()
        # Check if the user was registered and logged in successfully
        session_cookie = self.driver.get_cookie('sessionid')
        self.assertIsNotNone(session_cookie)