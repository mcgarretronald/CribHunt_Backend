from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Property(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    amenities = models.TextField()
    property_type = models.CharField(max_length=255)
    bedrooms = models.IntegerField()
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="properties")

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"

class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to='property_videos/')

    def __str__(self):
        return f"Video for {self.property.title}"
