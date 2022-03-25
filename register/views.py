from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def register_view(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            return render(response, "register_post.html")

        
    else:
        form = UserCreationForm()
    
    return render(response, "register.html", {"form":form})