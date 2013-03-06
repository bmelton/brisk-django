from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',                                          'forum.views.index',        name='forum_home'),
    url(r'^(?P<category>[-\w]+)/$',                     'forum.views.category',     name='forum_category_home'),
    url(r'^subscribe_topic/(?P<topic>[-\w]+)/$',        'forum.views.subscribe_topic',    
                                                                                    name='forum_subscribe_topic'),
    url(r'^subscribe_forum/(?P<topic>[-\w]+)/$',        'forum.views.subscribe_forum',    
                                                                                    name='forum_subscribe_forum'),
    url(r'^topic/new/(?P<forum>[-\w]+)/$',              'forum.views.create_topic', name='forum_create_topic'),
    url(r'^topic/reply/(?P<topic>[-\w]+)/$',            'forum.views.reply',        name='forum_reply'),
    url(r'^(?P<category>[-\w]+)/(?P<forum>[-\w]+)/$',   'forum.views.forum',        name='forum_board_home'),
    url(r'^topic/(?P<topic>[-\w]+)/edit/delete$',       'forum.views.delete_topic', name='forum_delete_topic'),
    url(r'^topic/(?P<topic>[-\w]+)/edit/$',             'forum.views.edit_topic',   name='forum_edit_topic'),
    url(r'^(?P<category>[-\w]+)/(?P<forum>[-\w]+)/(?P<topic>[-\w]+)/$',   
                                                        'forum.views.topic',        name='forum_topic_home'),
)
