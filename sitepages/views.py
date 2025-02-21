from django.http import FileResponse, Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os
import boto3
import json
from django.db.models import Avg, Q
from rest_framework import viewsets
from .models import Drink, Song, DrinkRating, SongRating
from .forms import SongUploadForm, DrinkRatingForm, SongRatingForm
from .serializers import DrinkSerializer, SongSerializer
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

        if not os.path.exists(local_path):  # Only download if it doesn't exist
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
            data = json.loads(request.body)  # Ensure JSON data is read
            rating_value = int(data.get("rating", 0))
            comment = data.get("comment", "").strip() or ""

            # Check if user has already rated the song
            existing_rating = SongRating.objects.filter(user=request.user, song=song).first()
            if existing_rating:
                return JsonResponse({"success": False, "error": "You have already rated this song."}, status=400)

            # Save the rating
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

    song = get_object_or_404(Song, id=song_id)
    local_path = os.path.join(settings.MEDIA_ROOT, "temp_music", os.path.basename(song.audio_file.name))

    try:
        return FileResponse(open(local_path, "rb"), content_type="audio/mpeg")
    except FileNotFoundError:
        raise Http404("Song file not found.")

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
