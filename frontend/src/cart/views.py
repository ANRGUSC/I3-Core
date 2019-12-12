from __future__ import print_function

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from cart.models import Cart, CartItem
from digitalmarket.mixins import AjaxRequiredMixin
from products.models import Product


class CartView(LoginRequiredMixin, SingleObjectMixin, View):
    """
        Displays the contents of a user's shopping cart
        
        (LoginRequiredMixin, SingleObjectMixin, View)
        
        :model:`cart.Cart`
        
        **Context**
        
        :model:`cart.Cart`
        
        ``cart``: Cart object belonging to user.
        
        **Template**
        
        :template:`cart/view.html`
        """
    model = Cart
    template_name = "cart/view.html"

    def get_object(self, *args, **kwargs):
        """ calls get_cart() method from User in accounts.models
            """
        return self.request.user.get_cart()

    def get(self, request, *args, **kwargs):
        """ Takes request and renders page with context of Cart
            """
        cart = self.get_object()

        context = {
            "cart": cart
        }

        template = self.template_name
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        """ If request is POST, redirect to cart list page
            """
        cart = self.get_object()

        product_id = int(request.POST.get("item"))
        qty = int(request.POST.get("qty", 1))

        if product_id is not None:
            product = get_object_or_404(Product, pk=product_id)
            message = request.POST.get("request_message", "")
            # print("Request msg: " + str(message))

            cart_item = CartItem(cart=cart, product=product)
            cart_item.quantity = qty
            cart_item.intention = message
            if "request_attachment" in request.FILES:
                cart_item.attachment = request.FILES["request_attachment"]
            cart_item.save()

        return HttpResponseRedirect(reverse('cart:list'))


class CartAjaxView(LoginRequiredMixin, AjaxRequiredMixin, SingleObjectMixin, View):
    """
        Ajax version of cart view
        
        When frontend Javascript makes Ajax call (async), return a Json object
        """

    model = Cart

    def get_object(self, *args, **kwargs):
        return self.request.user.get_cart()

    def post(self, request, *args, **kwargs):
        cart = self.get_object()

        product_id = int(request.POST.get("item"))
        qty = int(request.POST.get("qty", 1))

        if product_id is not None:
            product = get_object_or_404(Product, pk=product_id)
            message = request.POST.get("request_message", "")
            print("Request msg: " + str(message))

            if qty < 1:
                data = {
                    'success': False,
                    'errorMsg': 'Quantity cannot be less than 1',
                    'errorCode': '400'
                }
            else:
                cart_item = CartItem(cart=cart, product=product)
                cart_item.quantity = qty
                cart_item.intention = message
                cart_item.save()

                data = {
                    'success': True
                }
        else:
            data = {
                'success': False,
                'errorMsg': 'Item id not provided',
                'errorCode': '400'
            }

        return JsonResponse(data=data)

    def delete(self, request, *args, **kwargs):
        item_id = int(request.GET.get("item"))
        print(item_id)
        if item_id is not None:
            cart_item = CartItem.objects.get(pk=item_id)
            if cart_item is not None:
                cart_item.delete()

                data = {
                    'success': True
                }
            else:
                data = {
                    'success': False,
                    'errorMsg': 'Cart item not found',
                    'errorCode': '404'
                }
        else:
            data = {
                'success': False,
                'errorMsg': 'Item id not provided',
                'errorCode': '400'
            }

        return JsonResponse(data=data)
