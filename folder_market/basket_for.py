from .models_for import BasketScope, Item_info, Salesman_info

def add_item(request, id_product):
    item_for_add = Item_info.objects.get(item_id= id_product)
    if item_for_add.salesman not in BasketScope.objects.values("check_salesman"):
        BasketScope.objects.create(added_item = item_for_add, check_salesman = request.user.username)
    else:
        return "You can't add your item to basket"
    
def remove_item():
    basket_for_delete = BasketScope.objects.last()
    try:
        basket_for_delete.delete()
    except:
        pass
    
def remove_card(request):
    remove_checker = Salesman_info.objects.get(validator_user=request.user.username)
    remove_checker.card_number = None
    remove_checker.save()

def remove_item_info(id_item):
    item_for_delete = Item_info.objects.get(name=id_item)
    item_for_delete.delete()