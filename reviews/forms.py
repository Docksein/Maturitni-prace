from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows":20,
                "cols":70
            }
        )
    )

    class Meta:
        model = Review
        fields = ["author_name", "ratings", "comment"]
