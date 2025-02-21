from django.db import models
from django.conf import settings
from django.db.models import Avg

#// Drink Models //#
class Drink(models.Model):
    CATEGORY_CHOICES = [
        ('coffee', 'Coffee'),
        ('tea', 'Tea'),
        ('hot chocolate', 'Hot Chocolate'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    ingredients = models.TextField(help_text="List ingredients separated by commas")
    method = models.TextField(help_text="Preparation method")

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        return self.ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    def user_has_rated(self, user):
        return self.ratings.filter(user=user).exists()


class DrinkRating(models.Model):
    drink = models.ForeignKey(Drink, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('drink', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.drink.name}: {self.rating}/5"


#// Song Models //#
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to="music/")  # Stores files in AWS S3

    def __str__(self):
        return f"{self.title} - {self.artist}"

    @property
    def average_rating(self):
        return self.ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    def user_has_rated(self, user):
        return self.ratings.filter(user=user).exists() if user.is_authenticated else False


# Song Rating Model
class SongRating(models.Model):
    song = models.ForeignKey(Song, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('song', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.song.title}: {self.rating}/5"