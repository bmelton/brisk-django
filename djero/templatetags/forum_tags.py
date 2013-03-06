from django import template
from django.core.urlresolvers import reverse

from forum.models import Message, Topic, Category
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
import datetime

register = template.Library()

class UserCountNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        users = User.objects.filter(is_active=True).count()
        return users-1

class TopicCountNode(template.Node):
    def render(self, context):
        topics = Topic.objects.filter(active=False).count()
        return topics

class MessageCountNode(template.Node):
    def render(self, context):
        messages = Message.objects.filter(active=True).count()
        return messages

@register.tag
def user_count(parser, token):
    return UserCountNode()

@register.tag
def topic_count(parser, token):
    return TopicCountNode()

@register.tag
def message_count(parser, token):
    return MessageCountNode()

@register.tag
def is_moderator(parser, token):
    bits = token.contents.split()
    if len(bits) <= 2:
        raise TemplateSyntaxError, "is_moderator needs a forum and user"
    return IsModerator(bits[1], bits[2])

@register.filter
def is_moderator_of(user, forum):
    try: 
        mod = forum.moderator_set.filter(user=user).count()
        print mod
        return mod == 1
    except Exception:
        return False

@register.filter
def is_in_group_for_category(user, category):
    if user.is_superuser == True:
        return True
    try: 
        category = Category.objects.get(pk=category.pk)
        category_groups = category.groups.all()
        if len(category_groups) == 0:
            return True
        passes = False
        for user_group in user.groups.all():
            print user_group
            if user_group in category_groups:
                passes = True
                return True
        return passes
    except Exception, e:
        print str(e)
        return False

@register.filter
def can_see_category(user, category):
    passes = True
    anon = user.is_anonymous()

    if user.is_superuser == True:
        return True
    if category.require_logged_in and anon:
        return False
    return passes

@register.filter
def can_see_forum(user, forum):
    passes = True
    anon = user.is_anonymous()

    if user.is_superuser == True:
        return True
    if forum.require_logged_in and anon:
        return False
    return passes
