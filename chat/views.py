from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from .models import Topic, Message, Reply
from .forms import TopicForm, MessageForm, ReplyForm
from .serializers import TopicSerializer, MessageSerializer, ReplySerializer


def topic_list(request):
    query = request.GET.get("q", "")
    topics = Topic.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, "chat/topic_list.html", {"topics": topics, "query": query})

@login_required
def topic_create(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.save()
            return redirect("chat:topic_list")
    else:
        form = TopicForm()
    
    return render(request, "chat/topic_create.html", {"form": form})

def topic_detail(request, topic_id):
    """View a topic and its messages."""
    topic = get_object_or_404(Topic, id=topic_id)
    messages = topic.messages.all()
    return render(request, "chat/topic_detail.html", {"topic": topic, "messages": messages})

@login_required
def message_create(request, topic_id):
    """Post a message within a topic."""
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.topic = topic
            message.save()
            return redirect("chat:topic_detail", topic_id=topic.id)
    else:
        form = MessageForm()
    
    return render(request, "chat/message_create.html", {"form": form, "topic": topic})

@login_required
def reply_create(request, message_id):
    """Reply to a message."""
    message = get_object_or_404(Message, id=message_id)

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.message = message
            reply.save()
            return redirect("chat:topic_detail", topic_id=message.topic.id)
    else:
        form = ReplyForm()
    
    return render(request, "chat/reply_create.html", {"form": form, "message": message})

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by("-created_at")
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Require authentication to create

    def perform_create(self, serializer):
        """Automatically set 'created_by' field from the authenticated user."""
        serializer.save(created_by=self.request.user)
        
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("-created_at")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Auto-assign the logged-in user to the message"""
        serializer.save(user=self.request.user)

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all().order_by("-created_at")
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Auto-assign the logged-in user to the reply"""
        serializer.save(user=self.request.user)