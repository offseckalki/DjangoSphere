# profiles/views.py
from django.contrib.auth.models import User
from django.shortcuts import render

def search_users(request):
    query = request.GET.get('query')
    if query:
        # Perform case-insensitive search on username and full name
        users = User.objects.filter(username__icontains=query) | User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query)
    else:
        users = User.objects.none()

    return render(request, 'profiles/search_results.html', {'query': query, 'users': users})
