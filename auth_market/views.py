from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, FormChange, ChangeUsername
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from folder_market.models_for import Salesman_info, Item_info, RatingStorage
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from folder_market.sensitive_ignore import Email_one_ignore, Email_two_ignore


def register(request):
    form = RegisterForm(request.POST)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next', reverse("folder_market:redirect_index")))
        else:
            messages.error(request, "Error")
    return render(request, "auth_market/register.html", context)

def login_user(request):
    form = AuthenticationForm(data = request.POST)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', reverse("folder_market:redirect_index")))
        else:
            messages.error(request, "Error")
    return render(request, "auth_market/login.html", context)

@login_required
def change_info(request):
    form = FormChange(request.user, request.POST)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            send_email("You have changed your password")
            return redirect(request.GET.get('next', reverse("folder_market:redirect_index")))
        else:
            messages.error(request, "Error")
    return render(request, "auth_market/change_info.html", context)

@login_required
def change_username(request):
    form = ChangeUsername(request.POST, instance=request.user)
    old_username = request.user.username
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            mapping_data = form.cleaned_data["username"]
            for salesman_info in Salesman_info.objects.filter(validator_user= old_username):    
                salesman_info.validator_user = mapping_data
                salesman_info.save()
            for item_info in Item_info.objects.filter(salesman= old_username):
                item_info.salesman = mapping_data
                item_info.save()
            for rating_info in RatingStorage.objects.filter(unique_user= old_username):
                rating_info.unique_user = mapping_data
                rating_info.save()
            form.save()
            send_email("You have changed your username")
            return redirect(request.GET.get('next', reverse("folder_market:redirect_index")))
        else:
            messages.error(request, "Error")
    return render(request, "auth_market/change_username.html", context)

def send_email(body):
    send_mail(
        'Notification',
        str(body),
        Email_one_ignore,
        [Email_two_ignore],
        fail_silently=False,
    )

def log_out(request):
    logout(request)
    return redirect("/auth_market/login")


                
        