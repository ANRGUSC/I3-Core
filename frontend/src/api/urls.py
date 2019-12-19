from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
import views

urlpatterns = [
    url(r'^seller/product/$', views.SellerProductListAPIView.as_view(), name = "product_list"),
    url(r'^seller/product/(?P<pk>\d+)/$', views.SellerProductDetailAPIView.as_view(), name = "product_detail"),
    url(r'^buyer/product/$', views.BuyerProductListAPIView.as_view(), name = "product_list"),
    url(r'^buyer/product/(?P<pk>\d+)/$', views.BuyerProductDetailAPIView.as_view(), name = "product_detail"),
    url(r'^buyer/purchase/$', views.PurchaseListView.as_view(), name = "purchase_list"),
    url(r'^buyer/purchase/(?P<pk>\d+)/$', views.PurchaseDetailView.as_view(), name = "purchase_detail"),
    url(r'^seller/sale/$', views.SaleListView.as_view(), name = "sale_list"),
    url(r'^seller/sale/(?P<pk>\d+)/$', views.SaleDetailView.as_view(), name = "sale_detail"),
]