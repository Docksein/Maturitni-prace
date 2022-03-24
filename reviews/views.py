from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Food, Review
from .forms import ReviewForm
from django.utils import timezone

def home_view(request, *args, **kwargs):
    food_list = Food.objects.order_by('-upload_date')[:9]

    return render(request, "home.html", {"food_list":food_list})

def food_list_view(request):
    
    food_list = Food.objects.order_by("title")
    context = { "food_list" : food_list }
    return render(request, "jidlo.html", context)

def review_list_view(request):
    pass

def review_view(request, food_id):

    food = get_object_or_404(Food, pk=food_id)
    form = ReviewForm(request.POST or None)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            ratings = form.cleaned_data['ratings']
            comment = form.cleaned_data['comment']
            author_name = form.cleaned_data['author_name']
            review = Review()
            review.ratings = ratings
            review.comment = comment
            review.author_name = author_name
            review.food = food
            review.published_date = timezone.now()
            review.save()
            
        else:
            form = ReviewForm()
    
    return render(request, "reviews.html", { "form": form, "food":food, })