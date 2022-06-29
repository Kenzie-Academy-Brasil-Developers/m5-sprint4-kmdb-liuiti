from django.shortcuts import render
from movies.models import Movie
from rest_framework.views import APIView, Response, status
from .serializers import MovieSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from movies.permissions import CustomPermission

class MovieView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomPermission]

    def post(self, request):
        serializer = MovieSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request, movie_id = None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many = True)
        return Response(serializer.data)

class MovieViewDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomPermission]

    def get(self, request, movie_id):
        try:
            if movie_id:
                movie = Movie.objects.get(id=movie_id)
                serializer = MovieSerializer(movie)

                return Response(serializer.data)
        
        except ObjectDoesNotExist:
            return Response(
                {"message": "Movie not found"}, status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, movie_id):
        try:
            if movie_id:
                movie = Movie.objects.get(id=movie_id)
                movie.delete()

                return Response(status = status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            return Response(
                {"message": "Movie not found."}, status.HTTP_404_NOT_FOUND
            )            
    
    def patch(self, request, movie_id):
        try:
            animal = Movie.objects.get(id=movie_id)
            serializer = MovieSerializer(animal, request.data, partial = True)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            return Response(serializer.data)
        
        except ObjectDoesNotExist:
            return Response(
                {"message": "Movie not found."}, status.HTTP_404_NOT_FOUND
            )