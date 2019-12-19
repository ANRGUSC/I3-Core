from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class NotificationBox(models.Model):
    """
        Defines one to one relationship with the user, and data and methods regarding notifications
        
        NotificationBox(id, user, timestamp, updated)
        """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=False, blank=True, related_name="notification_box")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def num_unread(self):
        return self.notifications.filter(read=False, archived=False).count()

    def get_all(self):
        return self.notifications.all()

    def get_unarchived(self):
        return self.notifications.filter(archived=False).order_by('-timestamp')

    def __unicode__(self):
        return str(self.user.username)


class NotificationItem(models.Model):
    """
        Model for one item in notification box
        
        NotificationItem(id, notification_box, timestamp, subject, body, read, archived)
        """
    notification_box = models.ForeignKey(NotificationBox, related_name='notifications')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    subject = models.CharField(blank=True, max_length=64)
    body = models.TextField(blank=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def belongs_to_user(self, user):
        return self.notification_box.user == user

    def __unicode__(self):
        return "%s - %s" % (self.subject, self.body)
