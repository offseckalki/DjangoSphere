from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile

class UserSearchForm(forms.Form):
    username_query = forms.CharField(max_length=100)

class UserDetailsForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError('Last name is required.')
        return last_name

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
