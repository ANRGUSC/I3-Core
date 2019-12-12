from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from .views import (
    create_view,
    delete_view,
    edit_view,
)

app_name = 'devices'
urlpatterns = [
    url(r'^create/', create_view, name='create'),
    url(r'^delete/(?P<device_id>\d+)/$', delete_view, name='delete'),
    url(r'^edit/(?P<device_id>\d+)/$', edit_view, name='edit'),
]
