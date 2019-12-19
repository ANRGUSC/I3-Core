from django import forms
import re

from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
import accounts
from .models import User
from django.core.exceptions import ObjectDoesNotExist


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "user_type",
            "password"
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "tommy",
                    "class": "form-control"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "trojan@usc.edu",
                    "class": "form-control"
                }
            ),
            "user_type": forms.Select(
                choices=accounts.models.USER_TYPES,
                attrs={
                    "class": "form-control"
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }

    verify_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].required = False

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserModelForm, self).clean(*args, **kwargs)

        password = cleaned_data['password']
        verify_password = cleaned_data['verify_password']
        if password and verify_password and password == verify_password:
            cleaned_data['password'] = make_password(password=password)
        else:
            self.add_error('password', 'Passwords do not match')
            self.add_error('verify_password', 'Passwords do not match')

        # if 'user_type' not in cleaned_data:
        #     cleaned_data['user_type'] = accounts.models.BUYER[0]

        return cleaned_data

    def clean_user_type(self):
        if 'user_type' not in self.cleaned_data or self.cleaned_data['user_type'] == '':
            return accounts.models.BUYER[0]
        return self.cleaned_data['user_type']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')
class UserInviteModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
        ]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "trojan@usc.edu",
                    "class": "form-control"
                }
            ),
        }
    def send_email(self, email_address):
        subject = 'You are invited to I3!'
        print self
        msg = 'Please click this link to sign up. http://neptune.usc.edu:8000/accounts/signup'
        email = EmailMessage(subject, msg, to=[email_address])
        email.send()
        pass
    def save(self):
        # Sets username to email before saving
        user = super(UserInviteModelForm, self).save(commit=False)
        return user
