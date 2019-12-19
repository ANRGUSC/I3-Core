from django.conf.urls import url

from accounts.views import UserCreateView
from billing.views import TransactionsView
from dashboard.views import DashboardView, UsersListView
from flows.views import FlowsView
from analytics import views

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='index'),
    url(r'^transactions/$', TransactionsView.as_view(), name='transactions'),
    url(r'^flows/$', FlowsView.as_view(), name='flows'),
    url(r'^users/$', UsersListView.as_view(), name='users-list'),
    url(r'^users/create$', UserCreateView.as_view(), name='users-create'),
]
