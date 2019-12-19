import os
from mimetypes import guess_type
from wsgiref.util import FileWrapper

from django.conf import settings
# from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

# Create your views here.
import digitalmarket.mixins
# from sellers.models import SellerAccount
# from sellers.mixins import SellerAccountMixin
from tags.models import Tag
from .forms import ProductModelForm
from .models import Product, ProductRating


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
        products = Product.objects
        if query:
            products = products.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).exclude(seller=request.user).order_by("title")
        else:
            products = products.exclude(seller=request.user).order_by("title")

        context = {
            'product_list': products
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
        
        a form for assigning fields in new product
        
        **Template**
        
        :template:`products/product_create.html`
        
        """
    model = Product
    template_name = "products/product_create.html"
    form_class = ProductModelForm
    # success_url = "/products/"
    submit_btn = "Create Product"

    def form_valid(self, form):
        seller = self.request.user
        form.instance.seller = seller
        valid_data = super(ProductCreateView, self).form_valid(form)
        return valid_data


# Might not be useful
class ProductRatingAjaxView(digitalmarket.mixins.AjaxRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)
        # credit card required **

        user = request.user
        product_id = request.POST.get("product_id")
        rating_value = request.POST.get("rating_value")
        exists = Product.objects.filter(id=product_id).exists()
        if not exists:
            return JsonResponse({}, status=404)

        try:
            product_obj = Product.object.get(id=product_id)
        except:
            product_obj = Product.objects.filter(id=product_id).first()

        rating_obj, rating_obj_created = ProductRating.objects.get_or_create(
            user=user,
            product=product_obj
        )
        try:
            rating_obj = ProductRating.objects.get(user=user, product=product_obj)
        except ProductRating.MultipleObjectsReturned:
            rating_obj = ProductRating.objects.filter(user=user, product=product_obj).first()
        except:
            # rating_obj = ProductRating.objects.create(user=user, product=product_obj)
            rating_obj = ProductRating()
            rating_obj.user = user
            rating_obj.product = product_obj
        rating_obj.rating = int(rating_value)
        myproducts = user.myproducts.products.all()

        if product_obj in myproducts:
            rating_obj.verified = True
        # verify ownership
        rating_obj.save()

        data = {
            "success": True
        }
        return JsonResponse(data)


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
        print initial
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
