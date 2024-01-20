from django.urls import path
from core.views import user_profile, search_users

urlpatterns = [
    path('search/', search_users, name='search_users'),  # Add this line for search functionality
    path('<str:username>/', user_profile, name='user_profile'),
    # Add other URL patterns for your profiles app as needed
]
