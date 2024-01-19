from django.urls import path
from core import views  # Adjust the import path based on your actual structure

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    # Add other URL patterns for your profiles app as needed
]
