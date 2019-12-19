from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from .views import (
    ProductCreateView,
    ProductDetailView,
    ProductDownloadView,
    ProductListView,
    ProductUpdateView,
    ProductRatingAjaxView,
    VendorListView,
    product_delete,
    ProductMapView,
)

app_name = 'products'
urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),  # products:list
    url(r'^map/$', ProductMapView.as_view(), name='map'),
    url(r'^create/', ProductCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail_slug'),
    url(r'^delete/(?P<product_id>\d+)/$', product_delete, name='delete'),
    url(r'^(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='update_slug'),
    url(r'^ajax/rating/$', ProductRatingAjaxView.as_view(), name='ajax_rating'),
    
    url(r'^vendor/$', RedirectView.as_view(pattern_name='products:list'), name='vendor_list'),
    url(r'^vendor/(?P<vendor_name>[\w.@+-]+)/$', VendorListView.as_view(), name='vendor_detail'),
    url(r'^(?P<pk>\d+)/download/$', ProductDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/$', ProductDownloadView.as_view(), name='download_slug'),
]
