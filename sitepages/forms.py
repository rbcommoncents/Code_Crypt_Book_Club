from django import forms
from .models import Drink, Song

class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ["name", "category", "ingredients", "method"]
        widgets = {
            "ingredients": forms.Textarea(attrs={"rows": 3, "placeholder": "List ingredients separated by commas"}),
            "method": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe the preparation method"}),
        }

class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["title", "artist", "genre", "audio_file"]