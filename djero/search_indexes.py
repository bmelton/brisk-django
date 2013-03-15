import datetime
from haystack import indexes
from models import Topic, Message
from guardian.shortcuts import get_groups_with_perms

class TopicIndex(indexes.SearchIndex, indexes.Indexable):
    text        = indexes.CharField(document=True, use_template=True)
    author      = indexes.CharField(model_attr='user')
    created     = indexes.DateTimeField(model_attr='created')
    group_access= indexes.MultiValueField()

    def get_model(self):
        return Topic

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

    def get_updated_field(self):
        return "modified"

    def prepare_group_access(self, obj):
        groups = []
        groups_with_access = obj.get_allowed_groups()
        for group in groups_with_access:
            groups.append(group.id)
        return groups

class MessageIndex(indexes.SearchIndex, indexes.Indexable):
    text        = indexes.CharField(document=True, use_template=True)
    author      = indexes.CharField(model_attr='user')
    created     = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Message

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

    def get_updated_field(self):
        return "modified"
