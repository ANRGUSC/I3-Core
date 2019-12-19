import random
import string
import subprocess
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

# CHECKOUT_LOG_PATH = '/home/zxc/Desktop/checkout_log'
# NP_PATH = '/home/zxc/Desktop/frontend/src/np'

class Transaction(models.Model):
    """
        Model for one transaction
        
        Transaction(id, buyer, seller, product, price, quantity, timestamp, success)
        """
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transaction_buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transaction_seller', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='transactions_set', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=65, decimal_places=2, default=9.99, null=True)
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
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restricted_request_buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restricted_request_seller', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=65, decimal_places=2, null=False)
    quantity = models.PositiveIntegerField(default=1)
    # success = models.BooleanField(default=False)
    success = models.PositiveIntegerField(default=2)
    intention = models.TextField(blank=True)
    attachment = models.FileField(null=True)
    replied = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.id


def restrict_request_pre_save_receiver(sender, instance, *args, **kwargs):
    """ Added: when seller approves the restricted request, send a message to the buyer
        """
    if instance.success==1:
        config = SafeConfigParser()
        config.read('/code/config.ini')
        db = MySQLdb.connect(host=config.get('main', 'mysql_host'),  # your host, usually localhost
                         user=config.get('main', 'mysql_name'),  # your username
                         passwd=config.get('main', 'mysql_pw'),  # your password
                         db=config.get('main', 'mysql_db'))  # your database

        cur = db.cursor()
        log = config.get('main', 'checkout_log_path')
        # log = CHECKOUT_LOG_PATH
        NP_PATH = config.get('main', 'np_path')
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

        original_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
        if not cur.execute("select (1) from users where username = %s limit 1", (username,)):
      
            command = NP_PATH + ' ' + '-p' + ' ' + original_password
            command_bytes = command.encode('utf-8')
            pw_bytes = subprocess.Popen(command_bytes, stdout=subprocess.PIPE, shell=True).communicate()[0]
            password = pw_bytes.decode().rstrip('\n')
            
            cur.execute("insert into users (username,pw,user_id) values (%s,%s,%s)",
                        (username, password, user.id))  # stdout: ignore '\n'

            # Send password to email
            subject = 'Your new password'
            msg = "Your password to I3  is: " + original_password
            email = EmailMessage(subject, msg, to=[user_email])
            email.send()

            # Record email as notification
            notification_box = request.user.get_notification_box()
            notification_item = NotificationItem(
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
            
    if instance.success==0: # purchase declined
    
        username = instance.requester.username
        user_email = instance.requester.email
        topic = instance.product.title
        prod_num = instance.quantity
        subject = 'Purchase declined'
        msg = 'You got your purchase declined ' + topic + '.'
        email = EmailMessage(subject, msg,
                             to=[user_email])  # Added: send to the buyer to tell him the restricted product is declined
        email.send()

        # Record email as notification
        notification_box = NotificationBox.objects.get_or_create(user=instance.requester)[0]
        notification_item = NotificationItem.objects.create(
            notification_box=notification_box,
            subject=subject,
            body=msg)

        notification_item.save()

pre_save.connect(restrict_request_pre_save_receiver, sender=RestrictedRequest)
