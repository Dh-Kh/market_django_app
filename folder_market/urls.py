from django.urls import path
from . import views

app_name = "folder_market"
urlpatterns = [
    path("", views.RedirectIndex.as_view() , name="redirect_index"),
    path("<int:page>", views.Index.as_view(), name="index"),
    path("dashboard_items/", views.DashboardItems.as_view(), name="dashboard_items"),
    path("update_item/<str:check_item>/", views.UpdateItem.as_view(), name = "update_item"),
    path("dashboard_salesmans/", views.DashboardSalesmans.as_view(), name="dashboard_salesmans"),
    path("start_trade/", views.StartTrade.as_view(), name = "start_trade"),
    path("search/", views.SearchItem.as_view(), name= "search_item"),
    path("find_your_order/<int:id_product>/", views.FindYourOrder.as_view(), name = "find_your_order"),
    path("display_basket/", views.DisplayBasket.as_view(), name = "display_basket"),
    path("add_category/", views.ADD_Category.as_view(), name = "add_category"),
    path("display_category/",  views.DisplayCategory.as_view(), name = "display_category"),
    path("display_unknown_category/", views.DisplayUnknownCategory.as_view(), name = "display_unknown_category"),
    path("display_current_category/<str:cat_name>/", views.DisplayCurrentCategory.as_view(), name = "display_current_category"),
    path("payment_action/", views.PaymentAction.as_view(), name = "payment_action"),
    path('remove_from_list/<int:item_id>/', views.remove_from_list, name='remove_from_list'),
    path("wallet_page/", views.WalletPage.as_view(), name="wallet_page"), 
    ]
