from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from market import settings

class SeleniumMixin:
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()

    def tearDown(self):
        self.selenium.quit()
    
class LoginTest(SeleniumMixin, LiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('john', 'johnpassworD1234')
        
    def test_for_login_test(self):        
        self.selenium.get(self.live_server_url + "/auth_market/login/")
        form_username = self.selenium.find_element(By.ID, 'id_username')
        form_username.send_keys('john')
        form_password = self.selenium.find_element(By.ID, 'id_password')
        form_password.send_keys('johnpassworD1234')
        login_button = self.selenium.find_element(By.TAG_NAME, 'button')
        login_button.click()

class RegisterTest(SeleniumMixin, LiveServerTestCase):
    def test_for_register_test(self):
        self.selenium.get(self.live_server_url + "/auth_market/register/")
        form_username = self.selenium.find_element(By.ID, 'id_username')
        form_username.send_keys('john')
        form_password1 = self.selenium.find_element(By.ID, 'id_password1')
        form_password1.send_keys('johnpassworD1234')
        form_password2 = self.selenium.find_element(By.ID, 'id_password2')
        form_password2.send_keys('johnpassworD1234')
        login_button = self.selenium.find_element(By.TAG_NAME, 'button')
        login_button.click()

class Change_InfoTest(SeleniumMixin, LiveServerTestCase):
   def setUp(self):
       super().setUp()
       user = User.objects.create_user(username="John", password="YokoandJohn")
       self.client.force_login(user)  
       session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
       self.selenium.get(self.live_server_url + "/auth_market/login/")
       self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 
                              'value': session_key, 'path': '/'})
       
   def test_for_change_info(self):
       pass

class Change_UsernameTest(SeleniumMixin, LiveServerTestCase):
    def setUp(self):
        super().setUp()
        user = User.objects.create_user(username="John", password="YokoandJohn")
        self.client.force_login(user)  
        session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        self.selenium.get(self.live_server_url + "/auth_market/login/")
        self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 
                               'value': session_key, 'path': '/'})
        
    def test_for_change_username(self):
        self.selenium.get(self.live_server_url + "/auth_market/change_username/")
        form_username = self.selenium.find_element(By.ID, 'id_username')
        form_username.send_keys('john')
        submit_button = self.selenium.find_element(By.TAG_NAME, 'button')
        submit_button.click()
        
class Change_EmailTest(SeleniumMixin, LiveServerTestCase):
    def setUp(self):
        super().setUp()
        user = User.objects.create_user(username="John", password="YokoandJohn")
        self.client.force_login(user)  
        session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        self.selenium.get(self.live_server_url + "/auth_market/login/")
        self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 
                               'value': session_key, 'path': '/'})
        
    def test_for_change_email(self):
        self.selenium.get(self.live_server_url + "/auth_market/change_email/")
        form_email = self.selenium.find_element(By.ID, 'id_email')
        form_email.send_keys('johnlennon@gmail.com')
        submit_button = self.selenium.find_element(By.TAG_NAME, 'button')
        submit_button.click()

class Display_user_accountTest(SeleniumMixin, LiveServerTestCase):
    def setUp(self):
        super().setUp()
        user = User.objects.create_user(username="John", password="YokoandJohn")
        self.client.force_login(user)  
        session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        self.selenium.get(self.live_server_url + "/auth_market/login/")
        self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 
                               'value': session_key, 'path': '/'})
        
    def test_for_display_user_account(self):
        self.selenium.get(self.live_server_url + "/auth_market/display_user_account/")

