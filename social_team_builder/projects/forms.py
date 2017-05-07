from django import forms

from . import models


class CreateProjectForm(forms.ModelForm):
    """Form to create a new project."""
    title = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Project Title', 'class': 'circle--input--h1'}
        )
    )
    description = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': 'Project description...'}
        )
    )
    time_estimate = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': 'Time estimate', 'class': 'circle--textarea--input'}
        )
    )

    class Meta:
        fields = (
            'title',
            'description',
            'time_estimate'
        )
        model = models.Project


class CreatePositionForm(forms.ModelForm):
    """Form to create a new position for a project."""
    name = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Position Title', 'class': 'circle--input--h3'}
        )
    )
    description = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': 'Position description...'}
        )
    )

    class Meta:
        fields = (
            'name',
            'description',
            'related_skill'
        )
        model = models.Position
