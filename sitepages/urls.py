from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    rate_drink, rate_song, serve_local_video, serve_local_song, landing_page,
    DrinkListView, ProfileView, ProfileEditView, SongListView, SongUploadView,
    DrinkViewSet, SongViewSet, ArtListView, ArtDetailView, ArtViewSet, ArtCreateView
)
from . import views
from django.conf import settings
from django.conf.urls.static import static

# API Router for Django REST Framework
router = DefaultRouter()
router.register(r"drinks", DrinkViewSet)
router.register(r"songs", SongViewSet)
router.register(r"art", ArtViewSet)

urlpatterns = [
    # API Endpoints
    path("api/", include(router.urls)), 

    # Frontend Views (HTML Pages)
    path("", landing_page, name="landing"),
    path("videos/welcome.mp4", serve_local_video, name="serve_local_video"),

    # Drinks
    path("drinks/", DrinkListView.as_view(), name="drink_list"),
    path("drinks/rate/<int:drink_id>/", views.rate_drink, name="rate_drink"),

    # User Profiles
    path("profile/", ProfileView.as_view(), name="profile_view"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),

    # Music
    path("music/", SongListView.as_view(), name="song_list"),
    path("music/rate/<int:song_id>/", views.rate_song, name="rate_song"),
    path("music/upload/", SongUploadView.as_view(), name="song_upload"),
    path("music/play/<int:song_id>/", serve_local_song, name="serve_local_song"),

    # Art
    path("art/", ArtListView.as_view(), name="art_list"), 
    path("art/<int:pk>/", ArtDetailView.as_view(), name="art_detail"), 
    path("art/upload/", ArtCreateView.as_view(), name="art_create"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
