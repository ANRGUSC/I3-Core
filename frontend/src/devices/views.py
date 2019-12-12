# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from configparser import SafeConfigParser
from django.shortcuts import render
import os
import MySQLdb
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from notifications.models import NotificationItem
from django.core.mail import EmailMessage
from .models import Device
from hubs.models import Hub
from products.models import Product
from .forms import DeviceCreateForm, DeviceEditForm
from django.urls import reverse
# Create your views here.
import subprocess

# NP_PATH = '/home/zxc/Desktop/frontend/src/np'

@login_required
def create_view(request):
    """ Takes a http request and renders a page for creating a Device.
        """
    
    if(request.method == 'POST'):
        
        form = DeviceCreateForm(request.POST)
        #print (request.user.username)
        #print (request.POST)      
        #print form['password'].value()
        #print form['hub_name'].value()
        #print form['name'].value()
        #print form['seller_name'].value()
        #print form['rgs_type'].value()
        #print request.content_type
        #print form.is_valid()

        if form.is_valid():
            
            valid_hub_name = 0
            queryset_hub = Hub.objects.filter(seller_name=request.user.username)
            for h in queryset_hub:
                if h.name == request.user.username + '/' + form.cleaned_data['hub_name']:
                    valid_hub_name = 1
                    break
            if valid_hub_name == 0:
                new_form = DeviceCreateForm()
                context = {
                    'form' : new_form,
                }
                return render(request, 'devices/device_create.html', context)
                
            queryset_device = Device.objects.filter(hub_name=(request.user.username+'/'+form.cleaned_data['hub_name']))
            for d in queryset_device:
                if d.name == request.user.username + '$' + form.cleaned_data['hub_name'] + '$' + form.cleaned_data['name']:
                    new_form = DeviceCreateForm()
                    context = {
                        'form' : new_form,
                    }
                    return render(request, 'devices/device_create.html', context)      
            ''' create a device instance and save to database '''
            instance = Device()
            instance.seller_name = request.user.username
            instance.hub_name = request.user.username + '/' + form.cleaned_data['hub_name']
            instance.name = request.user.username + '$' + form.cleaned_data['hub_name'] + '$' + form.cleaned_data['name']
            instance.rgs_type = form.cleaned_data['rgs_type']
            if(instance.rgs_type == '1'): # api key, needs hash
                config = SafeConfigParser()
                config.read('/code/config.ini')
                NP_PATH = config.get('main', 'np_path')         
                command = NP_PATH + ' -p ' + form.cleaned_data['password']
                command_bytes = command.encode('utf-8')
                password_bytes = subprocess.Popen(command_bytes, stdout=subprocess.PIPE, shell=True).communicate()[0]
                instance.password = password_bytes.decode().rstrip('\n')
            else: # public key, no hash
                instance.password = form.cleaned_data['password']
            """
            Authentication is strictly related to devices
            need to insert into both users table and acls table
            """
            
            config = SafeConfigParser()
            config.read('/code/config.ini')
            db = MySQLdb.connect(host=config.get('main', 'mysql_host'),  # your host, usually localhost
                         user=config.get('main', 'mysql_name'),  # your username
                         passwd=config.get('main', 'mysql_pw'),  # your password
                         db=config.get('main', 'mysql_db'))  # your database

            cur = db.cursor()
            # insert into AUTHENTICATION (users) table
            if(instance.rgs_type == '1'): # api key, needs hash
                #command_bytes = command.encode('utf-8')
                #password_bytes = subprocess.Popen(command_bytes, stdout=subprocess.PIPE, shell=True).communicate()[0]
                #password = password_bytes.decode()
                config = SafeConfigParser()
                config.read('/code/config.ini')
                NP_PATH = config.get('main', 'np_path')
                command = NP_PATH + ' -p ' + form.cleaned_data['password']
                command_bytes = command.encode('utf-8')
                device_pw_bytes = subprocess.Popen(command_bytes, stdout=subprocess.PIPE, shell=True).communicate()[0]
                device_pw = device_pw_bytes.decode().rstrip('\n')
                cur.execute("insert into users (username,pw,user_id) values (%s,%s,%s)",
                    (instance.name, device_pw, request.user.id))
                    
            else: # no need to hash
                cur.execute("insert into users (username,pw,user_id) values (%s,%s,%s)",
                    (instance.name, form.cleaned_data['password'], request.user.id))
            
            # insert into AUTHORIZATION (acls) table
            queryset_product = Product.objects.filter(hub = instance.hub_name)
            rw = 2  # seller: can read and write
    
            for p in queryset_product:
                cur.execute("insert into acls (username,topic,rw,user_id,topic_id) values (%s,%s,%s,%s,%s)",(instance.name, p.title, str(rw), request.user.id, p.id))
                
            db.commit()
            
            instance.save()
            subject = 'New device registered'
            msg = instance.name + ' created inside ' + instance.hub_name
            email = EmailMessage(subject, msg, to=[request.user.email])
            email.send()

            notification_box = request.user.get_notification_box()
            notification_item = NotificationItem(
            notification_box=notification_box,
            subject=subject,
            body=msg)
            notification_item.save()
            
            return HttpResponseRedirect(reverse('hubs:list') )
    """  
    queryset_hubs = Hub.objects.filter(seller_name = request.user.username)
    HUB_CHOICES = []
    for hub_instance in queryset_hubs:
        temp = []
        temp.append(hub_instance.name)
        temp.append(hub_instance.name)
        HUB_CHOICES.append(temp)
    ''' dynamically pass a parameter from the view to the form
        get a list of all hubs of current logged-in user and make a scroll-down list of choices'''
    # form = DeviceCreateForm(HUB_CHOICES)
    """
    form = DeviceCreateForm()
    context = {
        'form' : form,
    }
    return render(request, 'devices/device_create.html', context)

