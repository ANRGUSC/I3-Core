# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import os
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import Hub
from devices.models import Device
from products.models import Product
from .forms import HubCreateForm
from django.urls import reverse
# Create your views here.

@login_required
def create_view(request):
    """ Takes a http request and renders a page for creating a Hub.
        """
    if(request.method == 'POST'):
    
        form = HubCreateForm(request.POST)
        
        # Check if the form is valid:
        if form.is_valid():
            queryset_hub = Hub.objects.filter(seller_name=request.user.username)
            for h in queryset_hub:
                if h.name == request.user.username + '/' + form.cleaned_data['name']:
                    form = HubCreateForm()
                    context = {
                        'form' : form,
                    }
                    return render(request, 'hubs/hub_create.html', context)
            ''' create a hub instance, add username and save to database '''
            instance = Hub()
            instance.seller_name = request.user.username
            instance.name = request.user.username + '/' + form.cleaned_data['name']
            instance.private = form.cleaned_data['private']
            instance.save()
            return HttpResponseRedirect(reverse('hubs:list') )
            
    form = HubCreateForm()
    context = {
        'form' : form,
    }
    return render(request, 'hubs/hub_create.html', context)

@login_required
def list_view(request):
    """ Renders a page that lists all hubs of this seller
        """
    input_username = request.user.username
    ''' choose from database hubs that belong to the logged in seller'''
    queryset = Hub.objects.filter(seller_name = input_username)
    hub_instance_list = []
    for h in queryset:
        hub_instance_list.append(h)
    template = "hubs/hub_list.html"
    context = {
        "hub_instance_list": hub_instance_list
    }
    return render(request, template, context)

@login_required
def detail_view(request, hub_id):
    '''
    Takes a request by id of hub and renders a detailed view of hub (all topics and devices)'''
    hub_instance = get_object_or_404(Hub, id=hub_id)
    
    if not (hub_instance.seller_name==request.user.username):
        if hub_instance.private==True:
            template = "hubs/hub_reject.html"
            return render(request, template) 
        else:
            queryset_device = Device.objects.filter(hub_name = hub_instance.name)
            queryset_product = Product.objects.filter(hub = hub_instance.name)
            product_list = []
            device_list = []
            for d in queryset_device:
                device_list.append(d)
            for p in queryset_product:
                product_list.append(p)
        
            is_private = hub_instance.private
            template = "hubs/hub_detail_no_button.html"
            context = {
                "product_list": product_list,
                "device_list": device_list,
                "is_private": is_private,
            }
            return render(request, template, context)
    
    queryset_device = Device.objects.filter(hub_name = hub_instance.name)
    queryset_product = Product.objects.filter(hub = hub_instance.name)
    product_list = []
    device_list = []
    for d in queryset_device:
        device_list.append(d)
    for p in queryset_product:
        product_list.append(p)
        
    is_private = hub_instance.private
    template = "hubs/hub_detail.html"
    context = {
        "product_list": product_list,
        "device_list": device_list,
        "is_private": is_private,
    }
    return render(request, template, context)

'''
@login_required
def detail_slug_view(request, slug=None):
    """ Takes a request by slug of product and renders a detailed view of product
        """
    product = Product.objects.get(slug=slug)
    try:
        product = get_object_or_404(Product, slug=slug)
    except Product.MultipleObjectsReturned:
        product = Product.objects.filter(slug=slug).order_by("-title").first()
    # print slug
    # product = 1
    template = "detail_view.html"
    context = {
        "object": product
    }
    return render(request, template, context)
'''

'''
class HubListView(LoginRequiredMixin, View):
    """
        Displays a list of hubs that belong to the seller 
        """

    def get(self, request, *args, **kwargs):

class HubDetailView(LoginRequiredMixin, digitalmarket.mixins.MultiSlugMixin, DetailView):
    def get_context_data(self, *args, **kwargs):
        """ Retrieves product object for detail view.
            """
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context


class HubCreateView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        seller = self.request.user
        form.instance.seller = seller
        valid_data = super(ProductCreateView, self).form_valid(form)
        return valid_data
'''
