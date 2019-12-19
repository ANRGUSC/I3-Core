from django.conf.urls import url

from .views import KeyCreateView, KeyDetailView

urlpatterns = [
    url(r'^$', KeyDetailView.as_view(), name='index'),
    url(r'^create/$', KeyCreateView.as_view(), name='create'),
]