@login_required
def delete_view(request, device_id):
    """ Takes a http request and renders a page for deleting a Device.
        """
    instance = get_object_or_404(Device, id=device_id)
    if not (request.user.username==instance.seller_name):
        context = {'error_message': 'this is not your device to delete'}
        return render(request, 'devices/device_delete_not_allowed.html')
        
    config = SafeConfigParser()
    config.read('/code/config.ini')
    db = MySQLdb.connect(host=config.get('main', 'mysql_host'),  # your host, usually localhost
                 user=config.get('main', 'mysql_name'),  # your username
                 passwd=config.get('main', 'mysql_pw'),  # your password
                 db=config.get('main', 'mysql_db'))  # your database
    cur = db.cursor()
    cur.execute("delete from users where username='{0}'".format(str(instance.name)))
    cur.execute("delete from acls where username='{0}'".format(str(instance.name)))
    
    db.commit()
    subject = 'New device deleted'
    msg = instance.name + ' deleted from ' + instance.hub_name
    email = EmailMessage(subject, msg, to=[request.user.email])
    email.send()

    notification_box = request.user.get_notification_box()
    notification_item = NotificationItem(
    notification_box=notification_box,
    subject=subject,
    body=msg)
    notification_item.save()
    instance.delete()
    return render(request, 'devices/device_delete.html')

# change device password
@login_required
def edit_view(request, device_id):
    """ Takes a http request and renders a page for editing a Device (change password or public key)
        """
    instance = get_object_or_404(Device, id=device_id)
    if not (request.user.username==instance.seller_name):
        context = {'error_message': 'this is not your device'}
        return render(request, 'devices/device_delete_not_allowed.html')
        
    if(request.method == 'GET'):
        form = DeviceEditForm()
        context = {
            'form' : form,
        }
        return render(request, 'devices/device_edit.html', context)
            
    elif (request.method == 'POST'):
        
        form = DeviceEditForm(request.POST)

        if form.is_valid():
            
            config = SafeConfigParser()
            config.read('/code/config.ini')
            db = MySQLdb.connect(host=config.get('main', 'mysql_host'),  # your host, usually localhost
                                 user=config.get('main', 'mysql_name'),  # your username
                                 passwd=config.get('main', 'mysql_pw'),  # your password
                                 db=config.get('main', 'mysql_db'))  # your database

            cur = db.cursor()
            NP_PATH = config.get('main', 'np_path')
            if(form.cleaned_data['rgs_type'] == '1'): # api key, needs hash         
                command = NP_PATH + ' -p ' + form.cleaned_data['password']
                command_bytes = command.encode('utf-8')
                password_bytes = subprocess.Popen(command_bytes, stdout=subprocess.PIPE, shell=True).communicate()[0]
                instance.password = password_bytes.decode().rstrip('\n')
            else: # public key, no hash
                instance.password = form.cleaned_data['password']
            instance.rgs_type = form.cleaned_data['rgs_type']
            
            cur.execute("UPDATE users SET pw='{0}' WHERE username='{1}'".format(instance.password, instance.name));  
            db.commit()
            instance.save()
            return HttpResponseRedirect('/hubs/')
            
        form = DeviceEditForm()
        context = {
            'form' : form,
        }
        return render(request, 'devices/device_edit.html', context)    
