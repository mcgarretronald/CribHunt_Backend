from rest_framework import serializers
from .models import Property, PropertyImage, PropertyVideo
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ['id', 'video']

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)  # Allow uploads
    videos = PropertyVideoSerializer(many=True, required=False)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'

    def get_owner(self, obj):
        return obj.owner.phone_number if hasattr(obj.owner, 'phone_number') else "Phone number not available"

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        videos_data = self.context['request'].FILES.getlist('videos')

        property_instance = Property.objects.create(**validated_data)

        for image in images_data:
            PropertyImage.objects.create(property=property_instance, image=image)
        
        for video in videos_data:
            PropertyVideo.objects.create(property=property_instance, video=video)

        return property_instance
