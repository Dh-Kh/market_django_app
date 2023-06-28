from django.test import TestCase
from auth_market.forms import (
    RegisterForm, FormChange, ChangeUsername, Change_Email
    )
from django.contrib.auth.models import User



class Test_RegisterForm(TestCase):
    def test_for_register_form(self):
        form = RegisterForm(data = {
            "username": "John",
            "password1": "NewPassword123!",
            "password2": "NewPassword123!",
            "captcha_0": "8e10ebf60c5f23fd6e6a9959853730cd69062a15",
            "captcha_1": "PASSED"
            })
        print(form.errors)
        self.assertTrue(form.is_valid())
class Test_FormChange(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = "John", password = "OldPassword4422*")
        
    def test_for_form_change(self):
        form = FormChange(user=self.user , data = {
            "old_password": 'OldPassword4422*',
            "new_password1": "NewPassword123!",
            "new_password2": "NewPassword123!"
            })
        self.assertTrue(form.is_valid())
class Test_ChangeUsername(TestCase):
    def test_for_change_username(self):
        form = ChangeUsername(data = {
            "username": "Igor"
            })
        self.assertTrue(form.is_valid())
        
class Test_ChangeEmail(TestCase):
    def test_for_change_email(self):
        form = Change_Email(data={"email": "flask_django@gmail.com"})
        self.assertTrue(form.is_valid())

