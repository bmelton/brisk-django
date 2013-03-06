from django.db import models
from models import *

class ForumManager(models.Manager):
    def moderators(self, model):
        qs = Moderator.objects.filter(forum=self.pk)
        return qs
