from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from smartfields import fields

from . import models
from projects.models import Skill

User = get_user_model()

def must_be_empty(value):
    if value:
        raise forms.ValidationError('Is not empty')


class UserCreateForm(UserCreationForm):
    """Create a user on signup page."""
    email = forms.EmailField(
        label='Email Address',
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'Email Address'}
    ))
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label='leave empty',
        validators=[must_be_empty]
    )

    class Meta:
        fields = (
            "username",
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


class UserProfileUpdateForm(forms.ModelForm):
    """Update UserProfile model information."""
    firstname = forms.CharField(
                    label='First Name',
                    required=False,
                    widget=forms.TextInput(
                        attrs={'placeholder': 'Enter your first name...'})
                )
    lastname = forms.CharField(
                    label='Last Name',
                    required=False,
                    widget=forms.TextInput(
                        attrs={'placeholder': 'Enter your last name...'})
                )
    bio = forms.CharField(
        label='About You',
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Tell us about yourself...',
                'style': 'resize: both; overflow: auto;',
            }
        )
    )
    avatar = fields.ImageField(blank=True)
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label=''
    )
    class Meta:
        model = models.UserProfile
        fields = ['firstname', 'lastname', 'bio', 'avatar', 'skills']
        labels = {
            'avatar': _('Your Photo'),
        }
