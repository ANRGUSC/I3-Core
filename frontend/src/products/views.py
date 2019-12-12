import os
from mimetypes import guess_type
from wsgiref.util import FileWrapper
from configparser import SafeConfigParser
from django.conf import settings
# from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
# Create your views here.
import digitalmarket.mixins
# from sellers.models import SellerAccount
# from sellers.mixins import SellerAccountMixin
from tags.models import Tag
from .forms import ProductModelForm
from .models import Product, ProductRating
from hubs.models import Hub
import MySQLdb
from notifications.models import NotificationItem
from django.core.mail import EmailMessage
from accounts.models import User
from django.core.serializers.json import DjangoJSONEncoder
import json
#HUB_CHOICES = [['1','1'],['2','2'],['3','3']]

class ProductListView(LoginRequiredMixin, View):
    """
        Displays a list of products.
        
        (LoginRequiredMixin, View)
        
        :model:`products.Products`
        
        **Context**
        
        :model:`products.Products`
        
        ``product_list``: a list of products excluding ones where user is seller.
        
        **Template**
        
        :template:`products/product_list.html`
        
        """
    def get(self, request, *args, **kwargs):
        """ Takes request and renders page of products list.
            """
        query = request.GET.get("q")
        latitude = request.GET.get("lat")
        longitude = request.GET.get("long")
        radius = request.GET.get("rad")
        products = Product.objects
        if query:
            products = products.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).exclude(seller=request.user).order_by("title")
        # TODO: get products within a radius
        elif (latitude and longitude and radius):
            products = products.exclude(seller=request.user).order_by("title")
            
        else:
            products = products.exclude(seller=request.user).order_by("title")

        default_query = ""
        if(query is not None):
            default_query = str(query)
        # print(default_query)
        context = {
            'product_list': products,
            'default_query': default_query
        }

        return render(request, 'products/product_list.html', context=context)

class ProductDetailView(LoginRequiredMixin, digitalmarket.mixins.MultiSlugMixin, DetailView):
    """
        Displays a detailed view of a product.
        
        (LoginRequiredMixin, MultiSlugMixin, DetailView)
        
        :model:`products.Products`
        
        **Context**
        
        :model:`products.Products`
        
        instance of Product that was referenced by slug in request
        
        **Template**
        
        :template:`products/product_detail.html`
        
        """

    model = Product

    def get_context_data(self, *args, **kwargs):
        """ Retrieves product object for detail view.
            """
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    """
        Displays a form for seller to add a product to their account.
        
        (LoginRequiredMixin, CreateView)
        
        :model:`products.Products`
        
        **Context**
        
        a form for assigning fields in n6ew product
        
        **Template**
        
        :template:`products/product_create.html`
        
        """
    model = Product
    template_name = "products/product_create.html"
    form_class = ProductModelForm
    # success_url = "/products/"
    submit_btn = "Create Product"
    
    def form_valid(self, form):
        valid_hub_name = 0
        queryset_hub = Hub.objects.filter(seller_name=self.request.user.username)
        for h in queryset_hub:
            if h.name == self.request.user.username + '/' + form.instance.hub:
                valid_hub_name = 1
                break
        if(valid_hub_name == 0):
            return HttpResponseRedirect('products/create')
            
        queryset_product = Product.objects.filter(hub=(self.request.user.username+'/'+form.cleaned_data['hub']))
        for p in queryset_product:
            if p.title == self.request.user.username + '/' + form.cleaned_data['hub'] + '/' + form.cleaned_data['title']:
                return HttpResponseRedirect('products/create')
                    
        seller = self.request.user
        form.instance.seller = seller
        form.instance.hub = self.request.user.username + '/' + form.instance.hub
        form.instance.title = form.instance.hub + '/' + form.instance.title
        valid_hub_name = 0
        queryset_hub = Hub.objects.filter(seller_name=self.request.user.username)
        valid_data = super(ProductCreateView, self).form_valid(form)
        return valid_data

class ProductMapView(LoginRequiredMixin, View):
    """
        Displays a page for the user to see the products registered on a map
        """
    def get(self, request, *args, **kwargs):
        """ Takes request and renders page of products list.
            """
        query = request.GET.get("q")
        latitude = request.GET.get("lat")
        longitude = request.GET.get("long")
        radius = request.GET.get("rad")
        products = Product.objects.filter(longitude__isnull=False).filter(latitude__isnull=False)
        if query:
            products = products.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).exclude(seller=request.user).order_by("title")
        # TODO: get products within a radius
        elif (latitude and longitude and radius):
            products = products.exclude(seller=request.user).order_by("title")
            
        else:
            products = products.exclude(seller=request.user).order_by("title")
        # return a list of json objects, easy for javascript to process

        product_value_list = products.values_list('id', 'longitude', 'latitude', 'title')
        #print (product_value_list)
        product_list_json = json.dumps(list(product_value_list), cls=DjangoJSONEncoder)
        #print (product_list_json)
        default_query = ""
        if(query is not None) :
            default_query = str(query)
        context = {
            'product_list': product_list_json,
            'default_query': default_query
        }
        return render(request, 'products/product_map.html', context=context)

