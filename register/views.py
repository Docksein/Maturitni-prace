from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def register_view(response):
    form = UserCreationForm()
    return render(response, "login.html", {"form":form})