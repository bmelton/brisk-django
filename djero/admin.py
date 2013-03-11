from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from models import *

class ForumAdmin(GuardedModelAdmin):
    class Media:
        js = (
            'admin/js/admin_list_reorder.js',
        )

    model = Forum
    list_display = ('category', 'name','created','last_updated','position',)
    list_display_links = ('category',)
    list_editable = ('position',)
    list_filter = ('category',)
    search_fields = ['title',]

# class CategoryAdmin(admin.ModelAdmin):
class CategoryAdmin(GuardedModelAdmin):
    def changelist_view(self, request, extra_context=None):
        test = request.META.get('HTTP_REFERER')
        # test = request.META['HTTP_REFERER'].split(request.META['PATH_INFO'])
        if test:
            test = test.split(request.META.get('PATH_INFO'))
            if test[-1] and not test[-1].startswith('?'):
                if not request.GET.has_key('active__exact'):
                    q = request.GET.copy()
                    q["active__exact"] = 1
                    request.GET = q
                    request.META['QUERY_STRING'] = request.GET.urlencode()
        else:
            if not request.GET.has_key('active__exact'):
                q = request.GET.copy()
                q["active__exact"] = 1
                request.GET = q
                request.META['QUERY_STRING'] = request.GET.urlencode()
            
        return super(CategoryAdmin, self).changelist_view(request, extra_context=extra_context)

    class Media:
        js = (
            'admin/js/admin_list_reorder.js',
        )

    model = Category
    
    list_display    = ('name', 'position',)
    list_editable   = ('position',)
    list_filter     = ('active',)

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('category', 'forum', 'topic', 'user','text',)
    list_filter = ('category', 'forum', 'user', )
    list_display_links = ('text',)
    search_fields = ['user__username','text',]

class TopicAdmin(GuardedModelAdmin):
    model = Topic
    list_display = ('category', 'forum', 'user', 'message','created','modified',)
    list_filter = ('category', 'forum', 'user', )
    search_fields = ['user__username', 'message',]

class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'forum')
    list_filter = ('forum',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Moderator, ModeratorAdmin)
