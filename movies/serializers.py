from rest_framework import serializers
from genres.serializers import GenreSerializer
from genres.models import Genre
from movies.models import Movie

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict):
        genres_data = validated_data.pop("genres")
        movie = Movie.objects.create(**validated_data)
        for gen in genres_data:
            genre = Genre.objects.get_or_create(**gen)[0]
            movie.genres.add(genre)

        return movie

    def update(self, instance: Movie, validated_data: dict) -> Movie:
        genre_movie = validated_data.get("genres")

        if genre_movie:
            genre_data = validated_data.pop("genres")
            for gen in genre_data:
                genre = Genre.objects.get_or_create(**gen)[0]
                instance.genres.add(genre)

        instance.title = validated_data.get("title", instance.title)
        instance.duration = validated_data.get("duration", instance.duration)
        instance.premiere = validated_data.get("premiere", instance.premiere)
        instance.classification = validated_data.get("classification", instance.classification)
        instance.synopsis = validated_data.get("synopsis", instance.synopsis)

        instance.save()

        return instance
