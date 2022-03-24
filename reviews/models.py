from unicodedata import name
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Food (models.Model):
    
    title = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("food_reviews", kwargs={"food_id": self.id})

    def __str__(self):
        return self.title


class Review (models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    rating_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=40, default="Anonymní")
    comment = models.CharField(max_length=1000)
    ratings = models.IntegerField(choices=rating_choices)