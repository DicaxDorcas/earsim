from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Room(models.Model):
    user_list = models.ManyToManyField(User)

    def __add_message(self, type, sender, message=None):
        '''Generic function for adding a message to the chat room'''
        m = Message(room=self, type=type, author=sender, message=message)
        m.save()
        return m

    def say(self, sender, message):
        '''Say something in to the chat room'''
        return self.__add_message('m', sender, message)

    def join(self, user):
        return self.__add_message('j', user)

    def leave(self, user):
        return self.__add_message('l', user)

    def messages(self, after_pk=None, after_date=None):
        m = Message.objects.filter(room=self)
        if after_pk:
            m = m.filter(pk__gt=after_pk)
        if after_date:
            m = m.filter(timestamp__gte=after_date)
        return m.order_by('pk')

    def last_message_id(self):
        m = Message.objects.filter(room=self).order_by('-pk')
        if m:
            return m[0].id
        else:
            return 0

    def __unicode__(self):
        return 'Chat in UserGroup: %d' % (self.user_group.id)

MESSAGE_TYPE_CHOICES = (
    ('s','system'),
    ('a','action'),
    ('m', 'message'),
    ('j','join'),
    ('l','leave'),
    ('n','notification')
)

class Message(models.Model):
    room = models.ForeignKey(Room)
    type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES)
    author = models.ForeignKey(User, related_name='author', blank=True, null=True)
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
