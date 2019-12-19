from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from rest_framework.authtoken.models import Token
from accounts.models import User
from digitalmarket.mixins import StaffRequiredMixin
from .models import Key
from .forms import KeyCreateForm
from rest_framework.authtoken.models import Token


class KeyCreateView(CreateView):
    template_name = "key/key_create.html"
    form_class = KeyCreateForm
    def form_valid(self, form):
        user = self.request.user
        token = Token.objects.create(user=user)
        valid_data = super(KeyCreateView, self).form_valid(form)
        return valid_data
class KeyDetailView(DetailView):
    template_name = "key/key_detail.html"
    model = Token
    def get(self, request, *args, **kwargs):
        context = {
            "key": Token.objects.get_or_create(user=self.request.user)[0]
        }
        return render(request, "key/key_detail.html", context)