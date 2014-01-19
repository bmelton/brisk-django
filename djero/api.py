from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.authentication import Authentication
from django.conf.urls.defaults import url
from tastypie.utils import trailing_slash
from django.conf import settings
from models import Category, Forum, Topic, Message
from django.contrib.auth.models import User

class UserResource(ModelResource):
    class Meta:
        queryset        = User.objects.all()
        resource_name   = 'auth/user'
        excludes        = ['email', 'password', 'is_superuser', 'is_staff']
        authorization   = DjangoAuthorization()
        authentication  = Authentication()

        filtering = {
            'id'        : ALL,
            'username'  : ALL,
            'last_name' : ALL,
        }

    def dehydrate(self, bundle):
        #bundle.data['profile'] = bundle.obj.get_absolute_url()
        bundle.data['moderator'] = True
        return bundle

class CategoryResource(ModelResource):
    class Meta:
        queryset        = Category.objects.filter(active=True).order_by('position')
        resource_name   = 'category'
        authorization   = DjangoAuthorization()
        authentication  = Authentication()

        filtering = {
            'id'        : ALL,
            'slug'      : ALL,
            'category'  : ALL_WITH_RELATIONS,
        }

class ForumResource(ModelResource):
    category            = fields.ToOneField(CategoryResource, 'category', full=True)
    class Meta:
        queryset        = Forum.objects.filter(active=True).order_by('category__position', 'position')
        resource_name   = 'forum'
        authorization   = DjangoAuthorization()
        authentication  = Authentication()

        filtering = {
            'id'        : ALL,
            'slug'      : ALL,
            'category'  : ALL_WITH_RELATIONS,
        }

class TopicResource(ModelResource):
    category            = fields.ToOneField(CategoryResource, 'category', full=True)
    forum               = fields.ToOneField(ForumResource, 'forum', full=True)
    user                = fields.ToOneField(UserResource, 'user', full=True)
    last_user           = fields.ToOneField(UserResource, 'last_user', full=True)
    class Meta:
        queryset        = Topic.objects.filter(active=True).order_by('-modified')
        resource_name   = 'topic'
        authorization   = DjangoAuthorization()
        authentication  = Authentication()

        filtering = {
            'id'        : ALL,
            'slug'      : ALL,
            'forum'     : ALL_WITH_RELATIONS,
            'modified'  : ALL,
        }

    def dehydrate(self, bundle):
        bundle.data['avatar'] = "/static/img/avatars/hobbes.png";
        return bundle

class MessageResource(ModelResource):
    category            = fields.ToOneField(CategoryResource, 'category', full=True)
    forum               = fields.ToOneField(ForumResource, 'forum', full=True)
    topic               = fields.ToOneField(TopicResource, 'topic', full=True)
    user                = fields.ToOneField(UserResource,  'user',  full=True)
    class Meta:
        queryset        = Message.objects.filter(active=True).order_by('-modified')
        resource_name   = 'message'
        authorization   = DjangoAuthorization()
        authentication  = Authentication()

        filtering = {
            'id'        : ALL,
            'category'  : ALL_WITH_RELATIONS,
            'forum'     : ALL_WITH_RELATIONS,
            'topic'     : ALL_WITH_RELATIONS,
            'modified'  : ALL,
        }

