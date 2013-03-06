import datetime
from haystack import indexes
from models import Topic, Message

class TopicIndex(indexes.SearchIndex, indexes.Indexable):
    text        = indexes.CharField(document=True, use_template=True)
    author      = indexes.CharField(model_attr='user')
    created     = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return Topic

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

    def get_updated_field(self):
        return "modified"

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
