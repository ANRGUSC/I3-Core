from django.conf.urls import url

from cart.views import CartView, CartAjaxView

urlpatterns = [
    url(r'^$', CartView.as_view(), name='list'),
    url(r'^ajax/$', CartAjaxView.as_view(), name='ajax'),
]
