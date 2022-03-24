from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Food, Review
from .forms import ReviewForm

def food_list_view(request):
    food_list = Food.objects.order_by("title")
    context = { "food_list" : food_list }
    return render(request, "jidlo.html", context)

def review_view(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    form = ReviewForm(request.POST or None)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            form = ReviewForm()
        else:
            form = ReviewForm()
    
    return render(request, "reviews.html", { "form": form })