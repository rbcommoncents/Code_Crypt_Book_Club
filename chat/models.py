from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Topic(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topics")

    def __str__(self):
        return self.title

class Message(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user} on {self.topic}"

class Reply(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user} on {self.message.topic}"
