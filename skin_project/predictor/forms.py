from django import forms
from .models import SkinPrediction

class SkinPredictionForm(forms.ModelForm):
    class Meta:
        model = SkinPrediction
        fields = ['image']  # Only include the image field for uploading
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }

