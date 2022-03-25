from django import forms
from .models import Review, Food

class ReviewForm(forms.ModelForm):
    
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows":10,
                "cols":70
            }
        )
    )

    class Meta:
        model = Review
        fields = ["ratings", "comment"]


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["description"]