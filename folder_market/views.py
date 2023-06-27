from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, FormView
from .models_for import (Item_info, Salesman_info, 
                         RatingStorage, BasketScope, Category)
from .forms import (addItem, SearchData, CreateSalesmans, OnlyForSubmit, OnlyForDelete, 
                    CreateCategory, AddCard, ChangeItem)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from thefuzz import fuzz
from django.contrib import messages
from .system_rating import recommendation_func
from .system_statistics import display_statistics
from collections import deque
from .basket_for import add_item, remove_item, remove_card, remove_item_info
from .filter_system import if_word_real, make_suggestion
from .check_category import check_caregory, google_search_link
from django.db.models import Sum


class RedirectIndex(View):
    def get(self, request):
        return redirect("/folder_market/1")

class Index(ListView):
    model = RatingStorage
    template_name = "folder_market/index.html"
    paginate_by = 5
    context_object_name = "display_page"
    
    def get_queryset(self):
        ratings_storage = super().get_queryset()
        ratings_storage = ratings_storage.filter(unique_user = self.request.user.username).select_related("id_connector")
        display_page = deque()
        for rating_storage in ratings_storage:
            if rating_storage.rating_storage > recommendation_func(self.request.user.username):
               display_page.appendleft([rating_storage.id_connector])
            else:
                display_page.append([rating_storage.id_connector])
        return list(display_page)  
    
class DashboardItems(FormView):
    form_class = addItem
    template_name = "folder_market/dashboard_items.html"
    context_object_name = "form"
    
    def form_valid(self, form):
        username_for = self.request.user.username
        form = addItem(self.request.POST, self.request.FILES)
        for_reuse = Salesman_info.objects.filter(validator_user=username_for)
        if form.is_valid():
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
                            messages.error(self.request, "Error1")
            else:
                try:
                    form.save()
                    return redirect("/folder_market/")
                except:
                    messages.error(self.request, "Error2")
            return redirect("/folder_market/")

@method_decorator(login_required, name='dispatch')    
class UpdateItem(FormView):
    template_name = "folder_market/update_item.html"
    form_class = ChangeItem
    form1_class = OnlyForDelete
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        context["form1"] = self.form1_class()
        return context
    
    def post(self, request, *args, **kwargs):
        check_item = self.kwargs["check_item"]
        username_for = self.request.user.username
        change_item = Item_info.objects.get(name=check_item)
        form = ChangeItem(self.request.POST, self.request.FILES, instance=change_item)
        form1 = OnlyForDelete(self.request.POST)
        if self.request.method == "POST":
            if "form-update" in self.request.POST:
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
                        messages.error(self.request, "Error")
                else:
                    return HttpResponse("You haven't access to page")
            if "form-delete" in self.request.POST:
                if change_item.salesman == username_for:
                    if form1.is_valid():
                        remove_item_info(check_item)
                        return redirect("/folder_market/")
                    else:
                        messages.error(self.request, "Error1")
                else:
                    return HttpResponse("You haven't access to page")

                
@method_decorator(login_required, name='dispatch')   
class DashboardSalesmans(ListView):
    model = Salesman_info
    template_name = "folder_market/dashboard_salesmans.html"
    context_object_name = "data_items"
        
    def get_queryset(self):
        try:
            data_items = super().get_queryset()
            data_items = data_items.get(validator_user=self.request.user.username)
            return data_items
        except Salesman_info.DoesNotExist:
            data_items = None

@method_decorator(login_required, name='dispatch')   
class StartTrade(FormView):
    template_name = "folder_market/start_trade.html"
    form_class = CreateSalesmans
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username_for = self.request.user.username
        check = Salesman_info.objects.filter(validator_user=username_for).exists()
        context["username_for"] = username_for
        context["check"] = check
        context["display_statistics"] = display_statistics(self.request)
        return context
    
    def form_valid(self, form):
        username_for = self.request.user.username
        check = Salesman_info.objects.filter(validator_user=username_for).exists()
        if check:
            messages.error(self.request, "Error1")
        else:
            salesman = form.save(commit=False)
            salesman.validator_user = username_for
            salesman.save()
            return redirect("/folder_market/dashboard_salesmans/")

class SearchItem(FormView):
    template_name = "folder_market/search.html"
    form_class = SearchData
    def post(self, request, *args, **kwargs):
        form = SearchData(self.request.POST)
        context = {"form": form}
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


