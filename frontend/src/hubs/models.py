# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Hub(models.Model):
    """
        Defines the basic data structure for a Hub
        
        Hub(id, seller_name, name in the form of {SELLER_NAME}/{HUB_NAME})
        """
    seller_name = models.CharField(max_length=30)
    name = models.CharField(max_length=80)
    private = models.BooleanField(default=True)