@login_required
def product_delete(request, product_id):
    """
        Function for the user to delete the product he created
        All buyers of this product would be notified
        It's NOT suggested to use this funciton
        """
    instance = get_object_or_404(Product, id=product_id)
    if not (request.user.id==instance.seller_id):
        context = {}
        return render(request, 'products/product_delete_not_allowed.html', context)
        
    config = SafeConfigParser()
    config.read('/code/config.ini')
    db = MySQLdb.connect(host=config.get('main', 'mysql_host'),  # your host, usually localhost
                         user=config.get('main', 'mysql_name'),  # your username
                         passwd=config.get('main', 'mysql_pw'),  # your password
                         db=config.get('main', 'mysql_db'))  # your database
    
    cur = db.cursor()
    # Anyone who bought this product should be notified
    # when the creator deleted this product
    cur.execute("select user_id from acls where topic_id='{0}'".format(product_id))
    buyer_id_list = [item[0] for item in cur.fetchall()]
    # print (type(buyer_id_list))
    # print (buyer_id_list)
    # for i in buyer_id_list:
    #     print (i)
    #     print (type(i))
    for i in buyer_id_list:
        buyer_id = int(i)
        if(not buyer_id==request.user.id):
            buyer = get_object_or_404(User, id=buyer_id)
            subject = request.user.username + ' deleted a product you bought'
            msg = instance.title + ' deleted by ' + request.user.username
            email = EmailMessage(subject, msg, to=[buyer.email])
            email.send()

            notification_box = buyer.get_notification_box()
            notification_item = NotificationItem(
            notification_box=notification_box,
            subject=subject,
            body=msg)
            notification_item.save()
        
    cur_del = db.cursor()
    cur_del.execute("delete from acls where topic_id='{0}'".format(product_id))
    
    db.commit()
    subject = 'New product deleted'
    msg = instance.title + ' deleted from ' + instance.hub
    email = EmailMessage(subject, msg, to=[request.user.email])
    email.send()

    notification_box = request.user.get_notification_box()
    notification_item = NotificationItem(
    notification_box=notification_box,
    subject=subject,
    body=msg)
    notification_item.save()
    instance.delete()
    return render(request, 'products/product_delete.html')
       
class ProductRatingAjaxView(digitalmarket.mixins.AjaxRequiredMixin, View):
    """
        Function for the user to check ratng and rate a product
        POST operation comes with permission control
        if request user is not logged in, return fail
        if request user is creator of request product, return fail
        if request user already rated the product, return fail (even if he bought it more than once)
        everybody can rate the product (once and for all)
        product rating have two values: overall rating (average by all raters) and verified rating (average by buyers)
        """

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=401)

        user = request.user
        product_id = request.POST.get("product_id")
        rating_value = request.POST.get("rating_value")
        exists = Product.objects.filter(id=product_id).exists()
        if not exists:
            return JsonResponse({}, status=404)
            
        product_instance = Product.objects.get(id=product_id)
        if(product_instance.seller_id == user.id):
            return JsonResponse({}, status=401)
            
        rating_exists = ProductRating.objects.filter(product_id=product_id).filter(user_id=user.id).exists()
        if rating_exists:
            return JsonResponse({}, status=401)
            
        rating_instance = ProductRating()
        rating_instance.user_id = user.id
        rating_instance.product_id = product_id
        rating_instance.rating = rating_value
        # TODO: add verified buyer
        rating_instance.verified = False
        
        rating_instance.save()
        data = {
            "success": True
        }
        return JsonResponse(data)
        
    # GET operation has no permission control
    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({}, status=401)
            
        product_id = request.GET.get("product_id")
        exists = Product.objects.filter(id=product_id).exists()
        if not exists:
            return JsonResponse({}, status=404)
            
        queryset_productRating = ProductRating.objects.filter(product_id=product_id)
        
        if not queryset_productRating:
            response_obj = {
                "rating": 0,
		"count": 0,
                "success": True
            }
            return JsonResponse(response_obj)
        else:
            total = 0
            count = 0
            for instance in queryset_productRating:
                total = total + instance.rating
                count = count + 1      
            response_obj = {
                "rating": round(float(total)/count, 2),
                "count": count,
                "success": True
            }
            return JsonResponse(response_obj)
        return JsonResponse({}, status=404)


