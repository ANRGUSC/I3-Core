from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from .views import *

# should we allow POST requests?
# Note: Use '' in http part when passing mutiple query parameters
# TODO
"""
All api endpoints require login (API key as auth token)
Everybody should be able to view all products, with filter such as seller, sensor type etc
Everybody should be able to view details of any product

1. GET      /products/: all products. Query filter: sensor_type, seller, price etc.
2. POST     /product/create/: specify all fields, including hub
3. POST     /product/delete/(?P<pk>\d+)/: permission check
4. GET      /product/purchase/: (NO PERMISSION CHECK) list of products this guy bought

HUB and DEVICE are basically the same, with some difference in permission 
5. GET      /hubs/: a list of user's hubs
6. ...
"""

# DOING or DONE:
# GET /products/: all products. Query filters: 'http:{DNS}:8000/api/products/?sensor_type=sensor&seller=zxc' 
#     PK or NAME (detail view)
#     sensor_type = sensor, actuator, both
#     seller = {{SELLER_NAME}}
#     restricted_active
#     ?? sale_price_lower_bound
#     hub
#     description_contains: use %20 to replace space
"""
currently only allow GET request for product query
"""
urlpatterns = [
    url(r'^product/$', ProductAPIView.as_view(), name = "product"),
    #url(r'^seller/product/$', SellerProductListAPIView.as_view(), name = "product_list"),
    #url(r'^seller/product/(?P<pk>\d+)/$', SellerProductDetailAPIView.as_view(), name = "product_detail"),
    #url(r'^buyer/product/$', BuyerProductListAPIView.as_view(), name = "product_list"),
    #url(r'^buyer/product/(?P<pk>\d+)/$', BuyerProductDetailAPIView.as_view(), name = "product_detail"),
    #url(r'^buyer/purchase/$', PurchaseListView.as_view(), name = "purchase_list"),
    #url(r'^buyer/purchase/(?P<pk>\d+)/$', PurchaseDetailView.as_view(), name = "purchase_detail"),
    #url(r'^seller/sale/$', SaleListView.as_view(), name = "sale_list"),
    #url(r'^seller/sale/(?P<pk>\d+)/$', SaleDetailView.as_view(), name = "sale_detail"),
]
