from django.urls import path
from . import views
app_name = "auth_market"
urlpatterns = [
    path("login/", views.login_user, name="login_user"),
    path("log_out/", views.log_out, name = "log_out"),
    path('register/', views.register, name='register'),
    path("change_info/", views.change_info, name = "change_info"),
    path("change_username/", views.change_username, name = "change_username"),
    path("change_email/", views.change_email, name = "change_email"),
    path("send_secret_key/", views.send_secret_key, name = "send_secret_key"),
    path("display_user_account/", views.display_user_account, name = "display_user_account")
    ]