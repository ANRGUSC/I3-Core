import os
import random
import string
import shutil
import subprocess
from configparser import SafeConfigParser

import MySQLdb
from PIL import Image
from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.db.models import PositiveSmallIntegerField
from notifications.models import NotificationItem
from flows.models import Flow
from django.utils.translation import ugettext_lazy as _
from devices.models import Device

# NP_PATH = '/home/zxc/Desktop/frontend/src/np'

def download_media_location(instance, filename):
    return "%s/%s" % (instance.slug, filename)


SENSOR = (1, 'Sensor')
ACTUACTOR= (2, 'Actuactor')
BOTH = (3, 'Both')


class Product(models.Model):
    """
        Defines the basic data structure for a product
        
        Product(id, seller, hub, media, title, slug, restricted_active, sensor_type, description, price, sale_active, sale_price)
        """
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='selling_products_set', on_delete=models.CASCADE)
    hub = models.CharField(max_length=80)
    media = models.ImageField(blank=True, null=True,
                              upload_to=download_media_location,
                              storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    title = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, unique=True)
    restricted_active = models.BooleanField(default=False)
    sensor_type = PositiveSmallIntegerField(_("sensor type"), choices=(BOTH, ACTUACTOR, SENSOR), default=SENSOR[0])
    description = models.TextField()
    price = models.DecimalField(max_digits=65, decimal_places=2, default=9.99, null=True, )  # 100.00
    sale_active = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=65,
                                     decimal_places=2, default=6.99, null=True, blank=True)  # 100.00
    longitude = models.DecimalField(max_digits=65,
                                     decimal_places=4, null=True, blank=True)
    latitude = models.DecimalField(max_digits=65,
                                     decimal_places=4, null=True, blank=True)
    def __unicode__(self):  # def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """ returns url for detail view of product
            """
        view_name = "products:detail_slug"
        return reverse(view_name, kwargs={"slug": self.slug})

    def get_edit_url(self):
        """ returns url for product edit view
            """
        view_name = "sellers:product_edit"
        return reverse(view_name, kwargs={"pk": self.id})

    def get_download(self):
        """ returns url for download
            """
        view_name = "products:download_slug"
        url = reverse(view_name, kwargs={"slug": self.slug})
        return url

    @property
    def get_price(self):
        if self.sale_price and self.sale_active:
            return self.sale_price
        return self.price

    def get_html_price(self):
        price = self.get_price
        if price == self.sale_price:
            return "<p><span>%s</span> <span style='color:red;text-decoration:line-through;'>%s</span></p>" % (
                self.sale_price, self.price)
        else:
            return "<p>%s</p>" % (self.price)

    def add_to_cart(self):
        """ Called by cart view when adding porduct to cart. Returns url of cart and product id.
            """
        return "%s?item=%s&qty=1" % (reverse("cart"), self.id)

    def remove_from_cart(self):
        """ Called by cart view when deleting porduct from cart. Returns url of cart and product id.
            """
        return "%s?item=%s&qty=1&delete=True" % (reverse("cart"), self.id)

    def get_title(self):
        return "%s" % self.title

    def get_seller_username(self):
        return self.seller.username

    """
    get thumbails, instance.thumbail_set.all()
    """


def create_slug(instance, new_slug=None):
    """ function create_slug will generate a slug from title of product, or return a slug passed as an argument
        """
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


# Authorization process for broker
def process_authorization(instance):
    """ Authorization process for broker is a plug-in
        """
    config = SafeConfigParser()
    config.read('/code/config.ini')
    db = MySQLdb.connect(host=config.get('main', 'mysql_host'),  # your host, usually localhost
                         user=config.get('main', 'mysql_name'),  # your username
                         passwd=config.get('main', 'mysql_pw'),  # your password
                         db=config.get('main', 'mysql_db'))  # your database

    cur = db.cursor()
    username = instance.seller.username
    user_email = instance.seller.email
    topic = instance.title
    """
    IMPORTANT LOGIC when creating a topic
    This part is only for creating a product
    NO extra credential will be assigned to the seller
    creating a product has nothing to do with authentication
    extract all devices inside the same hub with this product
    """
    flow_obj = Flow.objects.create(
        user=instance.seller,
        topic=topic,
        direction='out',
        state='inactive')
    flow_obj.save()

    # send to the user which topic is able to pub/sub
    subject = 'New product added'
    msg = topic + ' created inside ' + instance.hub
    email = EmailMessage(subject, msg, to=[user_email])
    email.send()

    # Record email as notification
    notification_box = instance.seller.get_notification_box()
    notification_item = NotificationItem(
        notification_box=notification_box,
        subject=subject,
        body=msg)
    notification_item.save()

    queryset_device = Device.objects.filter(hub_name = instance.hub)
    # insert into acls table
    rw = 2  # seller: can read and write
    
    for d in queryset_device:
        cur.execute("insert into acls (username,topic,rw,user_id,topic_id) values (%s,%s,%s,%s,%s)",(d.name, topic, str(rw), instance.seller.id, instance.id))
    db.commit()


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    """ If there is no slug entered in the slug field at the time a product is being saved into the database, this function will automatically create one using create_slug()
        """
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def thumbnail_location(instance, filename):
    """ returns a string with filename and slug
        """
    return "%s/%s" % (instance.product.slug, filename)


THUMB_CHOICES = (
    ("hd", "HD"),
    ("sd", "SD"),
    ("micro", "Micro"),
)


class Thumbnail(models.Model):
    """
        thumbnail: media pics
        
        Defines a model for a thumbnail
        
        Thumbnail(id, product, type, height, width, media)
        """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # instance.product.title  # instance.product.title
    type = models.CharField(max_length=20, choices=THUMB_CHOICES, default='hd')
    height = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(
        width_field="width",
        height_field="height",
        blank=True,
        null=True,
        upload_to=thumbnail_location)

    def __unicode__(self):  # __str__(self):
        return str(self.media.path)


def create_new_thumb(media_path, instance, owner_slug, max_length, max_width):
    """ sets the media field of thumbnail object using arguments
        """
    filename = os.path.basename(media_path)
    thumb = Image.open(media_path)
    size = (max_length, max_width)
    thumb.thumbnail(size, Image.ANTIALIAS)
    temp_loc = "%s/%s/tmp" % (settings.MEDIA_ROOT, owner_slug)
    if not os.path.exists(temp_loc):
        os.makedirs(temp_loc)
    temp_file_path = os.path.join(temp_loc, filename)
    if os.path.exists(temp_file_path):
        temp_path = os.path.join(temp_loc, "%s" % (random.random()))
        os.makedirs(temp_path)
        temp_file_path = os.path.join(temp_path, filename)

    temp_image = open(temp_file_path, "wb")
    thumb.save(temp_image)
    thumb_data = open(temp_file_path, "rb")

    thumb_file = File(thumb_data)
    instance.media.save(filename, thumb_file)
    shutil.rmtree(temp_loc, ignore_errors=True)
    return True


def product_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.media:
        hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
        sd, sd_created = Thumbnail.objects.get_or_create(product=instance, type='sd')
        micro, micro_created = Thumbnail.objects.get_or_create(product=instance, type='micro')

        hd_max = (500, 500)
        sd_max = (350, 350)
        micro_max = (150, 150)

        media_path = instance.media.path
        owner_slug = instance.slug
        if hd_created:
            create_new_thumb(media_path, hd, owner_slug, hd_max[0], hd_max[1])

        if sd_created:
            create_new_thumb(media_path, sd, owner_slug, sd_max[0], sd_max[1])

        if micro_created:
            create_new_thumb(media_path, micro, owner_slug, micro_max[0], micro_max[1])

    process_authorization(instance)


post_save.connect(product_post_save_receiver, sender=Product)

class ProductRating(models.Model):
    """
        Defines a model representing one product rating by one user
        
        ProductRating(id, user, product, rating, verified)
        """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.rating

