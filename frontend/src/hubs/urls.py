from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from .views import (
    list_view,
    create_view,
    detail_view,
)

app_name = 'hubs'
urlpatterns = [
    url(r'^$', list_view, name='list'),
    url(r'^create/', create_view, name='create'),
    url(r'^(?P<hub_id>\d+)/$', detail_view, name='detail'),
]
