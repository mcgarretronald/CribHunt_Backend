from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
import requests
import logging
import json
import os
from .models import CustomUser

User = get_user_model()
logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Auth0LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        auth0_token = request.data.get("access_token")
        is_landlord = request.data.get("is_landlord", False)
        is_renter = request.data.get("is_renter", False)

        if not auth0_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        auth0_domain = settings.AUTH0_DOMAIN
        auth0_url = f"https://{auth0_domain}/userinfo"

        headers = {"Authorization": f"Bearer {auth0_token}"}
        response = requests.get(auth0_url, headers=headers)

        if response.status_code != 200:
            return Response({"error": "Invalid Auth0 token"}, status=status.HTTP_400_BAD_REQUEST)

        auth0_user_info = response.json()
        email = auth0_user_info.get("email")

        if not email:
            return Response({"error": "Email not provided by Auth0"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user exists
        user = User.objects.filter(email=email).first()

        if user:
            # Existing user - log them in
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Auth0 login successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "is_landlord": user.is_landlord,
                    "is_renter": user.is_renter
                }
            }, status=status.HTTP_200_OK)

        # New user - register them with Auth0 (without a password)
        user = User(
            email=email,
            username=email.split("@")[0],  # Use email prefix as username
            is_landlord=is_landlord,
            is_renter=is_renter
        )
        user.set_unusable_password()  # This prevents password login
        user.save()

        # Issue JWT tokens for new Auth0 user
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Auth0 registration successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {
                "email": user.email,
                "username": user.username,
                "is_landlord": user.is_landlord,
                "is_renter": user.is_renter
            }
        }, status=status.HTTP_201_CREATED)
