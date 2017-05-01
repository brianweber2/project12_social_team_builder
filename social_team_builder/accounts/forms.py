from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from smartfields import fields

from . import models

User = get_user_model()


class UserCreateForm(UserCreationForm):
    """Create a user on signup page."""
    class Meta:
        fields = (
            "email",
            "password1",
            "password2"
        )
        model = get_user_model()


class UserUpdateForm(forms.ModelForm):
    """Update User model information."""
    email = forms.EmailField(
                label='Email Address',
                widget=forms.TextInput(
                    attrs={
                        'type': 'email',
                        'placeholder': 'Enter your email address...'}
                ))
    username = forms.CharField(
                label='Username',
                widget=forms.TextInput(
                    attrs={
                        'placeholder': 'Enter a username...'}
                ))
    class Meta:
        model = get_user_model()
        fields = ['email', 'username']


class UserProfileUpdateform(forms.ModelForm):
    """Update UserProfile model information."""
    firstname = forms.CharField(
                    label='First Name',
                    widget=forms.TextInput(
                        attrs={'placeholder': 'Enter your first name...'})
                )
    lastname = forms.CharField(
                    label='Last Name',
                    widget=forms.TextInput(
                        attrs={'placeholder': 'Enter your last name...'})
                )
    bio = forms.CharField(max_length=300, label='About You',
                            widget=forms.Textarea(
                                attrs={
                                    'placeholder': 'Tell us about yourself...',
                                    'style': 'resize: both; overflow: auto;',
                                }
                            ))
    avatar = fields.ImageField(blank=True)
    class Meta:
        model = models.UserProfile
        fields = ['firstname', 'lastname', 'bio', 'avatar', 'skills']
        labels = {
            'avatar': _('Your Photo'),
            'skills': '',
        }
