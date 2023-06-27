from django.test import LiveServerTestCase, TestCase, Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from market import settings
from folder_market.models_for import Item_info


class SeleniumMixin:
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()

    def tearDown(self):
        self.selenium.quit()
    
class RedirectIndexTest(SeleniumMixin, LiveServerTestCase):    
    def test_for_redirect_index(self):
        self.selenium.get(f"{self.live_server_url}/folder_market/")
        
class IndexTest(SeleniumMixin, LiveServerTestCase):
    def test_for_index(self):
        self.selenium.get(f"{self.live_server_url}/folder_market/2")

class DashboardItemsTest(SeleniumMixin, LiveServerTestCase):
    def test_for_dashboard_items(self):
        self.selenium.get(self.live_server_url + "/folder_market/dashboard_items/")
        form_name = self.selenium.find_element(By.ID, "id_name")
        form_name.send_keys("Iphone")
        form_price = self.selenium.find_element(By.ID, "id_price")
        form_price.send_keys(1000)
        form_product_desc = self.selenium.find_element(By.ID, "id_product_description")
        form_product_desc.send_keys("Smartphone for smart peoples")
        form_cat = self.selenium.find_element(By.ID, "id_category")
        form_cat.send_keys("---------")
        submit_button = self.selenium.find_element(By.ID, "input_submit")
        submit_button.click()
        
class UpdateItemTest(SeleniumMixin, LiveServerTestCase):
    def setUp(self):
         super().setUp()
         user = User.objects.create_user(username="John", password="YokoandJohn")
         self.client.force_login(user)  
         session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
         self.selenium.get(self.live_server_url + "/auth_market/login/")
         self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 
                                'value': session_key, 'path': '/'})
    def test_for_update_item(self):
        self.selenium.get(self.live_server_url + "/folder_market/update_item/Computer/")
        form_price = self.selenium.find_element(By.ID, "id_price")
        form_price.send_keys(1000)
        form_product_desc = self.selenium.find_element(By.ID, "id_product_description")
        form_product_desc.send_keys("Smartphone for smart peoples")
        submit_button = self.selenium.find_element(By.ID, "input_submit")
        submit_button.click()

    def test_for_delete_item(self):
        self.selenium.get(self.live_server_url + "/folder_market/update_item/Computer/")
        delete_button = self.selenium.find_element(By.ID, "delete_button")
        delete_button.click()

class DashboardSalesmansTestAuth(SeleniumMixin, LiveServerTestCase):
    def setUp(self):
         super().setUp()
         user = User.objects.create_user(username="John", password="YokoandJohn")
         self.client.force_login(user)  
         session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
         self.selenium.get(self.live_server_url + "/auth_market/login/")
         self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 
                                'value': session_key, 'path': '/'})
    def test_for_dashboard_salesmans_first(self):
        self.selenium.get(self.live_server_url + "/folder_market/dashboard_salesmans/")
        first_link = self.selenium.find_element(By.XPATH, "//a[@title='first_click']")
        first_link.click()
        
    def test_for_dashboard_salesmans_second(self):
        self.selenium.get(self.live_server_url + "/folder_market/dashboard_salesmans/")
        second_link = self.selenium.find_element(By.XPATH, "//a[@title='second_link']")
        second_link.click()
        
    def test_for_dashboard_salesmans_three(self):
         self.selenium.get(self.live_server_url + "/folder_market/dashboard_salesmans/")
         third_link = self.selenium.find_element(By.XPATH, "//a[@title='third_link']")
         third_link.click()
        
    def test_for_dashboard_salesmans_button(self):
        self.selenium.get(self.live_server_url + "/folder_market/dashboard_salesmans/")
        go_back = self.selenium.find_element(By.ID, "go_back")
        go_back.click()
        
    
class DashboardSalesmansTest(SeleniumMixin, LiveServerTestCase):
    def  test_for_dashboard_salesmans_not_auth(self):
        self.selenium.get(self.live_server_url + "/folder_market/dashboard_salesmans/")
        
