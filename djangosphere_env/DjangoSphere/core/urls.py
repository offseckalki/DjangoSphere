from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
# urls.py
from django.urls import path
from .views import search_users

urlpatterns = [
    # ... your other patterns
    path('search/', search_users, name='search_users'),
]


urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('rooms/', include('room.urls')),  # Include room-specific URLs
    path('profiles/', include('core.templates.profiles.urls')),


]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
