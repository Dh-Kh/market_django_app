from django.urls import path
from . import views

app_name = "folder_market"
urlpatterns = [
    path("", views.redirect_index, name = "redirect_index"),
    path("<int:page>", views.index, name="index"),
    path("dashboard_items/", views.dashboard_items, name="dashboard_items"),
    path("dashboard_salesmans/", views.dashboard_salesmans, name="dashboard_salesmans"),
    path("search/", views.search_item, name= "search_item"),
    path("find_your_order/<int:id_product>/", views.find_your_order, name = "find_your_order"),
    path("start_trade/", views.start_trade, name = "start_trade"),
    path("display_basket/", views.display_basket, name = "display_basket"),
    path("add_category/", views.add_category, name = "add_category"),
    path("display_category/",  views.display_category, name = "display_category"),
    path("display_unknown_category/", views.display_unknown_category, name = "display_unknown_category"),
    path("display_current_category/<str:cat_name>/", views.display_current_category, name = "display_current_category"),
    path("payment_action/", views.payment_action, name = "payment_action"),
    path('remove_from_list/<int:item_id>/', views.remove_from_list, name='remove_from_list'),
    path("wallet_page/", views.wallet_page, name="wallet_page"), 
    path("update_item/<str:check_item>/", views.update_item, name = "update_item"),
    ]
