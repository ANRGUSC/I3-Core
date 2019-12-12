from __future__ import print_function

import random
import string
import subprocess
import time
from configparser import SafeConfigParser

import MySQLdb
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.generic import View

from billing.models import Transaction, ItemCount, RestrictedRequest
from digitalmarket.mixins import AjaxRequiredMixin
from notifications.models import NotificationItem
from flows.models import Flow

#NP_PATH = '/home/zxc/Desktop/frontend/src/np'
#CHECKOUT_LOG_PATH = '/home/zxc/Desktop/checkout_log'

class CheckoutAjaxView(LoginRequiredMixin, AjaxRequiredMixin, View):
    """
        View for the checkout function
        Add password, send email, send notification, send flow, deal with restricted permission
        """
    # Added: sending message to the broker
    def _sendAdminEmail(self, user, seller, topic, prod_num, message, request_file, restricted_active, request,
                        product_obj):

        config = SafeConfigParser()
        config.read('/code/config.ini')
        db = MySQLdb.connect(host=config.get('main', 'mysql_host'),  # your host, usually localhost
                         user=config.get('main', 'mysql_name'),  # your username
                         passwd=config.get('main', 'mysql_pw'),  # your password
                         db=config.get('main', 'mysql_db'))  # your database
        cur = db.cursor()
        log = config.get('main', 'checkout_log_path')
        NP_PATH = config.get('main', 'np_path')
        username = user.username
        user_email = user.email
        topic = topic

        # Password with 6 characters (lower case + number)
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

        # To do: make topic as a product obj that can be linked to
        flow_obj = Flow.objects.create(
            user=request.user,
            topic=topic,
            direction='in',
            state='inactive')
        flow_obj.save()

        # send to the user which topic is able to pub/sub
        # when the topic is unrestricted: insert to acls and send confirmation back to buyer
        if not restricted_active:
            subject = 'New product purchased'
            msg = 'Now you can subscribe to topic: ' + topic + '.'
            email = EmailMessage(subject, msg, to=[user_email])
            email.send()

            # Record email as notification
            notification_box = request.user.get_notification_box()
            notification_item = NotificationItem(
                notification_box=notification_box,
                subject=subject,
                body=msg)
            notification_item.save()

            subject = 'New buyer of an unrestricted topic'
            msg = 'Buyer ' + username + ' just bought product ' + topic + '.'
            email = EmailMessage(subject, msg, to=[seller.email])
            email.send()

            # Record email as notification
            notification_box = seller.get_notification_box()
            notification_item = NotificationItem(
                notification_box=notification_box,
                subject=subject,
                body=msg)
            notification_item.save()

            # insert into acls table
            rw = 1  # seller: can read and write
            if product_obj.sensor_type >= 2:
                rw = 2
            cur.execute("insert into acls (username,topic,rw,user_id, topic_id) values (%s,%s,%s,%s,%s)",
                        (username, topic, str(rw), user.id, product_obj.id))

            # write new sub info to log
            with open(log, 'a') as f:
                f.write(str(time.time()) + ': New Sub ' + username + ' ' + topic + ' ' + str(prod_num) + '\n')

        else:

            restricted_request_obj = RestrictedRequest(
                seller=product_obj.seller,
                requester=request.user,
                product=product_obj,
                price=product_obj.price,
                quantity=prod_num,
                intention=message,
                attachment=request_file
            )
            restricted_request_obj.save()

            subject = 'New product purchased (to be confirmed)'
            msg = 'Waiting seller to confirm purchase of ' + topic + '.'
            email = EmailMessage(subject, msg, to=[user_email])
            email.send()

            # Record email as notification
            notification_box = request.user.get_notification_box()
            notification_item = NotificationItem(
                notification_box=notification_box,
                subject=subject,
                body=msg)
            notification_item.save()

            subject = 'New buyer of a restricted topic'
            msg = 'Buyer ' + username + ' just bought product ' + topic + '. You need to approve the purchase.'
            email = EmailMessage(subject, msg, to=[seller.email])
            email.send()

            # Record email as notification
            notification_box = seller.get_notification_box()
            notification_item = NotificationItem(
                notification_box=notification_box,
                subject=subject,
                body=msg)
            notification_item.save()

        db.commit()

    def post(self, request, *args, **kwargs):
        # TODO: add credit card processing

        user = request.user
        cart = user.get_cart()

        if cart.num_items() == 0:
            data = {
                'success': False,
                'errMsg': 'Your cart is empty'
            }
            return JsonResponse(data=data)

        processed_items = []
        for item in cart.all_items():
            # TODO: how to handle restricted?
            transaction = Transaction(
                buyer=request.user,
                seller=item.product.seller,
                product=item.product,
                price=item.product.get_price * item.quantity,
                quantity=item.quantity,
            )
            transaction.save()

            item_count = ItemCount(
                buyer=request.user,
                product=item.product,
                order=item.quantity,
                quantity=item.quantity,
            )
            item_count.save()
            
            try:
                self._sendAdminEmail(user, item.product.seller, item.product.title, item.quantity,
                                     item.intention, item.attachment, item.product.restricted_active, request,
                                     item.product)
                processed_items.append(item)
            except:
                # TODO: log error, recover, try again?
                pass

        links = []
        for item in processed_items:
            download_link = item.product.get_download()
            preview_link = download_link + "?preview=True"
            link = {
                "download": download_link,
                "preview": preview_link,
            }
            links.append(link)
            item.delete()

        data = {
            'success': True,
            'links': links
        }

        return JsonResponse(data=data)


class RequestsAjaxView(LoginRequiredMixin, AjaxRequiredMixin, View):
    """
        seller decides whether to approve or decline the buy product request
        
        return Json object for frontend Ajax call
        """
    def post(self, request, *args, **kwargs):
        request_id = kwargs['pk']
        restricted_request = RestrictedRequest.objects.get(pk=request_id)

        if restricted_request.seller != request.user:
            data = {
                'success': False,
                'errMsg': 'Request not found',
                'errCode': '404'
            }
        else:
            task = kwargs['task']
            if task == 'approve':
                restricted_request.success = 1
            else:
                restricted_request.success = 0

            restricted_request.replied = True
            restricted_request.save()

            data = {
                'success': True
            }

        return JsonResponse(data=data)
