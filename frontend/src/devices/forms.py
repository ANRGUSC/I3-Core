from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from hubs.models import Hub

''' a form choice should be defined as a list or a tuple '''
RGS_TYPE = (('1', 'API_Key'), ('2', 'Asymmetric_Key_Pairs'))
#HUB_CHOICES = [['1', 'API_Key'], ['2', 'Asymmetric_Key_Pairs']]

class DeviceCreateForm(forms.Form):

    ''' only seller_name rendering is necessary'''
    
    # below part is quite confusing... 
    # see tutorial https://www.b-list.org/weblog/2008/nov/09/dynamic-forms/
    '''
    def __init__(self, HUB_CHOICES):
        super(DeviceCreateForm, self).__init__()
        self.fields['password'] = forms.CharField()
        self.fields['hub_name'] = forms.ChoiceField(choices=HUB_CHOICES, required=True)
        self.fields['name'] = forms.CharField()
        #self.fields['seller_name'] = forms.CharField()
        self.fields['rgs_type'] = forms.ChoiceField(choices=RGS_TYPE, required=True)
    '''
    password = forms.CharField()
    hub_name = forms.CharField()
    name = forms.CharField()
    # there shouldn't be a seller_name field in the form
    # because the form is just used for collecting data, it's not for saving to database
    # the seller_name field will be added to backend in view, other data will be collected through form data
    # seller_name = forms.CharField()
    rgs_type = forms.ChoiceField(choices=RGS_TYPE, required=True)
    
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
        
    def clean_password(self):
    
        data = self.cleaned_data['password']
        
        #  a hub name can only contain alpla-numeric chars

        if len(data) < 6:
            raise ValidationError(_('Too short'))
            
        if len(data) > 500:
            raise ValidationError(_('Too long'))
        # Remember to always return the cleaned data.
        return data

class DeviceEditForm(forms.Form):

    password = forms.CharField()
    rgs_type = forms.ChoiceField(choices=RGS_TYPE, required=True)
        
    def clean_password(self):
    
        data = self.cleaned_data['password']
        
        #  a hub name can only contain alpla-numeric chars

        if len(data) < 6:
            raise ValidationError(_('Too short'))
            
        if len(data) > 500:
            raise ValidationError(_('Too long'))
        # Remember to always return the cleaned data.
        return data
