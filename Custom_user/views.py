from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class RegisterView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful!",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "phone_number": user.phone_number,
                    "is_landlord": user.is_landlord,
                    "is_renter": user.is_renter,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            }, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    API endpoint to retrieve the logged-in user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Auth0LoginView(APIView):
    """
    API endpoint for logging in with Auth0.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("access_token")
        if not token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        auth0_domain = settings.AUTH0_DOMAIN
        user_info_url = f"https://{auth0_domain}/userinfo"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            user_info = requests.get(user_info_url, headers=headers)
            user_info.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Auth0 request failed: {e}")
            return Response({"error": "Invalid Auth0 token or request error"}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = user_info.json()
        email = user_data.get("email")
        name = user_data.get("name")
        profile_pic = user_data.get("picture")

        if not email:
            return Response({"error": "Email is required from Auth0"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(email=email, defaults={
            "username": name or email.split("@")[0],  # Default to part of email if name is missing
            "profile_picture": profile_pic
        })

        if not created:
            # Update user profile picture if it's different
            if user.profile_picture != profile_pic:
                user.profile_picture = profile_pic
                user.save()

        # Assign roles
        is_landlord = request.data.get("is_landlord", False)
        user.is_landlord = is_landlord
        user.is_renter = not is_landlord
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful!",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "profile_picture": user.profile_picture.url if user.profile_picture else None,
                "is_landlord": user.is_landlord,
                "is_renter": user.is_renter,
            }
        }, status=status.HTTP_200_OK)
