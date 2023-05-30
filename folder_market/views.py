from django.shortcuts import render, redirect
from .models_for import Item_info, Salesman_info, RatingStorage, BasketScope, Category
from .forms import addItem, SearchData, CreateSalesmans, OnlyForSubmit, OnlyForDelete, ForCommentsOnly, CreateCategory, AddCard, ChangeItem
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from thefuzz import fuzz
from django.http import HttpResponseNotFound
from django.contrib import messages
from .system_rating import recommendation_func
from .system_statistics import display_statistics
from collections import deque
from django.core.paginator import Paginator
from .basket_for import add_item, remove_item, remove_card, remove_item_info
from .filter_system import if_word_real, make_suggestion
from .check_category import check_caregory, google_search_link
from django.db.models import Sum

def redirect_index(request):
    return redirect("/folder_market/1")

def index(request, page):
    ratings_storage = RatingStorage.objects.filter(unique_user = request.user.username).select_related("id_connector")
    desired_data = deque()
    for rating_storage in ratings_storage:
        if rating_storage.rating_storage > recommendation_func(request.user.username):
            desired_data.appendleft([rating_storage.id_connector])
        else:
            desired_data.append([rating_storage.id_connector])
    if len(list(desired_data)) != 0:    
        paginator = Paginator(list(desired_data), per_page=5)
        display_page = paginator.get_page(page)
        context = {"display_page": display_page}
        return render(request, "folder_market/index.html", context)
    return render(request, "folder_market/index.html")

@login_required
def dashboard_items(request):
    username_for = request.user.username
    form = addItem(request.POST, request.FILES)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            for_reuse = Salesman_info.objects.filter(validator_user=username_for)
            if for_reuse.exists():
                mapping_data = form.cleaned_data["name"]
                for salesman_info in Salesman_info.objects.all():
                    if salesman_info.validator_user == username_for:
                        try:
                            data_use = form.save(commit=False)
                            data_use.salesman = username_for
                            if check_caregory(mapping_data) == True:    
                                data_use.save()
                            else:
                                data_use.category = None
                                data_use.save()
                            return redirect("/folder_market/")
                        except:
                            messages.error(request, "Error1")
            else:
                try:
                    form.save()
                    return redirect("/folder_market/")
                except:
                    messages.error(request, "Error2")
        else:
            messages.error(request, "Error")
    return render(request, "folder_market/dashboard_items.html", context)
    
@login_required
def update_item(request, check_item):
    username_for = request.user.username
    change_item = Item_info.objects.get(name=check_item)
    form = ChangeItem(request.POST, request.FILES, instance=change_item)
    form1 = OnlyForDelete(request.POST)
    context = {"form": form}
    if request.method == "POST":
        if "form-update" in request.POST:
            if change_item.salesman == username_for:
                if form.is_valid():
                    mapping_data1 = form.cleaned_data["price"]
                    mapping_data2 = form.cleaned_data["product_description"]
                    mapping_data3 = form.cleaned_data["imagine_file"]
                    try:
                        change_form = form.save(commit=False)
                        change_form.price = mapping_data1
                        change_form.product_description = mapping_data2
                        change_form.imagine_file = mapping_data3
                        change_form.save()
                        return redirect("/folder_market/")
                    except Exception as e:
                        return e
                
                else:
                    messages.error(request, "Error")
            else:
                return HttpResponse("You haven't access to page")
        if "form-delete" in request.POST:
            if change_item.salesman == username_for:
                if form1.is_valid():
                    remove_item_info(check_item)
                    return redirect("/folder_market/")
                else:
                    messages.error(request, "Error1")
            else:
                return HttpResponse("You haven't access to page")
    return render(request, "folder_market/update_item.html", context)
                
@login_required
def dashboard_salesmans(request):
    try:
        data_items = Salesman_info.objects.get(validator_user=request.user.username)
    except Salesman_info.DoesNotExist:
        data_items = None
        
    context = {"data_items": data_items}
    return render(request, "folder_market/dashboard_salesmans.html", context)

@login_required
def start_trade(request):
    username_for = request.user.username
    form = CreateSalesmans(request.POST)
    check = Salesman_info.objects.filter(validator_user=username_for).exists()
    context = {"form": form, "username_for": username_for, 
               "check": check, "display_statistics": display_statistics(request)}
    if request.method == "POST":
        if form.is_valid(): 
            try:
                if check:
                    messages.error(request, "Error1")
                else:
                    salesman = form.save(commit=False)
                    salesman.validator_user = username_for
                    salesman.save()
                    return redirect("/folder_market/dashboard_salesmans/")
            except:
                return redirect("/folder_market/start_trade")
        else:
            messages.error(request, "Error")
    return render(request, "folder_market/start_trade.html", context)
            
def search_item(request):
    form = SearchData(request.POST)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            desired_input = form.cleaned_data["desired_item"]
            container_ability = Item_info.objects.all().values("item_id", "name", "price")
            desired_ratio = 55
            desired_list = []
            for item in container_ability:
                ratio = fuzz.ratio(desired_input, item["name"])
                if desired_ratio <= ratio:
                    desired_list.append(item)
            
            if desired_list == []:
                messages.error(request, google_search_link(desired_input))
            else:
                context = {"form": form, "desired_list": desired_list}
                return render(request, "folder_market/search.html", context)
            
    return render(request, "folder_market/search.html", context)

