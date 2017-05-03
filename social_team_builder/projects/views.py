from django.shortcuts import render
from django.views import generic

from braces.views import LoginRequiredMixin

from . import forms
from . import models


class CreateProjectView(LoginRequiredMixin, generic.CreateView):
    """View to create a project that a user needs help on."""
    pass


class SeeAllProjectApplicantsView(LoginRequiredMixin, generic.TemplateView):
    """View to see all applicants for my project's positions."""
    pass


# View to search for projects based on words in their titles or descriptions


# View to filter projects by the positions they need filled


class UserApplyToProjectView(LoginRequiredMixin):
    """View for a user to apply for a position in a project."""
    pass
