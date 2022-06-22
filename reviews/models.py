from email.policy import default
from unicodedata import name
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import numpy 


class Food (models.Model):
    
    title = models.CharField(max_length=100)
    upload_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=100, null=True)

    def average_rating(self):
        all_ratings = map(lambda x: x.ratings, self.review_set.all())
        return str(numpy.mean(list(all_ratings)))[:5]

    def get_absolute_url(self):
        return reverse("food_reviews", kwargs={"food_id": self.id})

    def __str__(self):
        return self.title


class Review (models.Model):

    rating_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    published_date = models.DateTimeField(default=timezone.now)
    food_key = models.ForeignKey(Food, on_delete=models.CASCADE)
    author_name = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    ratings = models.IntegerField(choices=rating_choices)