class FindYourOrder(FormView):
    template_name = "folder_market/find_your_order.html"
    form_class = CreateSalesmans
    form1_class = OnlyForSubmit
    form2_class = OnlyForDelete
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        context["form1"] = self.form1_class()
        context["form2"] = self.form2_class()
        id_product = self.kwargs["id_product"]
        context["item_id"] = Item_info.objects.get(item_id = id_product)
        return context
    
    def post(self, request, *args, **kwargs):
        id_product = self.kwargs["id_product"]
        item_id = Item_info.objects.get(item_id = id_product)
        try:
            salesman_info = Salesman_info.objects.get(validator_user=item_id.salesman)
        except Salesman_info.DoesNotExist:
            salesman_info = None
        form = CreateSalesmans(request.POST, instance=salesman_info)
        form1 = OnlyForSubmit(request.POST)
        form2 = OnlyForDelete(request.POST)
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
                    messages.error(request, "Only one evaluation per user")
            elif "form-submit1" in request.POST:
                if form1.is_valid():
                    add_item(request, id_product)
                    return redirect(f"/folder_market/find_your_order/{id_product}")
            elif "form-submit2" in request.POST:
                if form2.is_valid():
                    remove_item()
                    return redirect(f"/folder_market/find_your_order/{id_product}")
            return redirect(f"/folder_market/find_your_order/{id_product}")
        
class DisplayBasket(ListView):
    model = BasketScope
    context_object_name = "list_for_basket"
    template_name =  "folder_market/display_basket.html"
    def get_queryset(self):
        basket_check = super().get_queryset()
        list_for_basket = []
        basket_check = basket_check.filter(check_salesman=self.request.user.username).select_related("added_item")
        for loop in basket_check:
            list_for_basket.append([[loop.added_item]])
        return list_for_basket
    
def remove_from_list(request, item_id):
    basket_for_delete = BasketScope.objects.filter(added_item__item_id = item_id).select_related("added_item")
    if basket_for_delete.exists() == False:
        return HttpResponse("Error", status=404)
    basket_for_delete.first().delete()
    return HttpResponse("Success", status=200)

@method_decorator(staff_member_required, name='dispatch')   
class ADD_Category(FormView):
    template_name = "folder_market/add_category.html"   
    form_class = CreateCategory
    def post(self, request, *args, **kwargs):
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
  
@method_decorator(cache_page(60 * 15), name='dispatch')  
class DisplayCategory(ListView):
    model = Category
    template_name = "folder_market/display_category.html"
    context_object_name = "get_category"
    def get_queryset(self):
        get_category = super().get_queryset()
        get_category = get_category.all()
        return get_category
        
class DisplayUnknownCategory(ListView):
    model = Item_info
    template_name = "folder_market/display_unknown_category.html"
    context_object_name = "item_category"
    def get_queryset(self):
        item_category = super().get_queryset()
        item_category = item_category.filter(category=None)
        return item_category    

class DisplayCurrentCategory(ListView):
    model = Item_info
    template_name = "folder_market/display_current_category.html"
    context_object_name = "item_category"
    def get_queryset(self):
        cat_name = self.kwargs["cat_name"]
        item_category = super().get_queryset()
        item_category = item_category.filter(category=cat_name)
        return item_category   

class PaymentAction(ListView):
    template_name = "folder_market/payment_action.html"
    model = BasketScope
    def get_queryset(self):
        your_items = super().get_queryset()
        your_items = your_items.filter(check_salesman=self.request.user.username).select_related("added_item")
        return your_items
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        your_items = self.get_queryset()
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
        context.update( {
            "count_items": count_items,
            "price_data": price_data,
            "price_check": sum(value for value in price_dict.values()),
            "your_items": your_items,
            "salesman_card": salesman_card_list,
            "price_dict": price_dict
        })
        return context

@method_decorator(login_required, name='dispatch')   
class WalletPage(FormView):
    template_name = "folder_market/wallet_page.html"
    form_class = AddCard
    form1_class = OnlyForDelete
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        context["form1"] = self.form1_class()
        try:
            for_reuse = Salesman_info.objects.get(validator_user=self.request.user.username)
            context["for_reuse"] = for_reuse
            context["check_exist"] = for_reuse.card_number
        except Salesman_info.DoesNotExist:
            return redirect("/folder_market/handler500/")
        return context


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for_reuse = context.get("for_reuse")
        username_for = self.request.user.username
        form = AddCard(self.request.POST, instance=for_reuse)
        form1 = OnlyForDelete(self.request.POST)
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
        return redirect("/folder_market/")
    

def handler404(request, exception):
    return render(request, "folder_market/404.html", status=404)

def handler500(request,  *args, **argv):
    return render(request, "folder_market/500.html", status=500)
    
    

