from django.forms import ValidationError
from rest_framework import serializers
from reviews.models import Review
from users.models import User
from movies.models import Movie


class CriticSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    
    critic = CriticSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'stars', 'review', 'spoilers', 'recomendation', 'movie_id', 'critic']
        extra_kwargs = {"recomendation": {"required": False}, "movie": {"required": False}, "critic": {"required": False}}

    def validate_stars(self, value):

         if value > 10:
             raise ValidationError("Ensure this value is less than or equal to 10.")

         if value < 1:
             raise ValidationError("Ensure this value is greater than or equal to 1.")

         return value
    
    def create(self, validated_data):

        movie_id = validated_data.pop('movie_id')
        movie = Movie.objects.get(id = movie_id)
        critic = validated_data.pop('critic')
        review = Review.objects.create(movie = movie, critic = critic, **validated_data)

        return review