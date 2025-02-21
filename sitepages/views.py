from django.http import FileResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.conf import settings
import os
import boto3
from rest_framework import viewsets
from .models import Drink, Song
from .forms import SongUploadForm
from .serializers import DrinkSerializer, SongSerializer
from accounts.models import CustomUser
from django.urls import reverse_lazy
from django.contrib import messages


def landing_page(request):
    return render(request, 'site/landing.html')


# Drinks Models
class DrinkListView(ListView):
    model = Drink
    template_name = 'site/drink_list.html'
    context_object_name = 'drinks'
    ordering = ['category', 'name']

class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer


# Profile/Bio Models
class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "site/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user  

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["phone_number", "profile_picture"] 
    template_name = "site/profile_edit.html"
    success_url = reverse_lazy("profile_view")

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

    def get_object(self):
        return self.request.user

# Music and Songs Models
class SongListView(ListView):
    model = Song
    template_name = "site/song_list.html"
    context_object_name = "songs"

    def get_queryset(self):
        queryset = super().get_queryset()
        for song in queryset:
            song.local_url = self.get_song_url(song)
        return queryset

    def get_song_url(self, song):

        local_path = os.path.join(settings.MEDIA_ROOT, "temp_music", os.path.basename(song.audio_file.name))

        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

        if not os.path.exists(local_path):  # Only download if it doesn't exist
            s3_client = boto3.client("s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            s3_client.download_file(settings.AWS_STORAGE_BUCKET_NAME, song.audio_file.name, local_path)

        return reverse("serve_local_song", args=[song.id])

class SongUploadView(LoginRequiredMixin, CreateView):
    model = Song
    form_class = SongUploadForm
    template_name = "site/song_upload.html"
    success_url = reverse_lazy("song_list")

def serve_local_song(request, song_id):

    song = get_object_or_404(Song, id=song_id)
    local_path = os.path.join(settings.MEDIA_ROOT, "temp_music", os.path.basename(song.audio_file.name))

    try:
        return FileResponse(open(local_path, "rb"), content_type="audio/mpeg")
    except FileNotFoundError:
        raise Http404("Song file not found.")

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
