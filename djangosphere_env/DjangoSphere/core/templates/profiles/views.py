from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import UserSearchForm  # Import the UserSearchForm

def search_users(request):
    form = UserSearchForm(request.GET)
    results = []

    if form.is_valid():
        username_query = form.cleaned_data['username_query']
        # Assuming UserProfile has a ForeignKey 'user' pointing to the User model
        results = UserProfile.objects.filter(user__username__icontains=username_query)

    return render(request, 'profiles/search_results.html', {'form': form, 'results': results})
