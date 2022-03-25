from tkinter import Scrollbar
from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Food, Review
from .forms import FoodForm, ReviewForm
from django.utils import timezone
from requests import get
from bs4 import BeautifulSoup

def get_foods():
    url = "https://docs.google.com/spreadsheets/d/1JpEUpUJ3slFP1y2PgJV1J_2_sBf5VOek4TUcq90P_Cs/pubhtml/sheet?headers=false&gid=0&range=A2:G43"

    response = get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    td_class = soup.find_all("td", {"class": "s12", "colspan":"4"})
    test = []
    i = 0

    for el in td_class:
        test.append(el.text.strip())

        if '' == test[i] or "A:" in test[i]:
            del test[i]
        else:
            i += 1

    td_class2 = soup.find_all("td", {"class": "s18"})
    for el in td_class2:
        test.append(el.text.strip())

        if '' == test[i] or "A:" in test[i]:
            del test[i]
        else:
            i += 1

    td_class3 = soup.find_all("td", {"class": "s15"})
    for el in td_class3:
        test.append(el.text.strip())

        if '' == test[i] or "A:" in test[i]:
            del test[i]
        else:
            i += 1
    
    return test

@staff_member_required
def get_foods_view(request):
    form = FoodForm(request.POST or None)

    if request.method == "POST":
        
        form = FoodForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            scrape_food = get_foods()
            j = 0
        
            for i in scrape_food:     
                food_instance = Food()
                food_instance.upload_date = timezone.now()
                food_instance.title = scrape_food[j]
                food_instance.description = description
                j += 1
                food_instance.save()

            
            return render(request, "food_post.html")

    return render(request, "add_foods.html", {"form":form})



def home_view(request, *args, **kwargs):
    food_list = Food.objects.order_by('-upload_date')[:9]

    return render(request, "home.html", {"food_list":food_list})

def food_list_view(request):
    
    food_list = Food.objects.order_by("title")
    context = { "food_list" : food_list }
    return render(request, "jidlo.html", context)

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