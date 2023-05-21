from django.contrib import admin
from .models_for import Item_info, Salesman_info, RatingStorage, BasketScope, UserComments, Category

admin.site.register(Item_info)
admin.site.register(Salesman_info)
admin.site.register(RatingStorage)
admin.site.register(BasketScope)
admin.site.register(UserComments)
admin.site.register(Category)