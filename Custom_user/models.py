from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_landlord = models.BooleanField(default=False)
    is_renter = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        """Override set_password to hash passwords properly"""
        from django.contrib.auth.hashers import make_password
        if raw_password:
            self.password = make_password(raw_password)
        else:
            self.set_unusable_password()  
