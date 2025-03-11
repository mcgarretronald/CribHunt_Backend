from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Property, PropertyImage, PropertyVideo
from .serializers import PropertySerializer, PropertyImageSerializer, PropertyVideoSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    parser_classes = (MultiPartParser, FormParser)  # Enable file uploads
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        property_instance = serializer.save(owner=self.request.user)

        # Handle multiple images
        images = self.request.FILES.getlist('images')
        if images:
            for image in images:
                if isinstance(image, InMemoryUploadedFile):  # Ensure it's a valid file
                    PropertyImage.objects.create(property=property_instance, image=image)

        # Handle multiple videos
        videos = self.request.FILES.getlist('videos')
        if videos:
            for video in videos:
                if isinstance(video, InMemoryUploadedFile):  # Ensure it's a valid file
                    PropertyVideo.objects.create(property=property_instance, video=video)

        # Return a success response
        return Response(
            {
                "message": "Property created successfully!",
                "property": PropertySerializer(property_instance).data,
            },
            status=status.HTTP_201_CREATED,
        )



class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # Handle images update (replace existing)
            images = request.FILES.getlist('images')
            if images:
                instance.images.all().delete()  # Remove old images
                for image in images:
                    PropertyImage.objects.create(property=instance, image=image)

            # Handle videos update (replace existing)
            videos = request.FILES.getlist('videos')
            if videos:
                instance.videos.all().delete()  # Remove old videos
                for video in videos:
                    PropertyVideo.objects.create(property=instance, video=video)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)