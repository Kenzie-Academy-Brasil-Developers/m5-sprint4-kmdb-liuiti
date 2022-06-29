from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView, Response, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from reviews.permissions import ReviewListPermission, ReviewDeletePermission
from .models import Review
from .serializers import ReviewSerializer


class ReviewView(APIView, PageNumberPagination):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewListPermission]

    def get(self, request, movie_id):
        try:
            if movie_id:
                reviews = Review.objects.filter(id = movie_id)
                result_page = self.paginate_queryset(reviews, request, view = self)
                serializer = ReviewSerializer(result_page, many = True)

                return self.get_paginated_response(serializer.data)

        except ObjectDoesNotExist:

            return Response(
                {"message": "Movie not found."}, status.HTTP_404_NOT_FOUND
            )

    def post(self, request, movie_id):
        try:
            if movie_id:
                serializer = ReviewSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(critic = request.user, movie_id = movie_id)
            
                return Response(serializer.data, status.HTTP_201_CREATED)
        
        except ObjectDoesNotExist:

            return Response(
                {"message": "Movie not found."}, status.HTTP_404_NOT_FOUND
            )

class ReviewViewDetail(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewDeletePermission]

    def delete(self, request, review_id):

        try:
            if review_id:

                review = Review.objects.get(id = review_id)
                self.check_object_permissions(request, review)
                review.delete()

                return Response(status = status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:

            return Response(
                {"message": "Review not found."}, status.HTTP_404_NOT_FOUND
            )

class ReviewsViewAllList(APIView, PageNumberPagination):

    def get(self, request):

        reviews = Review.objects.all()
        result_page = self.paginate_queryset(reviews, request, view = self)
        serializer = ReviewSerializer(result_page, many = True)

        return self.get_paginated_response(serializer.data)