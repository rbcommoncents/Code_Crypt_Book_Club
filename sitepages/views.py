from django.http import FileResponse, Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
import os
import boto3
import json
from django.db.models import Avg, Q
from rest_framework import viewsets, permissions
from .models import Drink, Song, DrinkRating, SongRating, Art
from .forms import SongUploadForm, DrinkRatingForm, SongRatingForm, ArtForm
from .serializers import DrinkSerializer, SongSerializer, ArtSerializer
from accounts.models import CustomUser
from django.urls import reverse_lazy
from django.contrib import messages


def landing_page(request):
    return render(request, 'site/landing.html')


# Drinks Views
class DrinkListView(ListView):
    model = Drink
    template_name = 'site/drink_list.html'
    context_object_name = 'drinks'
    ordering = ['category', 'name']

    def get_queryset(self):
        drinks = Drink.objects.all()
        user = self.request.user

        for drink in drinks:
            drink.user_has_rated = drink.ratings.filter(user=user).exists() if user.is_authenticated else False
        return drinks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DrinkRatingForm() 
        return context

@login_required
def rate_drink(request, drink_id):
    """Handles drink rating submission and redirects back to the drink list."""
    drink = get_object_or_404(Drink, id=drink_id)

    if request.method == "POST":
        form = DrinkRatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data["rating"]
            comment = form.cleaned_data.get("comment", "").strip()  # Ensure comment is always a string

            # If comment is empty, store an empty string instead of null
            comment = comment if comment else ""

            # Update or create the rating
            rating, created = DrinkRating.objects.update_or_create(
                user=request.user,
                drink=drink,
                defaults={"rating": rating_value, "comment": comment}
            )

            # Show success message and redirect to drink list
            messages.success(request, "Your rating has been updated!" if not created else "Thank you for your rating!")
            return redirect("drink_list")

    # Redirect to the drink list if not a POST request
    return redirect("drink_list")


class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


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
        queryset = Song.objects.all()
        search_query = self.request.GET.get("q", "")

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(artist__icontains=search_query) |
                Q(genre__icontains=search_query)
            )

        for song in queryset:
            song.user_has_rated = song.ratings.filter(user=self.request.user).exists() if self.request.user.is_authenticated else False
        
        return queryset

    def get_song_url(self, song):

        local_path = os.path.join(settings.MEDIA_ROOT, "temp_music", os.path.basename(song.audio_file.name))

        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

        if not os.path.exists(local_path): 
            s3_client = boto3.client("s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            s3_client.download_file(settings.AWS_STORAGE_BUCKET_NAME, song.audio_file.name, local_path)

        return reverse("serve_local_song", args=[song.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SongRatingForm()
        return context

@login_required
def rate_song(request, song_id):
    """Handles song rating submission and prevents duplicate ratings."""
    song = get_object_or_404(Song, id=song_id)

    if request.method == "POST":
        try:
            data = json.loads(request.body) 
            rating_value = int(data.get("rating", 0))
            comment = data.get("comment", "").strip() or ""

            existing_rating = SongRating.objects.filter(user=request.user, song=song).first()
            if existing_rating:
                return JsonResponse({"success": False, "error": "You have already rated this song."}, status=400)

            rating = SongRating.objects.create(
                user=request.user,
                song=song,
                rating=rating_value,
                comment=comment
            )

            return JsonResponse({"success": True, "new_avg_rating": song.average_rating})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

class SongUploadView(LoginRequiredMixin, CreateView):
    model = Song
    form_class = SongUploadForm
    template_name = "site/song_upload.html"
    success_url = reverse_lazy("song_list")

def serve_local_song(request, song_id):
    """Downloads a song from AWS S3 and serves it locally."""
    song = get_object_or_404(Song, id=song_id)
    local_path = os.path.join(settings.MEDIA_ROOT, "temp_music", os.path.basename(song.audio_file.name))

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    # Ensure temp_songs directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if not os.path.exists(local_path):  # Only download if missing
        try:
            s3_client.download_file(settings.AWS_STORAGE_BUCKET_NAME, song.audio_file.name, local_path)
        except Exception as e:
            raise Http404(f"Song file not found in S3: {e}")

    # Serve the file if it exists
    if os.path.exists(local_path):
        return FileResponse(open(local_path, "rb"), content_type="audio/mpeg")
    else:
        raise Http404("Local song file is missing.")

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

#// SERVE THE WELCOME VIDEO //#

def get_video_from_s3():
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    local_path = os.path.join(settings.MEDIA_ROOT, "videos", "welcome.mp4")
    
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if not os.path.exists(local_path): 
        try:
            s3_client.download_file(settings.AWS_STORAGE_BUCKET_NAME, "videos/welcome.mp4", local_path)
            print(f"Downloaded video to: {local_path}")
        except Exception as e:
            print(f"Failed to download video: {e}")
            return None  # Indicate failure

    return local_path 

def serve_local_video(request):
    video_path = get_video_from_s3()

    if video_path and os.path.exists(video_path):
        return FileResponse(open(video_path, "rb"), content_type="video/mp4")
    else:
        raise Http404("Video not found.")

#// Art Views \\#
class ArtListView(ListView):
    model = Art
    template_name = "site/art_list.html"
    context_object_name = "artworks"

class ArtDetailView(DetailView):
    model = Art
    template_name = "site/art_detail.html"
    context_object_name = "artwork"

class ArtViewSet(viewsets.ModelViewSet):    
    queryset = Art.objects.all()
    serializer_class = ArtSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()] 
        return [permissions.AllowAny()]

class ArtCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Art
    form_class = ArtForm
    template_name = "site/art_create.html"
    success_url = reverse_lazy("art_list")

    def test_func(self):
        return self.request.user.is_staff