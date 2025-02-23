from django.contrib import admin
from .models import Drink, Song, DrinkRating, SongRating, Art

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')

@admin.register(DrinkRating)
class DrinkRatingAdmin(admin.ModelAdmin):
    list_display = ('drink', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('drink__name', 'user__username')
    ordering = ('-created_at',)

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "genre")
    search_fields = ("title", "artist", "genre")

@admin.register(SongRating)
class SongRatingAdmin(admin.ModelAdmin):
    list_display = ('song', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('song__name', 'user__username')
    ordering = ('-created_at',)

@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "created_at")
    search_fields = ("title", "artist")
    readonly_fields = ("created_at",)