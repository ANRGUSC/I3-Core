"""digitalmarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

import accounts.views
from accounts.views import *
from checkout.views import CheckoutAjaxView, RequestsAjaxView
from dashboard.views import DashboardView
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    # Homepage
    url(r'^$', DashboardView.as_view(), name='home'),

    # User authentication
    url(r'^accounts/login/$', accounts.views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', accounts.views.LogoutView.as_view(), name='logout'),
    url(r'^accounts/signup/$', accounts.views.SignUpView.as_view(), name='signup'),
    url(r'^accounts/invite/$', accounts.views.InviteUserView.as_view(), name='invite'),
    # Administration
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Seller

    # Buyer
    url(r'^cart/', include("cart.urls", namespace='cart')),
    url(r'^checkout/$', CheckoutAjaxView.as_view(), name='checkout'),
    url(r'^requests/ajax/(?P<pk>\d+)/(?P<task>approve|decline)/$', RequestsAjaxView.as_view(), name='requests'),

    # Common
    url(r'^products/', include("products.urls", namespace='products')),
    url(r'^dashboard/', include("dashboard.urls", namespace='dashboard')),
    url(r'^notifications/', include("notifications.urls", namespace='notifications')),

    # # Other
    url(r'^key/', include("key.urls", namespace='key')),
    url(r'^api/', include("api.urls", namespace='api')),
    url(r'^docs/', include_docs_urls(title='Products API', description='IOTM API endpoint')),
    # url(r'^test/$', CheckoutTestView.as_view(), name='test'),
    # url(r'^seller/', include("sellers.urls", namespace='sellers')),
    # url(r'^tags/', include("tags.urls", namespace='tags')),
    # url(r'^library/', UserLibraryListView.as_view(), name='library'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
