from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.
class Flow(models.Model):
    """
        Model that represents the flow of data for a topic
        
        Flow(id, user, topic, direction, state)
        """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    topic = models.CharField(blank=True, max_length=64)
    direction = models.CharField(blank=True, max_length=64)
    state = models.CharField(blank=True, max_length=64)

    def __unicode__(self):
        return "%s" % (self.id)
