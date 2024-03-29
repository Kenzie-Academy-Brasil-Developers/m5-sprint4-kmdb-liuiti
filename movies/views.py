from movies.models import Movie
from rest_framework.views import APIView, Response, status
from .serializers import MovieSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from movies.permissions import CustomPermission
from rest_framework.pagination import PageNumberPagination

class MovieView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomPermission]

    def post(self, request):
        serializer = MovieSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request, movie_id = None):
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many = True)
        
        return self.get_paginated_response(serializer.data)

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