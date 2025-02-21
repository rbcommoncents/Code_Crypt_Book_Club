from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import serve_local_song, landing_page, DrinkListView, ProfileView, ProfileEditView, SongListView, SongUploadView, DrinkViewSet, SongViewSet

router = DefaultRouter()
router.register(r'drinks', DrinkViewSet)
router.register(r'songs', SongViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("", landing_page, name="landing"),
    path('drinks/', DrinkListView.as_view(), name='drink_list'),
    path("profile/", ProfileView.as_view(), name="profile_view"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("music/", SongListView.as_view(), name="song_list"),
    path("music/upload/", SongUploadView.as_view(), name="song_upload"),
    path("music/play/<int:song_id>/", serve_local_song, name="serve_local_song"),
]