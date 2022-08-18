from tkinter import Scrollbar
from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Food, Review, Tag
from .forms import ReviewForm
from django.utils import timezone
from django.core.paginator import Paginator
import datetime

def is_weekend():
    weekno = datetime.datetime.today().weekday()

    if weekno < 5:
        return False
    else: 
        return True
    
def home_view(request, *args, **kwargs):
    
    today = timezone.now()
    food_list = Food.objects.filter(upload_date__year=today.year, upload_date__month=today.month, upload_date__day=today.day)
    highest_rated = sorted(Food.objects.all(), key=lambda o: (o.average_rating_home()), reverse=True)[:5]
    weekend = is_weekend()

    return render(request, "home.html", {"food_list":food_list, "weekend":weekend, "highest_rated":highest_rated})

def food_list_view(request):
    
    if request.user.is_authenticated: 
        today = timezone.now()
        reviewed_today = Review.objects.filter(published_date__year=today.year, published_date__month=today.month, published_date__day=today.day, author_name = request.user).exists()    
    else:
        reviewed_today = False
    
    p = Paginator(Food.objects.order_by("title"), 10)
    page = request.GET.get('page')
    food_list = p.get_page(page)

    context = { "food_list" : food_list, "reviewed_today" : reviewed_today, }
    return render(request, "jidlo.html", context)

def tag_list_view(request, pk):

    tag = get_object_or_404(Tag, pk=pk)
    food_list = Food.objects.filter(tags=tag.id).order_by('-upload_date')

    return render(request, "tag.html", {"tag":tag, "food_list":food_list})

def tags_view(request):
    tags_list = Tag.objects.order_by("name")
    context = { "tags_list" : tags_list }
    return render(request, "all_tags.html", context)


def review_view(request, food_id):

    today = timezone.now()
    if request.user.is_authenticated: 
        reviewed_today = Review.objects.filter(published_date__year=today.year, published_date__month=today.month, published_date__day=today.day, author_name = request.user).exists()    
    else:
        reviewed_today = False

    food = get_object_or_404(Food, pk=food_id)
    form = ReviewForm(request.POST or None)
    review_list = Review.objects.filter(food_key = food).order_by('-published_date')

    if request.method == "POST":
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            if Review.objects.filter(published_date__year=today.year, published_date__month=today.month, published_date__day=today.day, author_name = request.user).exists():
                return render(request, "cannot_review.html", {"food":food})
            else:   
                ratings = form.cleaned_data['ratings']
                comment = form.cleaned_data['comment']
                review = Review(author_name = request.user)
                review.ratings = ratings
                review.comment = comment
                review.food_key = food
                review.published_date = timezone.now()
                review.save()
                form = ReviewForm()
                return render(request, "review_post.html", {"food":food})
                
        else:
            form = ReviewForm()
    
    return render(request, "reviews.html", { "form": form, "food":food, "review_list":review_list, "reviewed_today" : reviewed_today, })

def user_review_view(request):
    username = request.user
    review_list = Review.objects.filter(author_name=username).order_by('-published_date')
    return render(request, "user_reviews.html", {"review_list":review_list})