from django import forms
from .models import Review

rating_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )


class ReviewForm(forms.ModelForm):
    """
    A class to represent a review for a form that the user fills out
    ...
    Attributes
    ----------
    comment: str
        comment of the food
    ratings: int
        rating of the food from 1 to 5 (1 being the worst, 5 being the best)
    """
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"rows":10, "cols":70, "class":"form-control", "placeholder":"Zde přidejte komentář"}
        ),        
        label = "Komentář"

    )
    ratings = forms.ChoiceField(
        label = "Hodnocení",
        choices= rating_choices,
        widget = forms.Select(
            attrs={"class":"form-control"},
        ),
    )

    class Meta:
        model = Review
        fields = ["ratings", "comment"]
