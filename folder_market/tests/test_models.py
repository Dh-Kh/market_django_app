from django.test import TestCase
from folder_market.models_for import Salesman_info, Category, Item_info, RatingStorage, BasketScope, UserComments

class SalesmanTest(TestCase):
    
    def test_create_salesman_info(self):
        Salesman_info.objects.create(username="hello@gmail.com", 
             rating=5, validator_user="admin", card_number=100999)
        
        
        
class CategoryTest(TestCase):
    def test_for_category(self):
        Category.objects.create(category="something")

class Item_info_test(TestCase):
    def test_for_item_info(self):
        Item_info.objects.create(name="Product",
                                 price = 2000,
                                 )
        Item_info.objects.create(name="ProductX",
                                price=-1000,
                                imagine_file = r"C:\Users\Admin\Pictures\Screenshots\download.jpeg"
                                )
        
class RatingStorage_test(TestCase):
    
    def setUp(self):
        Salesman_info.objects.create(username="hello@gmail.com", 
                                     rating=5, validator_user="admin", card_number=100999)
        Item_info.objects.create(name="ProductX",
                                price=-1000,
                                imagine_file = r"C:\Users\Admin\Pictures\Screenshots\download.jpeg"
                                )
    def test_for_rating_storage(self):
        RatingStorage.objects.create(
            rating_storage=1,
            salesman_connector = Salesman_info.objects.get(validator_user="admin"),
            id_connector = Item_info.objects.get(item_id=1),
            unique_user = "Igor"
            )

class BasketScope_test(TestCase):
    def setUp(self):
        Item_info.objects.create(name="ProductX",
                                price=-1000,
                                imagine_file = r"C:\Users\Admin\Pictures\Screenshots\download.jpeg"
                                )
    def test_for_basket_scope(self):
        BasketScope.objects.create(
            added_item = Item_info.objects.get(item_id=1),
            check_salesman = "Igor"
            )

class UserComments_test(TestCase):
    def test_for_user_comments(self):
        UserComments.objects.create(
            comment_item = "hello",
            comment_body = "lalala",
            comment_user = "Igor"
        )
    
