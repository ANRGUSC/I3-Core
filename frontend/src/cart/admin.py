from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'num_items', 'updated']
    inlines = [
        CartItemInline
    ]

    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)
