from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Salesman_info(models.Model):
    username = models.EmailField(unique=True)
    rating = models.FloatField(default=0.0, validators=[
        MaxValueValidator(5), MinValueValidator(0)
        ])
    validator_user = models.CharField(max_length=100, null=True)
    card_number = models.IntegerField(validators=[MaxValueValidator(999999), 
                                      MinValueValidator(100000)], unique=True, null=True)


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.category
    
class Item_info(models.Model):
    item_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    data_creation = models.DateTimeField(auto_now_add=True)
    imagine_file = models.FileField(upload_to="images/", null=True, blank=True, verbose_name="")
    product_description = models.CharField(max_length=700, null = True, blank=True)
    salesman = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    

class RatingStorage(models.Model):
    rating_storage = models.FloatField(default=0.0, validators=[
        MaxValueValidator(5), MinValueValidator(0)
        ])
    salesman_connector = models.ForeignKey(Salesman_info, on_delete=models.CASCADE, null = True, blank=True)
    id_connector = models.ForeignKey(Item_info, on_delete=models.CASCADE)
    unique_user = models.CharField(max_length=100, null=True)
    
class BasketScope(models.Model):
    added_item = models.ForeignKey(Item_info, on_delete=models.CASCADE)
    check_salesman = models.CharField(max_length=100, null=True)
    
    

    


    