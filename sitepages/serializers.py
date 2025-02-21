from rest_framework import serializers
from .models import Drink, DrinkRating, Song

class DrinkSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Drink
        fields = ['id', 'name', 'category', 'ingredients', 'method', 'average_rating']

    def get_average_rating(self, obj):
        return obj.ratings.aggregate(Avg('rating'))['rating__avg'] or 0 

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'