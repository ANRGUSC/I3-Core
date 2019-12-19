import time
from configparser import SafeConfigParser

import MySQLdb
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
# from sellers.models import SellerAccount
from django.db.models.signals import pre_save

from notifications.models import NotificationBox, NotificationItem
from products.models import Product


class Transaction(models.Model):
    """
        Model for one transaction
        
        Transaction(id, buyer, seller, product, price, quantity, timestamp, success)
        """
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transaction_buyer')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transaction_seller')
    product = models.ForeignKey(Product, related_name='transactions_set')
    price = models.DecimalField(max_digits=65, decimal_places=2, default=9.99, null=True, )
    quantity = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    success = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % self.id


# Added: item count for buyer to track products
class ItemCount(models.Model):
    """
        Model used for buyer to track products
        
        ItemCount(id, buyer, product, order, price, quantity, order_timestamp, last_recv_timestamp, success)
        """
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    order = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=65, decimal_places=2, default=9.99, null=True, )
    quantity = models.PositiveIntegerField(default=0)
    order_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_recv_timestamp = models.DateTimeField(blank=True, null=True)
    success = models.BooleanField(default=False)

    # transaction_id_payment_system = Braintree / Stripe
    # payment_method
    # last_four

    def __unicode__(self):
        return "%s" % self.id


# Added: restricted request for seller to approve restricted product
class RestrictedRequest(models.Model):
    """
        Model of a request for a transaction that needs approval by seller
        
        RestrictedRequest(id, requester, seller, product, price, quantity, success, intention, replied)
        """
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restricted_request_buyer')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restricted_request_seller')
    product = models.ForeignKey(Product)
    price = models.DecimalField(max_digits=65, decimal_places=2, null=False)
    quantity = models.PositiveIntegerField(default=1)
    success = models.BooleanField(default=False)
    intention = models.TextField(blank=True)
    attachment = models.FileField(null=True)
    replied = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.id


def restrict_request_pre_save_receiver(sender, instance, *args, **kwargs):
    """ Added: when seller approves the restricted request, send a message to the buyer
        """
    if instance.success:
        config = SafeConfigParser()
        config.read('/usr/local/iotm/config.ini')
        db = MySQLdb.connect(host="mysql",  # your host, usually localhost
                             user=config.get('main', 'mysql_name'),  # your username
                             passwd=config.get('main', 'mysql_pw'),  # your password
                             db=config.get('main', 'mysql_db'))  # your database

        cur = db.cursor()
        log = config.get('main', 'log_path')

        username = instance.requester.username
        user_email = instance.requester.email
        topic = instance.product.title
        prod_num = instance.quantity
        subject = 'Purchase approved'
        msg = 'You got your purchase approved. Now you can subscribe to topic: ' + topic + '.'
        email = EmailMessage(subject, msg,
                             to=[user_email])  # Added: send to the buyer to tell him the restricted product is approved
        email.send()

        # Record email as notification
        notification_box = NotificationBox.objects.get_or_create(user=instance.requester)[0]
        notification_item = NotificationItem.objects.create(
            notification_box=notification_box,
            subject=subject,
            body=msg)

        notification_item.save()

        # insert into acls table
        rw = 1  # seller: can read and write
        if instance.product.sensor_type >= 2:
            rw = 2
        cur.execute("insert into acls (username,topic,rw,user_id,topic_id) values (%s,%s,%s,%s,%s)", (username, topic, str(rw), instance.requester.id, instance.product.id))
        db.commit()
        # write new sub info to log
        with open(log, 'a') as f:
            f.write(str(time.time()) + ': New Sub ' + username + ' ' + topic + ' ' + str(prod_num) + '\n')


pre_save.connect(restrict_request_pre_save_receiver, sender=RestrictedRequest)
