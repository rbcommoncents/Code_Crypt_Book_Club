from rest_framework import serializers
from .models import Topic, Message, Reply

class TopicSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Topic
        fields = ["id", "title", "description", "created_by", "created_at"]

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())

    class Meta:
        model = Message
        fields = ["id", "topic", "user", "content", "created_at"]

class ReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    message = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all())

    class Meta:
        model = Reply
        fields = ["id", "message", "user", "content", "created_at"]
