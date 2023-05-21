from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.test.client import Client
from folder_market.sensitive_ignore import First_ignore, Second_ignore

class SeleniumMixin:
    def setUp(self):
        options = Options()
        options.binary_location = First_ignore
        self.selenium = webdriver.Firefox(executable_path=Second_ignore, options=options)
       
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

class Change_infoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'johnpassworD1234')
        
    def test_for_change_info(self):
        response = self.client.get("/auth_market/change_info/")
        self.assertEqual(response.status_code, 302)  
        response = self.client.post("/auth_market/change_info/", {
            "password": 'johnpassworD1234',
            "new_password1": "johnpassworD1235",
            "new_password2":  "johnpassworD1235" 
        })
        self.assertEqual(response.status_code, 302)

class Change_usernameTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'johnpassworD1234')
        
    def test_for_change_username(self):
        response = self.client.get("/auth_market/change_username/")
        self.assertEqual(response.status_code, 302)  
        response = self.client.post("/auth_market/change_username/", {
            "username": 'Igor'
        })
        self.assertEqual(response.status_code, 302)
