# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db.models import PositiveSmallIntegerField
from django.utils.translation import ugettext_lazy as _

from cart.models import Cart
from notifications.models import NotificationBox
from products.models import Product

SELLER = (1, 'Seller')
BUYER = (2, 'Buyer')
BOTH = (3, 'Both')

USER_TYPES = (SELLER, BUYER, BOTH)


class User(AbstractUser):
    """
        Model for an authorized user
        
        User(id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, user_type)
        """
    REQUIRED_FIELDS = ['email', 'user_type']

    user_type = PositiveSmallIntegerField(_("user type"), choices=(BOTH, SELLER, BUYER), default=BOTH[0])

    def is_seller(self):
        return self.user_type & SELLER[0] != 0

    def selling_products(self):
        return Product.objects.filter(seller=self)

    def purchased_products(self):
        return Product.objects.filter(transactions_set__buyer=self)
        # return self.transaction_buyer.all()

    def get_notification_box(self):
        box, is_new = NotificationBox.objects.get_or_create(user=self)
        if is_new:
            box.save()
        return box

    def notifications(self):
        return self.get_notification_box().get_unarchived()

    def get_cart(self):
        cart, is_new = Cart.objects.get_or_create(user=self)
        if is_new:
            cart.save()
        return cart

    def get_seller_requests(self):
        if self.is_seller():
            return self.restricted_request_seller.filter(replied=False)
        else:
            return None

    class Meta:
        db_table = 'auth_user'

