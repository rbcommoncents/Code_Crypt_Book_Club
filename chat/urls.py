from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, MessageViewSet, ReplyViewSet, topic_list, topic_create, topic_detail, message_create, reply_create

# Separate namespace for frontend views
app_name = "chat"

# API Router for Django REST Framework
router = DefaultRouter()
router.register(r"topics", TopicViewSet, basename="topic")
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"replies", ReplyViewSet, basename="reply")

urlpatterns = [
    # Frontend Views (HTML Pages)
    path("", topic_list, name="topic_list"),
    path("create/", topic_create, name="topic_create"),
    path("<int:topic_id>/", topic_detail, name="topic_detail"),
    path("<int:topic_id>/message/", message_create, name="message_create"),
    path("message/<int:message_id>/reply/", reply_create, name="reply_create"),
]

# Separate API URL patterns
api_urlpatterns = [
    path("", include(router.urls)), 
]
