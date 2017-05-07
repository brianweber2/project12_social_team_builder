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
    requirements = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': ''}
        )
    )

    class Meta:
        fields = (
            'title',
            'description',
            'time_estimate',
            'requirements'
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
        )
        model = models.Position

PositionFormset = forms.modelformset_factory(
    models.Position,
    form=CreatePositionForm,
    extra=1,
    max_num=5
)
