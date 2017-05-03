from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.contrib import messages

from braces.views import LoginRequiredMixin

from . import forms
from . import models


class CreateProjectView(LoginRequiredMixin, generic.CreateView):
    """View to create a project that a user needs help on."""
    template_name = 'projects/project_new.html'
    login_url = settings.LOGIN_REDIRECT_URL
    form_class = forms.CreateProjectForm
    second_form_class = forms.CreatePositionForm

    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        form2 = self.second_form_class(data=request.POST)

        if form.is_valid() and form2.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
            new_position = form2.save(commit=False)
            new_position.project = new_project
            new_position.save()
            messages.success(request, "{} has been successfully added!".format(new_project.title))
            return HttpResponseRedirect(reverse('home'))
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2)
            )


class SeeAllProjectApplicantsView(LoginRequiredMixin, generic.TemplateView):
    """View to see all applicants for my project's positions."""
    pass


# View to search for projects based on words in their titles or descriptions


# View to filter projects by the positions they need filled


class UserApplyToProjectView(LoginRequiredMixin):
    """View for a user to apply for a position in a project."""
    pass
