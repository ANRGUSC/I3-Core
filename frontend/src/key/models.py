from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
from django.db import models
from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Sum
from django.db.models.signals import pre_save

class Key(models.Model):
    """
        Model representing user's shopping cart
        
        Cart(id, user, timestamp, updated)
        """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=False, blank=True)
    # items = models.ManyToManyField(Product, through=CartItem)
    key = models.CharField(max_length=32)
    acknowledgement = models.BooleanField(default=False)
    def get_absolute_url(self):
        """ returns url for API Key view
            """
        view_name = "key:index"
        return reverse(view_name)