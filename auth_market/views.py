from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import (RegisterForm, FormChange, ChangeUsername, 
                    Change_Email)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from folder_market.models_for import Salesman_info, Item_info, RatingStorage
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from folder_market.sensitive_ignore import Email_one_ignore
from django.http import HttpResponse
import pyotp
import urllib.parse

totp = pyotp.TOTP("base32secret3232", interval=300)


def register(request):
    form = RegisterForm(request.POST)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next', reverse("folder_market:redirect_index")))
        else:
            messages.error(request, form.errors)
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
    
    if request.user.email == "":
        return redirect("/auth_market/change_email/")
    
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            mapping_data = form.cleaned_data["verification_field"]
            if totp.verify(mapping_data):
                form.save()
                update_session_auth_hash(request, form.user)
                send_email(request, "You have changed your password")
                return redirect(request.GET.get('next', reverse("folder_market:redirect_index")))
            else:
                messages.error(request, "Failed verification")
        else:
            messages.error(request, form.errors)
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
            send_email(request, "You have changed your username")
            return redirect(request.GET.get('next', reverse("folder_market:redirect_index")))
        else:
            messages.error(request, "Error")
    return render(request, "auth_market/change_username.html", context)

def change_email(request):
    form = Change_Email(request.POST, instance=request.user)
    context = {"form": form, "email_check": request.user.email}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next', reverse("folder_market:redirect_index")))
        else:
            messages.error(request, "Error")
    return render(request, "auth_market/change_email.html", context)

@login_required
def display_user_account(request):
    context = {
        "data1": request.user.username,
        "data2": request.user.email, 
        "data3": request.user.date_joined
        }
    return render(request, "auth_market/display_user_account.html", context)

def send_email(request, body):
    send_mail(
        'Notification',
        str(body),
        Email_one_ignore,
        [request.user.email],
        fail_silently=False,
    )
    
def send_secret_key(request):
    email = urllib.parse.unquote(request.GET.get('email', ''))
    send_mail("Submit action", totp.now(), Email_one_ignore, [email], fail_silently=False,)
    return HttpResponse("Sending", 200)

def log_out(request):
    logout(request)
    return redirect("/auth_market/login")


                
        