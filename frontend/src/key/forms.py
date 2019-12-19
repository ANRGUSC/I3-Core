from django import forms

from django.utils.text import slugify

from .models import Key

class KeyCreateForm(forms.ModelForm):
    class Meta:
        model = Key
        fields = [
            "acknowledgement",
        ]
        widgets = {
            "acknowledgement": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            )
        }