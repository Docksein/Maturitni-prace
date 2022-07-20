from tkinter import Scrollbar
from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Food, Review, Tag
from .forms import ReviewForm
from django.utils import timezone
from requests import get
import pandas



def home_view(request, *args, **kwargs):
    food_list = Food.objects.order_by('-upload_date')[:9]

    return render(request, "home.html", {"food_list":food_list})

def food_list_view(request):
    
    food_list = Food.objects.order_by("title")
    context = { "food_list" : food_list }
    return render(request, "jidlo.html", context)

def tag_list_view(request, pk):

    tag = get_object_or_404(Tag, pk=pk)
    food_list = Food.objects.filter(tags=tag.id).order_by('-upload_date')

    return render(request, "tag.html", {"tag":tag, "food_list":food_list})

def review_view(request, food_id):

    food = get_object_or_404(Food, pk=food_id)
    form = ReviewForm(request.POST or None)
    review_list = Review.objects.filter(food_key = food).order_by('-published_date')

    if request.method == "POST":
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            ratings = form.cleaned_data['ratings']
            comment = form.cleaned_data['comment']
            review = Review(author_name = request.user)
            review.ratings = ratings
            review.comment = comment
            review.food_key = food
            review.published_date = timezone.now()
            review.save()
            form = ReviewForm()
            return render(request, "review_post.html")
            
        else:
            form = ReviewForm()
    
    return render(request, "reviews.html", { "form": form, "food":food, "review_list":review_list })

def user_review_view(request):
    username = request.user
    review_list = Review.objects.filter(author_name=username).order_by('-published_date')
    return render(request, "user_reviews.html", {"review_list":review_list})