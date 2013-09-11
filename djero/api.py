from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from django.conf.urls.defaults import url
from tastypie.utils import trailing_slash

from models import Category, Forum, Topic, Message

class CategoryResource(ModelResource):
    class Meta:
        queryset        = Category.objects.filter(active=True)
        resource_name   = 'category'
        authorization   = DjangoAuthorization()
        authentication  = SessionAuthentication()

        filtering = {
            'id'        : ALL,
            'slug'      : ALL,
            'category'  : ALL_WITH_RELATIONS,
        }

class ForumResource(ModelResource):
    category            = fields.ToOneField(CategoryResource, 'category', full=True)
    class Meta:
        queryset        = Forum.objects.filter(active=True)
        resource_name   = 'forum'
        authorization   = DjangoAuthorization()
        authentication  = SessionAuthentication()

        filtering = {
            'id'        : ALL,
            'slug'      : ALL,
            'category'  : ALL_WITH_RELATIONS,
        }

class TopicResource(ModelResource):
    category            = fields.ToOneField(CategoryResource, 'category', full=True)
    forum               = fields.ToOneField(ForumResource, 'forum', full=True)
    class Meta:
        queryset        = Topic.objects.filter(active=True)
        resource_name   = 'topic'
        authorization   = DjangoAuthorization()
        authentication  = SessionAuthentication()

        filtering = {
            'id'        : ALL,
            'slug'      : ALL,
            'forum'     : ALL_WITH_RELATIONS,
        }

class MessageResource(ModelResource):
    topic               = fields.ToOneField(TopicResource, 'topic', full=True)
    class Meta:
        queryset        = Message.objects.filter(active=True)
        resource_name   = 'message'
        authorization   = DjangoAuthorization()
        authentication  = SessionAuthentication()

        filtering = {
            'id'        : ALL,
            'category'  : ALL_WITH_RELATIONS,
            'forum'     : ALL_WITH_RELATIONS,
            'topic'     : ALL_WITH_RELATIONS,
        }

