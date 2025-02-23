from rest_framework import serializers
from .models import Drink, DrinkRating, Song, Art
from django.conf import settings

class DrinkSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Drink
        fields = ['id', 'name', 'category', 'ingredients', 'method', 'average_rating']

    def get_average_rating(self, obj):
        return obj.ratings.aggregate(Avg('rating'))['rating__avg'] or 0 

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class ArtSerializer(serializers.ModelSerializer):
    aws_url = serializers.SerializerMethodField()
    class Meta:
        model = Art
        fields = ["id", "title", "artist", "description", "image","aws_url", "created_at"]
    
    def get_aws_url(self, obj):
        if obj.image:
            return f"{settings.MEDIA_URL}{obj.image}"
        return None   