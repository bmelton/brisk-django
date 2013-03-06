from django import forms
from models import Topic, Message

"""
class TopicForm(forms.Form):
    title       = forms.CharField()
    category    = forms.HiddenInput()
    forum       = forms.HiddenInput()
    title       = forms.CharField()
    # slug        = forms.CharField(null=True, blank=True)
    sticky      = forms.CheckboxInput()
    user        = forms.HiddenInput()
    text        = forms.CharField(widget=forms.Textarea)
"""

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('user', 'category', 'forum', 'last_user', 'message', 'last_message', 'sticky', 'reply_count',
        'view_count', 'locked', 'active', 'created', 'responded_to', 'modified', 'slug')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('category', 'forum', 'topic', 'user', 'created', 'modified', 'active')
