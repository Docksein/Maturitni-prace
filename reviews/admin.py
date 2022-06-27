from django.contrib import admin
from .models import Food, Review, Tag

admin.site.register(Food)
admin.site.register(Review)
admin.site.register(Tag)