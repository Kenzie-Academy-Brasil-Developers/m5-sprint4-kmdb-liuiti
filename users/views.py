from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView, Response, status
from rest_framework.authtoken.models import Token
from users.serializers import LoginSerializer, RegisterSerializer
from .models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import CustomPermission
from django.core.exceptions import ObjectDoesNotExist

class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomPermission]

    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request, user_id = None):
        users = User.objects.all()
        serializer = RegisterSerializer(users, many = True)

        return Response(serializer.data)


class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomPermission]

    def get(self, request, user_id):
        try:
            if user_id:
                user = User.objects.get(id=user_id)
                serializer = RegisterSerializer(user)
                
                return Response(serializer.data)

        except ObjectDoesNotExist:
            return Response(
                {"message": "User not found."}, status.HTTP_404_NOT_FOUND
            )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        
        return Response(
            {"detail": "invalid email or password"}, status.HTTP_401_UNAUTHORIZED
        )