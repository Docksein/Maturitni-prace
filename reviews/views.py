from django.shortcuts import render, get_object_or_404
from .models import Food, Review
from .forms import ReviewForm

def food_view_list(request):
