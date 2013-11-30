from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

MESSAGE_TYPE_CHOICES = (
    ('s','system'),
    ('a','action'),
    ('m', 'message'),
    ('j','join'),
    ('l','leave'),
    ('n','notification')
)

class Message(models.Model):
    type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES)
    to_user = models.ForeignKey(User, related_name='to_user')
    from_user = models.ForeignKey(User, related_name='from_user')
    message = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.type == 's':
            return u'SYSTEM: %s' % self.message
        if self.type == 'n':
            return u'NOTIFICATION: %s' % self.message
        elif self.type == 'j':
            return 'JOIN: %s' % self.author
        elif self.type == 'l':
            return 'LEAVE: %s' % self.author
        elif self.type == 'a':
            return 'ACTION: %s > %s' % (self.author, self.message)
        return self.message
