from email.policy import default
from unicodedata import name
from django.forms import ImageField
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import numpy 

class Tag (models.Model):
    """
    A class to represent tag
    ...
    Attributes
    ----------
    name: str
        name of the tag
    
    Methods
    ----------
    get_absolute_url(self)

    __str__(self)
    """

    name = models.CharField(max_length=100)

    def get_absolute_url(self):
        """Return the absolute url of a tag"""
        return reverse("tag_list", kwargs={"pk": self.id})


    def __str__(self):
        """Return the name of a tag instance"""
        return self.name


class Food (models.Model):
    """
    A class to represent a food.
    ...
    Attributes
    ----------
    title : str
        title of the food
    upload_date: timezone.now()
        exact time of when the food was uploaded to the database
    picture: image file
        image file of the food
    tags: foreign key
        Many-to-many database relationship with the Tag class
    
    Methods
    ----------
    average_rating(self)

    average_rating_home(self)

    get_absolute_url(self)

    __str__(self)
    """
    
    title = models.CharField(max_length=200)
    upload_date = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to="images/", blank = True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)


    def average_rating(self):
        """Return average rating of all reviews"""
        all_ratings = map(lambda x: x.ratings, self.review_set.all())
        return str(numpy.mean(list(all_ratings)))[:3]
    
    def average_rating_home(self):
        """
        Return average rating of all reviews.
        If there are no reviews, return 0 so it can be sorted.
         """
        all_ratings = str(numpy.mean(list(map(lambda x: x.ratings, self.review_set.all()))))[:3]
        if all_ratings == "nan":
            return "0"
        else:
            return all_ratings


    def get_absolute_url(self):
        """Return absolute url of a food instance"""
        return reverse("food_reviews", kwargs={"food_id": self.id})

    def __str__(self):
        """Return the title of a food instance"""
        return self.title




class Review (models.Model):
    """
    A class to represent a review
    ...
    Attributes
    ----------
    published_date: timezone.now()
        exact time of when the review was published to the database
    food_key: ForeignKey
        key of the food that the review belongs to
    author_name : str
        name of the author that published the review
    comment: str
        comment of the food
    ratings: int
        rating of the food from 1 to 5 (1 being the worst, 5 being the best)
    """

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