def find_your_order(request, id_product):
    try:
        item_id = Item_info.objects.get(item_id = id_product)
    except Item_info.DoesNotExist:
        return HttpResponseNotFound("Sorry, this url is not found")
    try:
        salesman_info = Salesman_info.objects.get(validator_user=item_id.salesman)
    except Salesman_info.DoesNotExist:
        salesman_info = None
    form = CreateSalesmans(request.POST, instance=salesman_info)
    form1 = OnlyForSubmit(request.POST)
    form2 = OnlyForDelete(request.POST)
    form_com = ForCommentsOnly(request.POST)
    context = {"item_id": item_id, "form": form, "form_com": form_com}
    if request.method == "POST":
        if "form-submit" in request.POST:
            if form.is_valid(): 
                mapping_data = form.cleaned_data["rating"]
                if request.user.is_authenticated:
                    if RatingStorage.objects.filter(id_connector=item_id, unique_user=request.user.username).exists():
                        messages.error(request, "You could evaluate page only once")
                    else:
                        if salesman_info != None:
                            RatingStorage.objects.create(rating_storage = salesman_info.rating, salesman_connector = salesman_info, 
                                                 id_connector = item_id, unique_user=request.user.username)
                        else:
                            RatingStorage.objects.create(rating_storage = mapping_data, salesman_connector=None, 
                                                 id_connector = item_id, unique_user=request.user.username)
                    
                        return redirect("/folder_market/")
            else:
                messages.error(request, "Only auth user can evaluate posts")
        elif "form-submit1" in request.POST:
            if form1.is_valid():
                add_item(request, id_product)
                return redirect(f"/folder_market/find_your_order/{id_product}")
        elif "form-submit2" in request.POST:
            if form2.is_valid():
                remove_item()
                return redirect(f"/folder_market/find_your_order/{id_product}")
        if form_com.is_valid():
            if "form-submit-com" in request.POST:
                for_again = form_com.save(commit=False)
                for_again.comment_item = item_id.name
                for_again.comment_user = request.user.username
                for_again.save()
                messages.success(request, "Your comment is added")    
                return redirect(f"/folder_market/find_your_order/{id_product}")
        
    return render(request, "folder_market/find_your_order.html", context)


def display_basket(request):
    list_for_basket = []
    basket_check = BasketScope.objects.filter(check_salesman=request.user.username).select_related("added_item")
    for loop in basket_check:
        list_for_basket.append([[loop.added_item]])
    
    context = {"list_for_basket": list_for_basket}
    return render(request, "folder_market/display_basket.html" , context)

def remove_from_list(request, item_id):
    basket_for_delete = BasketScope.objects.filter(added_item__item_id = item_id).select_related("added_item")
    if basket_for_delete.exists() == False:
        return HttpResponse("Error", status=404)
    basket_for_delete.first().delete()
    return HttpResponse("Success", status=200)
        
@staff_member_required
def add_category(request):
    form = CreateCategory(request.POST)
    if form.is_valid():
        mapping_data = form.cleaned_data["category"]
        if if_word_real(mapping_data):    
            form.save()
            messages.success(request, "Success")
            return redirect("/folder_market/add_category/")
        else:
            messages.error(request, make_suggestion(mapping_data))
    context = {"form": form}
    return render(request, "folder_market/add_category.html", context)

@cache_page(60 * 15)
def display_category(request):
    get_category = Category.objects.all()
    context = {"get_category": get_category}
    return render(request, "folder_market/display_category.html", context)

def display_unknown_category(request):
    item_category = Item_info.objects.filter(category=None)
    context = {"item_category": item_category}
    return render(request, "folder_market/display_unknown_category.html", context)


def display_current_category(request, cat_name):
    item_category = Item_info.objects.filter(category=cat_name)
    context = {"item_category": item_category}
    return render(request, "folder_market/display_current_category.html", context)

def payment_action(request):
    your_items = BasketScope.objects.filter(check_salesman=request.user.username).select_related("added_item")
    salesman_card = Salesman_info.objects.all()
    count_items = your_items.count()
    price_data = your_items.aggregate(total_price = Sum("added_item__price"))["total_price"]
    salesman_card_list = []
    price_dict = {}
    for salesman_data in salesman_card:
        for desire_items in your_items:
            if salesman_data.validator_user == desire_items.added_item.salesman:
                if salesman_data.validator_user in price_dict:
                    price_dict[salesman_data.validator_user] += desire_items.added_item.price
                else:
                    price_dict[salesman_data.validator_user] = desire_items.added_item.price
                
                salesman_card_list.append(salesman_data.card_number)
    context = {
        "count_items": count_items,
        "price_data": price_data,
        "your_items": your_items,
        "salesman_card": salesman_card_list,
        "price_dict": price_dict
    }
    if your_items.exists() == False:
        messages.error(request, "No data to display")
    return render(request, "folder_market/payment_action.html", context)

@login_required
def wallet_page(request):
    username_for = request.user.username
    for_reuse = Salesman_info.objects.get(validator_user=username_for)
    form = AddCard(request.POST, instance=for_reuse)
    form1 = OnlyForDelete(request.POST)
    check_exist = for_reuse.card_number
    context = {"form": form, "check_exist": check_exist}
    if request.method == "POST":
        if "form-add" in request.POST:
            if form.is_valid():
                mapping_data = form.cleaned_data["card_number"]
                for salesman_info in Salesman_info.objects.all():
                    if salesman_info.validator_user == username_for:
                        try:
                            for_save = form.save(commit=False)
                            for_save.card_number = mapping_data
                            for_save.save()
                            return redirect("/folder_market/")
                        except Exception as e:
                            return e
            else:
                messages.error(request, "error")
        if "form-delete" in request.POST:
            if form1.is_valid():
                remove_card(request)
                return redirect("/folder_market/")
            else:
                messages.error(request, "error1")
    return render(request, "folder_market/wallet_page.html", context)
    
def pageNotFound(request, exception):
    return HttpResponseNotFound("Sorry, this url is not found")

