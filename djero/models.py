from django.db import models
from managers import ForumManager
from django.contrib.auth.models import User, Group
from uuslug import uuslug
import datetime

class Category(models.Model):
    groups              = models.ManyToManyField(Group, null=True, blank=True)
    name                = models.CharField(max_length=255, null=False, blank=False)
    slug                = models.CharField(max_length=255, null=True, blank=True)
    image               = models.URLField(max_length=255, null=True, blank=True)
    description         = models.TextField(null=True, blank=True)
    position            = models.PositiveSmallIntegerField("Position", null=True, blank=True)
    collapsible         = models.BooleanField(default=True)
    active              = models.BooleanField(default=False)
    require_logged_in   = models.BooleanField(default=False)

    class Meta():
        ordering = ['position']
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.name, instance=self)
        super(Category, self).save(*args, **kwargs)

class Forum(models.Model):
    groups              = models.ManyToManyField(Group, null=True, blank=True)
    name                = models.CharField(max_length=255, null=False, blank=False)
    slug                = models.CharField(max_length=255, null=True, blank=True)
    description         = models.TextField()
    category            = models.ForeignKey(Category)
    order               = models.IntegerField(null=True, blank=True)
    position            = models.IntegerField(null=True, blank=True)
    created             = models.DateTimeField(null=True, blank=True)
    last_updated        = models.DateTimeField(null=False, blank=False)
    topic_count         = models.IntegerField(null=True, blank=True, default=0)
    message_count       = models.IntegerField(null=True, blank=True, default=0)
    activate            = models.BooleanField(default=False)

    class Meta():
        ordering = ['position']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.now()
            self.slug = uuslug(self.name, instance=self)
        super(Forum, self).save(*args, **kwargs)

    def is_moderator(self, *args, **kwargs):
        if kwargs:
            if "user_id" in kwargs:
                mod = self.moderator_set.filter(user__id=kwargs["user_id"]).count()
                return mod == 1
        return False

class Moderator(models.Model):
    user                = models.ForeignKey(User)
    forum               = models.ForeignKey(Forum)

    def __unicode__(self):
        return self.user.username

class ActiveTopicManager(models.Manager):
    def get_query_set(self):
            return super(ActiveTopicManager, self).get_query_set().filter(active=True)

class Topic(models.Model):
    category            = models.ForeignKey(Category, null=True, blank=True)
    forum               = models.ForeignKey(Forum)
    title               = models.CharField(max_length=255, null=False, blank=False)
    slug                = models.CharField(max_length=255, null=True, blank=True)
    sticky              = models.BooleanField(default=False)
    user                = models.ForeignKey(User, related_name='user')
    last_user           = models.ForeignKey(User, related_name='last_user')
    message             = models.ForeignKey('Message', related_name='message', null=True, blank=True)
    last_message        = models.ForeignKey('Message', related_name='last_message', null=True, blank=True)
    reply_count         = models.IntegerField(default=0)
    view_count          = models.IntegerField(default=0)
    locked              = models.BooleanField(default=False)
    active              = models.BooleanField(default=False)
    created             = models.DateTimeField(null=True, blank=True)
    responded_to        = models.DateTimeField(null=True, blank=True)
    modified            = models.DateTimeField(null=True, blank=True)
    # objects             = ActiveTopicManager()
    # all_objects         = models.Manager()
    objects             = models.Manager()

    class Meta():
        get_latest_by   = 'created'
        ordering        = ['created']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.title, instance=self)
            self.created = datetime.datetime.now()
        else:
            self.modified = datetime.datetime.now()
        super(Topic, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('forum_topic_home', [self.category.slug, self.forum.slug, self.slug])

class Message(models.Model):
    category            = models.ForeignKey(Category)
    forum               = models.ForeignKey(Forum)
    topic               = models.ForeignKey(Topic, related_name='topic_messages')
    user                = models.ForeignKey(User)
    text                = models.TextField()                
    created             = models.DateTimeField(null=True, blank=True)
    modified            = models.DateTimeField(null=True, blank=True)
    active              = models.BooleanField(default=True)

    class Meta():
        ordering = ['created']

    def __unicode__(self):  
        return "%s : %s" % (self.user.username, self.topic.title)

    def save(self, *args, **kwargs):
        if not self.id:
            # self.slug = uuslug(self.title, instance=self)
            self.created = datetime.datetime.now()
        else:
            self.modified = datetime.datetime.now()
        super(Message, self).save(*args, **kwargs)
