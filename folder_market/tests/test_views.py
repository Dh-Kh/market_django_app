from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from django.contrib.auth.models import User
from django.test.client import Client
from folder_market.models_for import Item_info, BasketScope, Category
from folder_market.sensitive_ignore import First_ignore, Second_ignore

class SeleniumMixin:
    def setUp(self):
        options = Options()
        options.binary_location = First_ignore
        self.selenium = webdriver.Firefox(executable_path=Second_ignore, options=options)
       
    def tearDown(self):
        self.selenium.quit()
        
    
class RedirectIndexTest(SeleniumMixin, LiveServerTestCase):    
    def test_for_redirect_index(self):
        self.selenium.get(f"{self.live_server_url}/folder_market/")
        
class IndexTest(SeleniumMixin, LiveServerTestCase):
    def test_for_index(self):
        self.selenium.get(f"{self.live_server_url}/folder_market/2")

class Dashboard_itemsTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'johnpassworD1234')
        
    def test_for_dashboard_items(self):        
        response = self.client.get("/folder_market/dashboard_items/")
        self.assertEqual(response.status_code, 302)  
        response = self.client.post('/auth_market/login/', {'username': 'john', 'password': 'johnpassworD1234'})
        self.assertEqual(response.status_code, 200)  
        response = self.client.get("/folder_market/dashboard_items/")
        self.assertEqual(response.status_code, 302) 
        form_data = {
            'name': 'LG X',
            'price': 1000,
            'product_description': 'New phone',
            'category': 'Phones',
            'imagine_file': r'C:\Users\Admin\Pictures\Screenshots\download.jpeg',
        }
        response = self.client.post('/folder_market/dashboard_items/', data=form_data)
        self.assertEqual(response.status_code, 302)

class Update_itemTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'johnpassworD1234')
        self.client.login(username='john', password='johnpassworD1234')
        self.item = Item_info.objects.create(name="Product",
                                 price = 2000,
                                 product_description = None,
                                 imagine_file = None,
                    )
        
    def test_for_update_item(self):
        response = self.client.get("/folder_market/update_item/Product/")
        self.assertEqual(response.status_code, 302)  
        form_data = {
            'price': 1000,
            'product_description': 'New phone',
            'imagine_file': r'C:\Users\Admin\Pictures\Screenshots\download.jpeg',
        }
        response = self.client.post('/folder_market/update_item/Product/', data=form_data)
        self.assertEqual(response.status_code, 302)
        
class Dashboard_salesmansTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'johnpassworD1234')
        self.client.login(username='john', password='johnpassworD1234')
        
    def test_for_dashboard_salesmans(self):
        response = self.client.get("/folder_market/dashboard_salesmans/")
        self.assertEqual(response.status_code, 302)
        
class Start_tradeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'johnpassworD1234')
        self.client.login(username='john', password='johnpassworD1234')
    def test_for_start_trade(self):
        response = self.client.get("/folder_market/start_trade/")
        self.assertEqual(response.status_code, 302)
        
class Search_itemTest(TestCase):
    def test_for_search_item(self):
        response = self.client.get("/folder_market/search/")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/folder_market/search/")
        self.assertEqual(response.status_code, 200)

class Find_your_orderTest(TestCase):
    def setUp(self):
        self.item = Item_info.objects.create(item_id=10, name="Product", price=2000, 
                                             imagine_file = r"C:\Users\Admin\Pictures\Screenshots\download.jpeg",
                                             category = None, 
                                             salesman ="Igor"
                                             )

    def test_for_find_your_order(self):
        response = self.client.get("/folder_market/find_your_order/10/")
        self.assertEqual(response.status_code, 200)
        form_data = {
            'form-submit1': 'Submit', 
            "form-submit2": "Submit",
            "form-submit-com": "Submit"
        }
        response = self.client.post("/folder_market/find_your_order/10/", data=form_data)
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get("/folder_market/find_your_order/10/")
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get("/folder_market/find_your_order/444/")
        self.assertEqual(response.status_code, 404)

class Display_basket_test(TestCase):
    def setUp(self):
        self.item = Item_info.objects.create(item_id=1, name="Product", price=2000, 
                                             imagine_file = r"C:\Users\Admin\Pictures\Screenshots\download.jpeg",
                                             category = None, 
                                             salesman ="Igor"
                                             )
        self.basket = BasketScope.objects.create(added_item = Item_info.objects.get(item_id = 1),
            check_salesman ="Igor")
    def test_for_display_basket(self):
        response = self.client.get("/folder_market/display_basket/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/folder_market/remove_from_list/1/")
        self.assertEqual(response.status_code, 200)

class Add_category_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(is_superuser= True, username='john', password='johnpassworD1234')
        self.client.login(username='john', password='johnpassworD1234')
      
    def test_for_add_category(self):
        form_data = {
            "category": "Computers"
        }
        response = self.client.get("/folder_market/add_category/")
        self.assertEqual(response.status_code, 302)
        response = self.client.post("/folder_market/add_category/", data=form_data)
        self.assertEqual(response.status_code, 302)

class Display_category_test(TestCase):
    def test_for_display_category(self):
        response = self.client.get("/folder_market/display_category/")
        self.assertEqual(response.status_code, 200)
        
class Display_types_category_test(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category="Computers")
    def test_for_display_types_category(self):
        response = self.client.get("/folder_market/display_current_category/Computers/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/folder_market/display_unknown_category/")
        self.assertEqual(response.status_code, 200)
        
class Payment_action_test(TestCase):
    def test_for_payment_action(self):
        response = self.client.get("/folder_market/payment_action/")
        self.assertEqual(response.status_code, 200)

class Wallet_page_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username='john', password='johnpassworD1234')
        self.client.login(username='john', password='johnpassworD1234')
        
    def test_for_wallet_page(self):
        response = self.client.get("/folder_market/wallet_page/")
        self.assertEqual(response.status_code, 302)
        form_data = {
            "form-add": "Submit",
            "form-delete": "Submit"
        }
        response = self.client.post("/folder_market/wallet_page/", data = form_data)
        self.assertEqual(response.status_code, 302)