from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
from django.db import models
from decimal import Decimal
from django.conf import settings
from django.db.models.aggregates import Sum
from django.utils.dateformat import format

from products.models import Product
from django.db.models.signals import pre_save


def attachments_locations(instance, filename):
    return 'request_attachments/user_%s/%s_%s_%s' % (instance.cart.user.username,
                                                     instance.product.slug,
                                                     format(instance.added_on, 'U'),
                                                     filename)


class Cart(models.Model):
    """
        Model representing user's shopping cart
        
        Cart(id, user, timestamp, updated)
        """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=False, blank=True)
    # items = models.ManyToManyField(Product, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def num_items(self):
        return self.items.count()

    def all_items(self):
        return self.items.all()

    def total_price(self):
        return self.items.aggregate(total_price=Sum('total_price'))['total_price']

    def __unicode__(self):
        return str(self.id)
        # user
        # items
        # timestamp ** created
        # updated ** updated

        # subtotal price
        # taxes total
        # discounts
        # total price


class CartItem(models.Model):
    """
        Model representing one cart item
        
        CartItem(id, cart, product, quantity, price, total_price, intention)
        """
    cart = models.ForeignKey(Cart, related_name='items')
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=65, decimal_places=2)
    total_price = models.DecimalField(max_digits=65, decimal_places=2)
    added_on = models.DateTimeField(auto_now=True)
    intention = models.TextField(blank=True)
    attachment = models.FileField(upload_to=attachments_locations, null=True,
                                  storage=FileSystemStorage(location=settings.PROTECTED_ROOT))

    def __unicode__(self):
        return self.product.title

    def remove(self):
        return self.product.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    """ before saving, will multiply quantity with price
        """
    qty = instance.quantity
    if qty >= 1:
        instance.price = instance.product.get_price
        instance.total_price = Decimal(qty) * Decimal(instance.price)


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)
