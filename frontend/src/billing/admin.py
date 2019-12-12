from django.contrib import admin

# Register your models here.

from .models import Transaction
from .models import ItemCount, RestrictedRequest


class TransactionAdmin(admin.ModelAdmin):
    # inlines = [ThumbnailInline]
    list_display = ["__unicode__", "product", "buyer", "seller", "quantity", "price", "timestamp"]
    search_fields = ["price", "description"]

    list_filter = ["buyer", "seller"]
    # list_editable = ["sale_price"]

    class Meta:
        model = Transaction


class ItemCountAdmin(admin.ModelAdmin):
    # inlines = [ThumbnailInline]
    list_display = ["__unicode__", "product", "buyer", "quantity", "order", "price", "last_recv_timestamp",
                    'order_timestamp', 'success']
    search_fields = ["product"]

    # list_filter = ["price", "sale_price"]
    # list_editable = ["sale_price"]
    class Meta:
        model = ItemCount


class RestrictedRequestAdmin(admin.ModelAdmin):
    # inlines = [ThumbnailInline]
    list_display = ["__unicode__", "product", "requester", "seller", "price", "quantity", "intention", "success"]
    search_fields = ["seller"]

    # list_filter = ["price", "sale_price"]
    # list_editable = ["sale_price"]
    class Meta:
        model = RestrictedRequest


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ItemCount, ItemCountAdmin)
admin.site.register(RestrictedRequest, RestrictedRequestAdmin)
