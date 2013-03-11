from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from models import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from forms import TopicForm, MessageForm
from django.db.models import F
from actstream import action
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime
from guardian.shortcuts import get_objects_for_user

def index(request):
    # categories = Category.objects.prefetch_related('forum_set').all().order_by('position')
    categories = get_objects_for_user(request.user, ['djero.view_category'])
    categories.prefetch_related('forum_set').order_by('position')
    return render(request, "forum/index.html", {
        "categories"    : categories,
    })

def subscribe_topic(request, topic):
    return HttpResponse("Does not exist yet.")

def subscribe_forum(request, forum):
    return HttpResponse("Does not exist yet.")

def category(request, category):
    category = Category.objects.get(slug=category)
    forums   = Forum.objects.select_related('Moderator').filter(category=category)
    return render(request, "forum/category.html", {
        "category"      : category,
        "forums"        : forums,
    })

def forum(request, category, forum):
    forum = Forum.objects.select_related('Moderator').get(slug=forum)
    topics = Topic.objects.filter(forum=forum).order_by('-responded_to')
    page = request.GET.get('page')
    paginator = Paginator(topics, 20)

    try: 
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics  = paginator.page(1)
    except EmptyPage:
        topics  = paginator.page(paginator.num_pages)



    return render(request, "forum/forum.html", {
        "forum"         : forum,
        "topics"        : topics,
    })

def topic(request, category, forum, topic):
    topic = get_object_or_404(Topic, slug=topic)
    messages = Message.objects.filter(topic=topic)[1:]
    messageset = Message.objects.filter(topic=topic)[1:]

    page = request.GET.get('page')    
    paginator = Paginator(messageset, 10)

    try:        
        messages = paginator.page(page)    
    except PageNotAnInteger:        
        messages = paginator.page(1)    
    except EmptyPage:        
        messages = paginator.page(paginator.num_pages)

    return render(request, "forum/topic.html", {
        "topic"         : topic,
        "messages"      : messages,
        "messageset"    : messageset,
        "paginator"     : paginator,
    })

def delete_topic(request, topic):
    topic = get_object_or_404(Topic.objects.select_related(), slug=topic)
    forum = topic.forum
    topic.active = False
    for message in topic.topic_messages.all():
        message.active = False
        message.save()
    topic.save()
    return HttpResponseRedirect(reverse('djero.views.topic', kwargs={
        'category'  : forum.category.slug,
        'forum'     : forum.slug,
        'topic'     : topic.slug,
    }))

def edit_topic(request, topic):
    topic = get_object_or_404(Topic, slug=topic)
    topic_form      = TopicForm(instance=topic)
    message_form    = MessageForm(instance=topic.message)
    return render(request, "forum/edit_topic.html", {
        "topic"         : topic,
        "topic_form"    : topic_form,
        "message_form"  : message_form,
    })

@login_required
def create_topic(request, forum):
    forum = Forum.objects.select_related('Moderator').get(slug=forum)
    if request.method == "POST":
        topic_form      = TopicForm(request.POST, instance=Topic())
        message_form    = MessageForm(request.POST, instance=Message())
        if topic_form.is_valid():
            if message_form.is_valid():
                topic = topic_form.save(commit=False)
                topic.category    = forum.category
                topic.forum       = forum
                topic.user        = request.user
                topic.last_user   = request.user
                topic.save()
                message = message_form.save(commit=False)
                message.category    = forum.category
                message.forum       = forum
                message.topic       = topic
                message.user        = request.user
                message.save()
                topic.message = message
                topic.last_message = message
                topic.save()
                action.send(request.user, verb='created a topic', target=topic)
                return HttpResponseRedirect(reverse('djero.views.topic', kwargs={
                    'category'  : forum.category.slug,
                    'forum'     : forum.slug,
                    'topic'     : topic.slug,
                }))
        else:
            return HttpResponse(topic_form.errors)
    else:
        topic_form      = TopicForm()
        message_form    = MessageForm()
        return render(request, "forum/create_topic.html", {
            "forum"         : forum,
            "topic_form"    : topic_form,
            "message_form"  : message_form,
        })

@login_required
def reply(request, topic):
    if request.method == "POST":
        message_form = MessageForm(request.POST, instance=Message())
        topic = Topic.objects.get(slug=topic)
        if message_form.is_valid():
            message             = message_form.save(commit=False)
            message.category    = topic.forum.category
            message.topic       = topic
            message.forum       = topic.forum
            message.user        = request.user
            message.save()
            action.send(request.user, verb='replied to', target=message.topic)
            message.topic.responded_to = datetime.datetime.now()
            message.topic.save()

            Topic.objects.filter(id=topic.id).update(reply_count=F('reply_count')+1)
            return HttpResponseRedirect(reverse('djero.views.topic', kwargs={
                'category'  : topic.forum.category.slug, 
                'forum'     : topic.forum.slug, 
                'topic'     : topic.slug
            }))
        else:
            return HttpResponse("Invalid")
    else:
        message_form = MessageForm()
        topic = get_object_or_404(Topic, slug=topic)
        return render(request, "forum/reply.html", {
            "message_form"  : message_form,
            "topic"         : topic,
        })
