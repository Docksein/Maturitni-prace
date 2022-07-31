"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
from django import urls
from django.contrib import admin
from django.urls import path, include
from reviews.views import food_list_view, review_view, home_view, user_review_view, tag_list_view, tags_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('jidla/', food_list_view, name='food_list'),
    path('jidla/<int:food_id>', review_view, name='food_reviews'),
    path('', include("django.contrib.auth.urls")),
    path('moje_hodnoceni/', user_review_view, name = "user_review_view"),
    path('tag/<str:pk>', tag_list_view, name='tag_list'),
    path('tagy/', tags_view, name='all_tags_list'),
    path('accounts/', include('allauth.socialaccount.providers.google.urls')),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
