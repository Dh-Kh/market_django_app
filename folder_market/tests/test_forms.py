from django.test import TestCase
from folder_market.forms import (addItem, ChangeItem, SearchData, CreateSalesmans, 
                                 OnlyForSubmit, OnlyForDelete, ForCommentsOnly, CreateCategory, AddCard)

class Test_addItem(TestCase):
    def test_for_addedItem(self):
        addItem(data = {
            "name": "Computer",
            "price": 1000,
            "imagine_file": None,
            "product_description": None,
            "category": None
            })
        addItem(data = {
            "name": "Computer",
            "price": 1000,
            "imagine_file": r"C:\Users\Admin\Pictures\Screenshots\download.jpeg",
            "product_description": "Something",
            "category": "Something"
            })
        
class ChangeItem_test(TestCase):
    def test_for_ChangeItem_test(self):
        ChangeItem(
            data = {
                "name": "Hello",
                "price": 1000,
                "imagine_file": r"C:\Users\Admin\Pictures\Screenshots\download.jpeg",
                "product_description": "Something",
                "category": "Something"
                }
            )
class SearchData_test(TestCase):
    def test_for_SearchData(self):
        SearchData(
            data = {
                "desired_item": "something"
                }
            )
class CreateSalesmans_test(TestCase):
    def test_for_CreateSalesmans(self):
        CreateSalesmans(
            data = {
                "username": None,
                "rating": None,
                }
            )
        CreateSalesmans(
            data = {
                "username": "a@gmail.com",
                "rating": 5,
                }
            )
class OnlyForSubmit_test(TestCase):
    def test_for_OnlyForSubmit(self):
        OnlyForSubmit(
            data = {
                "submit": " "
                }
            )
class OnlyForDelete_test(TestCase):
    def test_for_OnlyForDelete(self):
        OnlyForDelete(
            data = {
                "submit": " "
                }
            )
class ForCommentsOnly_test(TestCase):
    def test_for_ForCommentsOnly(self):
        ForCommentsOnly(
            data = {
                "comment_body", "hello"
                }
            )
        
class CreateCategory_test(TestCase):
    def test_for_CreateCategory(self):
        CreateCategory(
            data = {
                "category": "games"
                }
            )
class AddCard_test(TestCase):
    def test_for_AddCard(self):
        AddCard(
            data = {
                "card_number": 999999
                }
            )