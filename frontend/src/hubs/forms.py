from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

PRIVATE_CHOICES = [[True, 'Private'],[False, 'Public']]

class HubCreateForm(forms.Form):

    name = forms.CharField()
    private = forms.ChoiceField(choices=PRIVATE_CHOICES, required=True)

    def clean_name(self):
    
        data = self.cleaned_data['name']
        
        #  a hub name can only contain alpla-numeric chars
        if (not data.isalnum()):
            raise ValidationError(_('Invalid Name'))
        
        if len(data) < 3:
            raise ValidationError(_('Too short'))
            
        if len(data) > 30:
            raise ValidationError(_('Too long'))
        # Remember to always return the cleaned data.
        return data
