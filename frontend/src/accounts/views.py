# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
import django
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from digitalmarket.mixins import StaffRequiredMixin

from forms import *

TYPE_DICT = {'1': 'Seller', '2': 'Buyer', '3': 'Both'}


class LoginView(View):
    """
        Displays a login page.
        
        (View)
        
        **Context**
        
        
        
        **Template**
        
        :template:`registration/login.html`
        """
    def get(self, request, *args, **kwargs):
        """ Redirects to dashboard page page if user is authenticated, else renders login page.
            """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))

        context = {}

        return render(request, 'registration/login.html', context=context)

    def post(self, request, *args, **kwargs):
        """ Submits user and name and password for authentication, raises errors if input is invalid. Redirects to dashboard if user is authenticated.
            """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))

        username = request.POST['username']
        password = request.POST['password']
        user = django.contrib.auth.authenticate(username=username, password=password)
        # user = django.contrib.auth.authenticate(request, username=username, password=password)

        if user is None:
            context = {
                'error': 'Invalid username/password!'
            }
            return render(request, 'registration/login.html', context=context)
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))

    def delete(self, request, *args, **kwargs):
        """ If user is authenticated, will redirect to current http request instance, otherwise to login page.
            """
        if request.user.is_authenticated():
            logout(request)

        return HttpResponseRedirect(reverse('login'))


class LogoutView(View):
    """
        Displays a logout page.
        """
    def get(self, request, *args, **kwargs):
        """
            redirect to logout page
            """
        if request.user.is_authenticated():
            logout(request)

        return HttpResponseRedirect(reverse('login'))

class UserCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = User
    template_name = "accounts/user_create.html"
    form_class = UserModelForm
    success_url = "/dashboard/users/"
    submit_btn = "Create User"

    # def form_valid(self, form):
    #     valid_data = super(UserCreateView, self).form_valid(form)
    #     return valid_data
    #
    # def form_invalid(self, form):
    #     invalid_data = super(UserCreateView, self).form_invalid(form)
    #     return invalid_data


class SignUpView(CreateView):
    model = User
    template_name = 'registration/signup.html'
    success_url = '/accounts/login/'
    submit_btn = 'Sign Up'
    form_class = UserModelForm

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return super(SignUpView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def form_valid(self, form):
        valid_data = super(SignUpView, self).form_valid(form)
        return valid_data

    def form_invalid(self, form):
        invalid_data = super(SignUpView, self).form_invalid(form)
        return invalid_data
class InviteUserView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = User
    template_name = 'registration/invite.html'
    success_url = '/accounts/invite'
    submit_btn = 'Invite'
    form_class = UserInviteModelForm
    def form_valid(self, form):
        valid_data = super(InviteUserView, self).form_valid(form)
        form.send_email(str(form.cleaned_data['email']))
        return valid_data