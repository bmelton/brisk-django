import logging
logger = logging.getLogger('djero')

from django.core.signals import request_finished
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import datetime
from django.dispatch.dispatcher import Signal
from voting.models import *
from django.contrib.auth.models import User, Group

# Listen for user creation, then add to the everybody Group
@receiver(post_save, sender=User, dispatch_uid='listen_to_article')
def listen_to_article(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(name="Everybody")

"""
@receiver(post_save, sender=Vote, dispatch_uid='listen_to_votes')
def listen_to_vote(sender, instance, created, **kwargs):
    if created:
        if instance.content_type == CONTENT_TYPE:
            # This vote is being applied to a djig article.
            article = Article.objects.get(pk=instance.object_id)
            logger.debug(article.love_count)
            # We don't want the initial vote to count for too much.
            same_user = instance.user == article.user
            if same_user:
                Article.objects.filter(pk=instance.object_id).update(love_count=F('love_count') + 1)
                logger.debug("Submission user vote - incremented by 1.")
            else:
                Article.objects.filter(pk=instance.object_id).update(love_count=F('love_count') + 2)
                logger.debug("Different user vote - incremented by 2.")
    else:
        logger.debug("DJIG_SIGNALS: Vote was edited or rescinded")

@receiver(comment_was_posted, sender=Comment, dispatch_uid='listen_to_comments')
def listen_to_comment(sender, comment, request, **kwargs):
    if comment.content_type == CONTENT_TYPE:
        logger.debug("This is a new comment on a Djig article")
        article = Article.objects.get(pk=comment.object_pk)
        same_user = comment.user == article.user
        if same_user:
            Article.objects.filter(pk=comment.object_pk).update(love_count=F('love_count') + 1)
            logger.debug("Comment by same user - incremented by 1.")
        else:
            Article.objects.filter(pk=comment.object_pk).update(love_count=F('love_count') + 2)
            logger.debug("Comment by non-submission user - incremented by 2.")

"""
