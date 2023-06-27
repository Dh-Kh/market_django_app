from django import forms
from .models_for import Item_info, Salesman_info, Category
from captcha.fields import CaptchaField

class addItem(forms.ModelForm):
    imagine_file = forms.FileField(required=False)
    product_description = forms.CharField(required=False, widget= forms.Textarea())
    category = forms.ModelChoiceField(queryset= Category.objects.all(), to_field_name='category', required=False)
    class Meta:
        model = Item_info
        fields = ['name', 'price', 'imagine_file', 'product_description', 'category']

class ChangeItem(forms.ModelForm):
    imagine_file = forms.FileField(required=False)
    product_description = forms.CharField(required=False, widget= forms.Textarea())
    class Meta:
        model = Item_info
        fields = ["price", 'product_description', 'imagine_file']
        
class SearchData(forms.Form):
    desired_item = forms.CharField(required=False)
    
class CreateSalesmans(forms.ModelForm):
    username = forms.EmailField(required=False)
    rating = forms.FloatField(required=False)  
    class Meta:
        model = Salesman_info
        exclude = ["validator_user", "card_number"]

class OnlyForSubmit(forms.Form):
    submit = forms.CharField(required=False, widget=forms.HiddenInput())

class OnlyForDelete(forms.Form):
    delete = forms.CharField(required=False, widget=forms.HiddenInput())
    
    
class CreateCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        
class AddCard(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Salesman_info
        fields = ["card_number"]