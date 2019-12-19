from django.conf.urls import url

from .views import NotificationBoxView, NotificationUpdateView

urlpatterns = [
    url(r'^$', NotificationBoxView.as_view(), name='list'),
    url(r'^ajax/(?P<pk>\d+)/(?P<action>read|unread|archive)/$', NotificationUpdateView.as_view(), name='mark'),
    url(r'^ajax/all/(?P<action>read|unread|archive)/$', NotificationUpdateView.as_view(), name='mark_all')
]   