class StartTradeTest(SeleniumMixin, LiveServerTestCase):
    def setUp(self):
         super().setUp()
         user = User.objects.create_user(username="John", password="YokoandJohn")
         self.client.force_login(user)  
         session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
         self.selenium.get(self.live_server_url + "/auth_market/login/")
         self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 
                                'value': session_key, 'path': '/'})
         
    def test_for_start_trade(self):
        self.selenium.get(self.live_server_url + "/folder_market/start_trade/")
        
class SearchItemTest(SeleniumMixin, LiveServerTestCase):
    def test_for_search_item(self):
        self.selenium.get(self.live_server_url + "/folder_market/search/")
        text_input = self.selenium.find_element(By.ID, "text_input")
        text_input.send_keys("Computer")
        button_submit = self.selenium.find_element(By.ID, "button_submit")
        button_submit.click()
        
class FindYourOrderTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.record = Item_info.objects.create(
            item_id=1, name="Product", price=2000, 
            imagine_file = r"C:\Users\Admin\Pictures\Screenshots\download.jpeg",
            category = None, salesman ="Igor")
                                             
    def test_for_find_your_order_first(self):
        response = self.client.get("/folder_market/find_your_order/1/")
        self.assertEqual(response.status_code, 200)
        form_data = {
            'form-submit1': 'Submit', 
            "form-submit2": "Submit",
        }
        response = self.client.post("/folder_market/find_your_order/1/", data=form_data)
        self.assertEqual(response.status_code, 302)
        
    
        
class DisplayBasketTest(SeleniumMixin, LiveServerTestCase):

    def test_for_display_basket_url(self):
        self.selenium.get(self.live_server_url + "/folder_market/display_basket/")
        first_url = self.selenium.find_element(By.XPATH, "//a[@title='first_url']")
        first_url.click()
        
    def test_for_display_basket_button(self):
        self.selenium.get(self.live_server_url + "/folder_market/display_basket/")
        button_submit = self.selenium.find_element(By.ID, "button_submit")
        button_submit.click()
        
class ADD_CategoryTest(SeleniumMixin, LiveServerTestCase):
    def setUp(self):
         super().setUp()
         self.user = User.objects.create_user(username="John", password="YokoandJohn")
         self.user.is_staff = True
         self.user.save()
         self.client.force_login(self.user)  
         session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
         self.selenium.get(self.live_server_url + "/auth_market/login/")
         self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 
                                'value': session_key, 'path': '/'})
         
    def test_for_add_category(self):
        self.selenium.get(self.live_server_url + "/folder_market/add_category/")
        form_category = self.selenium.find_element(By.ID, "category")
        form_category.send_keys("Phones")
        button_click = self.selenium.find_element(By.ID, "button-addon1")
        button_click.click()

class DisplayCategoryTest(SeleniumMixin, LiveServerTestCase):
    def setUp(self):
        super().setUp()
        user = User.objects.create_user(username="John", password="YokoandJohn")
        self.client.force_login(user)  
        session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        self.selenium.get(self.live_server_url + "/auth_market/login/")
        self.selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 
                               'value': session_key, 'path': '/'})
    
    def test_for_display_category(self):
        self.selenium.get(self.live_server_url + "/folder_market/display_category/")
        
class DisplayUnknownCategoryTest(SeleniumMixin, LiveServerTestCase):
    def test_for_display_unknown_category(self):
        self.selenium.get(self.live_server_url + "/folder_market/display_unknown_category/")
        
class DisplayCurrentCategoryTest(SeleniumMixin, LiveServerTestCase):
    def test_for_display_current_category(self):
        self.selenium.get(self.live_server_url + "/folder_market/display_current_category/")

class PaymentActionTest(SeleniumMixin, LiveServerTestCase):
    def test_for_payment_action(self):
        self.selenium.get(self.live_server_url + "/folder_market/payment_action/")
        
class WalletPageTest(TestCase):
     
    def test_for_wallet_page(self):
        response = self.client.get("/folder_market/wallet_page/")
        self.assertEqual(response.status_code, 302)
        form_data = {
            "form-add": "Submit",
            "form-delete": "Submit"
        }
        response = self.client.post("/folder_market/wallet_page/", data = form_data)
        self.assertEqual(response.status_code, 302)
