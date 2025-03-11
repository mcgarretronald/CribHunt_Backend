from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser


User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password", "phone_number", "is_landlord", "is_renter"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            phone_number=validated_data.get("phone_number", ""),
            is_landlord=validated_data.get("is_landlord", False),
            is_renter=validated_data.get("is_renter", False),
        )
        return user

class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email_or_username = data.get("email_or_username")
        password = data.get("password")

        # Try to find user by email
        user = User.objects.filter(email=email_or_username).first()

        # If not found, try username
        if not user:
            user = User.objects.filter(username=email_or_username).first()

        if not user:
            raise serializers.ValidationError({"email_or_username": "No account found with this email or username."})

        # Check if password is correct
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password. Please try again."})

        return {"user": user}
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "phone_number", "profile_picture", "is_landlord", "is_renter"]
