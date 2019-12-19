from django.contrib import admin

# Register your models here.
from . import models


class ThumbnailInline(admin.TabularInline):
    extra = 1
    model = models.Thumbnail


class ProductAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInline]
    list_display = ["__unicode__", "description", "price", "sale_price", "seller"]
    search_fields = ["title", "description"]
    list_filter = ["price", "sale_price", "seller"]
    list_editable = ["sale_price"]

    class Meta:
        model = models.Product


admin.site.register(models.Product, ProductAdmin)

# admin.site.register(MyProducts)

admin.site.register(models.Thumbnail)

admin.site.register(models.ProductRating)

# admin.site.register(CuratedProducts)
