from django import forms
from .models import Drink, Song, DrinkRating, SongRating, Art

#// Drink Forms //#
class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ["name", "category", "ingredients", "method"]
        widgets = {
            "ingredients": forms.Textarea(attrs={"rows": 3, "placeholder": "List ingredients separated by commas"}),
            "method": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe the preparation method"}),
        }

class DrinkRatingForm(forms.ModelForm):
    class Meta:
        model = DrinkRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),  # 1-5 star selection
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...', 'class': 'form-control'}),
        }

#// Song Forms \\#
class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["title", "artist", "genre", "audio_file"]


class SongRatingForm(forms.ModelForm):
    class Meta:
        model = SongRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),  # 1-5 star selection
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...', 'class': 'form-control'}),
        }

#// Art Forms \\#
class ArtForm(forms.ModelForm):    
    class Meta:
        model = Art
        fields = ["title", "artist", "description", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }