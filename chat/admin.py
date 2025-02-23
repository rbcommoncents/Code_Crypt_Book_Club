from django.contrib import admin
from .models import Topic, Message, Reply

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")
    search_fields = ("title", "description", "created_by__username")
    list_filter = ("created_at",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "created_at")
    search_fields = ("user__username", "content", "topic__title")
    list_filter = ("created_at",)

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at")
    search_fields = ("user__username", "content", "message__topic__title")
    list_filter = ("created_at",)
