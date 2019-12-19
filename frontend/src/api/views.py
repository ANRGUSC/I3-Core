from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from products.models import Product
from billing.models import Transaction
from django.contrib.auth import get_user_model
from products.serializers import ProductSerializer
from billing.serializers import TransactionSerializer
from rest_framework.authtoken.models import Token

User = get_user_model()

class BuyerProductDetailAPIView(APIView):
    """
    get:
    Returns a specific product that corresponds to the given primary key.

    """
    # Add authentication classes to force authentication to these views
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    def get(self, request, pk, *args, **kwargs):
        try:
            # Get a product by primary key to be returned to the user
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)

class BuyerProductListAPIView(APIView):
    """
    get:
    Returns a list of products.

    You can filter by `seller` or `sensor_type` by passing in url parameters `?seller=<seller_name>` or `?sensor_type=<sensor_type>`
    
    """
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # Require authentication for these views
    def get(self, request, *args, **kwargs):
        # Get all products
        product = Product.objects.all()
        seller = self.request.query_params.get('seller', None)
        sensor_type = self.request.query_params.get('sensor_type', None)
        if seller is not None:
            seller = User.objects.get(username = seller).pk
            product = product.filter(seller=seller)
        if sensor_type is not None:
            if sensor_type == 'sensor':
                sensor_type = 1
            elif sensor_type == 'actuator':
                sensor_type = 2
            else:
                sensor_type = 3
            product = product.filter(sensor_type=sensor_type)
        # Set the pagination class and add pagination to the query set
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(product, request)
        serializer = ProductSerializer(result_page, many=True)
        return JsonResponse(serializer.data, safe=False)
class SellerProductDetailAPIView(APIView):
    """
    get:
    Returns a specific product that corresponds to the given primary key.

    put:
    <b>Update</b> an instance of a product. User attemping to <b>UPDATE</b> the entry must be the same user that created the entry.

    Here is an example JSON file that must but submitted with the <b>PUT</b> request
    
        {
            "media": "http://samplemedia.url",
            "title": "sample title",
            "sensor_type": "sensor",
            "description": "sample description",
            "price": "9.99",
            "sale_active": false,
            "sale_price": "6.99"
        }

    delete:
    <b>Delete</b> an instance of a product. User attemping to <b>DELETE</b> the product must be the same user that created the product..
    """
    # Add authentication classes to force authentication to these views
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()
    def get(self, request, pk, *args, **kwargs):
        try:
            # Get a product by primary key to be returned to the user
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data)
    def put(self, request, pk, *args, **kwargs):
        try:
            print request.body
            # Get a product by primary key to be updated
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return HttpResponse(status=404)
        data = JSONParser().parse(request)
        user = User.objects.get(username=request.user)
        data['seller'] = user
        data['id'] = pk
        # Check if the logged in user created the original product
        if product.seller_id != user.pk:
            return HttpResponse(status=401)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    def delete(self, request, pk, *args, **kwargs):
        try:
            # Get a product by primary key to be deleted
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return HttpResponse(status=404)
        user = User.objects.get(username=request.user)
        # Check if the logged in user created the original product
        if product.seller_id == user.pk:
            product.delete()
            return HttpResponse(status=204)
        return HttpResponse(status=401)

class SellerProductListAPIView(APIView):
    """
    get:
    Returns a list of products. 

    You can filter by `seller` or `sensor_type` by passing in url parameters `?seller=<seller_name>` or `?sensor_type=<sensor_type>`.

    post:
    <b>Create</b> an instance of a product. The data must be submitted with ALL fields that are present when a GET request is performed. i.e. 'seller', 'media', 'title'...
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    # Require authentication for these views
    def get(self, request, *args, **kwargs):
        # Get all products
        product = Product.objects.all()
        seller = self.request.query_params.get('seller', None)
        sensor_type = self.request.query_params.get('sensor_type', None)
        if seller is not None:
            seller = User.objects.get(username = seller).pk
            product = product.filter(seller=seller)
        if sensor_type is not None:
            if sensor_type == 'sensor':
                sensor_type = 1
            elif sensor_type == 'actuator':
                sensor_type = 2
            else:
                sensor_type = 3
            product = product.filter(sensor_type=sensor_type)
        # Set the pagination class and add pagination to the query set
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(product, request)
        serializer = ProductSerializer(result_page, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        user = User.objects.get(username = request.user)
        data['seller'] = user
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class PurchaseListView(APIView):
    """
    get:
    Returns a list of buyer purchases.

    post:
    <b>Purchases</b> a product. 

    Here is an example of the JSON file that must be submitted with the purchase request.
    
        {
            "media": "http://samplemedia.url",
            "title": "sample title",
            "sensor_type": "sensor",
            "description": "sample description",
            "price": "9.99",
            "sale_active": false,
            "sale_price": "6.99"
        }

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()
    def get(self, request, *args, **kwargs):
        purchase = Transaction.objects.filter(buyer_id=request.user.id)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(purchase, request)
        serializer = TransactionSerializer(result_page, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        print data['id']
        product = Product.objects.get(id=data['id'])
        data['product'] = product
        seller = User.objects.get(username=product.seller)
        data['seller'] = seller
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['buyer_id'] = request.user.id
            serializer.validated_data['seller_id'] = seller.id
            serializer.validated_data['product_id'] = product.id
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class PurchaseDetailView(APIView):
    """
    get:
    Returns a specific purchase that was made by the buyer.

    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()
    def get(self, request, pk, *args, **kwargs):
        purchase = Transaction.objects.filter(buyer_id=request.user.id)
        serializer = TransactionSerializer(purchase, many=True)
        pk = int(pk)
        if pk < len(serializer.data):
            return JsonResponse(serializer.data[pk], safe=False)
        return JsonResponse({"status": "out of bounds"}, status=400)
class SaleListView(APIView):
    """
    get:
    Returns a list of sales made by seller.
    """
    queryset = Transaction.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        sale = Transaction.objects.filter(seller_id=request.user.id)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(sale, request)
        serializer = TransactionSerializer(result_page, many=True)
        return JsonResponse(serializer.data, safe=False)
class SaleDetailView(APIView):
    """
    get:
    Returns a single sale made by the seller.
     """
    queryset = Transaction.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, pk, *args, **kwargs):
        sale = Transaction.objects.filter(seller_id=request.user.id)
        serializer = TransactionSerializer(sale, many=True)
        pk = int(pk)
        if pk < len(serializer.data):
            return JsonResponse(serializer.data[pk], safe=False)
        return JsonResponse({"status": "out of bounds"}, status=400)