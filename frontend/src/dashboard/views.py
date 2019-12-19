from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View, ListView

from accounts.models import User
from digitalmarket.mixins import StaffRequiredMixin
from products.models import Product


class DashboardView(LoginRequiredMixin, View):
    """
        Displays dashboard
        
        (LoginRequiredMixin, View)
        
        **Context**
        
        If user is not a seller context does not include list of products for sale by user.
        
        :model:`products.Product`,  :model:`accounts.User`
        
        
        ``product_list``: a list of all products excluding ones sold by user
        
        ``selling``: a list of products user is selling.
        
        ``purchased``: list of products user has purchased
        
        **Template**
        
        :template:`dashboard/view.html`
        
        """
    def get(self, request, *args, **kwargs):
        """ Takes requst and renders page with context list of all products, list of seller's products, list of purchased products. Dashboard does not contain list of seller's products if user is not seller.
            """
        user = request.user

        if user.is_seller():
            product_list = Product.objects.exclude(seller=user)
            selling = user.selling_products()
            purchased = user.purchased_products()

            context = {
                'products': product_list,
                'sales': selling,
                'purchased': purchased
            }
            return render(request, "dashboard/view.html", context)
        else:
            product_list = Product.objects.all()
            purchased = user.purchased_products()

            context = {
                'products': product_list,
                'purchased': purchased
            }
            return render(request, "dashboard/view.html", context)


class UsersListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    template_name = 'accounts/users_list.html'
    model = User
