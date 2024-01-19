from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfilePictureForm, UserDetailsForm
from .models import UserProfile


def frontpage(request):
    return render(request, 'core/frontpage.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('frontpage')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('frontpage')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('frontpage')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If UserProfile does not exist, create a new one for the user
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserDetailsForm(request.POST, instance=request.user)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_picture_form.is_valid():
            user_form.save()
            profile_picture_form.save()
            messages.success(request, 'Profile details updated successfully.')

    else:
        user_form = UserDetailsForm(instance=request.user)
        profile_picture_form = ProfilePictureForm(instance=user_profile)

    return render(request, 'core/profile.html', {'user_form': user_form, 'profile_picture_form': profile_picture_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'core/change_password.html', {'form': form})