class ProductUpdateView(digitalmarket.mixins.SubmitBtnMixin, digitalmarket.mixins.MultiSlugMixin, UpdateView):
    """
        Displays view for seller to update product data.
        
        (ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView)
        
        :model:`products.Product`
        
        **Context**
        
        Form for updating fields in an existing product
        
        **Template**
        
        :template:`form.html`
        
        """

    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    # success_url = "/products/"
    submit_btn = "Update Product"

    def get_initial(self):
        """ Retrieves initial data for the form fields.
            """
        initial = super(ProductUpdateView, self).get_initial()
        tags = self.get_object().tag_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])
        """
        tag_list = []
        for x in tags:
            tag_list.append(x.title)
        """
        return initial

    def form_valid(self, form):
        """ Saves valid data or rasies error.
            """
        valid_data = super(ProductUpdateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        obj = self.get_object()
        obj.tag_set.clear()
        if tags:
            tags_list = tags.split(",")

            for tag in tags_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(self.get_object())
        return valid_data


class ProductDownloadView(digitalmarket.mixins.MultiSlugMixin, DetailView):
    """
        Displays detail view of product with a downloadable file.
        
        (MultiSlugMixin, DetailView)
        
        :model:`products.Product`
        
        **Context**
        
        :model:`products.Product`
        
        obj.media.path
        
        **Template**
        
        :template:`products/product_detail.html`
        
        """

    model = Product

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj in request.user.myproducts.products.all():
            filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
            guessed_type = guess_type(filepath)[0]
            wrapper = FileWrapper(file(filepath))
            mimetype = 'application/force-download'
            if guessed_type:
                mimetype = guessed_type
            response = HttpResponse(wrapper, content_type=mimetype)

            if not request.GET.get("preview"):
                response["Content-Disposition"] = "attachment; filename=%s" % (obj.media.name)

            response["X-SendFile"] = str(obj.media.name)
            return response
        else:
            raise Http404


class SellerProductListView(ListView):
    """
        Displays a a list of a products from the user's SellerAccount.
        
        (ListView)
        
        :model:`products.Product`
        
        **Context**
        
        object_list for super class ListView
        
        query set is filtered by user's seller account
        
        **Template**
        
        :template:`products/product_list_view.html`
        """
    model = Product
    template_name = "sellers/product_list_view.html"

    def get_queryset(self, *args, **kwargs):
        """ Returns query set filtered by user's account.
            """
        qs = super(SellerProductListView, self).get_queryset(**kwargs)
        qs = qs.filter(seller=self.get_account())
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).order_by("title")
        return qs


class VendorListView(ListView):
    """
        Displays list of products belonging to a queried seller's account.
        
        (ListView)
        
        :model:`products.Product`
        
        **Context**
        
        object_list for super class ListView
        
        **Template**
        
        products/product_list.html
        
        """
    model = Product
    template_name = "products/product_list.html"

    def get_object(self):
        """ Get object of seller's account.
            """
        username = self.kwargs.get("vendor_name")
        seller = get_object_or_404(SellerAccount, user__username=username)
        return seller

    def get_context_data(self, *args, **kwargs):
        """ Get context, list of products by vendor (a seller's account).
            """
        context = super(VendorListView, self).get_context_data(*args, **kwargs)
        context["vendor_name"] = str(self.get_object().user.username)
        return context

    def get_queryset(self, *args, **kwargs):
        """ Return query set of products by seller
            """
        seller = self.get_object()
        qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).order_by("title")
        return qs
'''
def create_view(request):
    """ Takes a http request and renders a page for creating a product.
        """
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        print form.cleaned_data.get("publish")
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "form": form,
        "submit_btn": "Create Product"
    }
    return render(request, template, context)


def update_view(request, object_id=None):
    """ Renders a page with context for updating product
        """
    product = get_object_or_404(Product, id=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        # instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "object": product,
        "form": form,
        "submit_btn": "Update Product"
    }
    return render(request, template, context)


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


def detail_view(request, object_id=None):
    """ Takes a request by id of product and renders a detailed view of product
        """
    product = get_object_or_404(Product, id=object_id)
    template = "detail_view.html"
    context = {
        "object": product
    }
    return render(request, template, context)


def list_view(request):
    """ Renders a page that lists all products.
        """
    # list of items
    print request
    queryset = Product.objects.all()
    template = "list_view.html"
    context = {
        "queryset": queryset
    }
    return render(request, template, context)
'''
