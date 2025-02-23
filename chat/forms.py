from django import forms
from .models import Topic, Message, Reply

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "description"]

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["content"]
