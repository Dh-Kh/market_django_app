from django.urls import path
from . import views
app_name = "auth_market"
urlpatterns = [
    path("login/", views.login_user, name="login_user"),
    path("log_out/", views.log_out, name = "log_out"),
    path('register/', views.register, name='register'),
    path("change_info/", views.change_info, name = "change_info"),
    path("change_username/", views.change_username, name = "change_username"),
    ]