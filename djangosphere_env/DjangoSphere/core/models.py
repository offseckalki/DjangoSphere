from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    # Your existing fields
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Add a search field (optional, based on your requirements)
    search_field = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        # Update the search field before saving (optional)
        self.search_field = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # Add other profile fields as needed
