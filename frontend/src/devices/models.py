# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Device(models.Model):
    """
        Defines the basic data structure for a Device
        
        Device(id, seller_name, hub_name, name in the form of 
        {SELLER_NAME}/{HUB_NAME}/{DEVICE_NAME}, rgs_type (1 for api key, 2 for asym key),
        password (np hashed pw or public key string))
        """
    seller_name = models.CharField(max_length=30)
    hub_name = models.CharField(max_length=80)
    name = models.CharField(max_length=100)
    rgs_type = models.CharField(max_length=1)
    password = models.CharField(max_length=1280)
