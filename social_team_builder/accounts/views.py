from django.contrib.auth import login, logout, get_user_model
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from braces.views import LoginRequiredMixin

from . import forms
from . import models


class SignUpView(SuccessMessageMixin, generic.CreateView):
    """View to allow user to sign up."""
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/signup.html'
    success_message = "Your account has been created!"


class SignInView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signin.html'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(SignInView, self).form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been logged out.")
        return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    """View for use to view their profile information."""
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        lookup = kwargs.get('username')
        user = models.User.objects.get(username=lookup)
        profile = models.UserProfile.objects.prefetch_related('skills').get(user=user)
        context['profile'] = profile
        context['skills'] = [skill for skill in profile.skills.all()]
        print(context['skills'])
        return context


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """View for user to update their profile information."""
    model = get_user_model()
    template_name = 'accounts/profile_edit.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    form_class = forms.UserUpdateForm
    second_form_class = forms.UserProfileUpdateform

    # Allow two forms to be shown in the view
    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.request.user)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=self.request.user.userprofile)
        return context

    # Make sure both models are saved on POST request
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(data=request.POST, instance=request.user)
        form2 = self.second_form_class(
            data=request.POST,
            instance=request.user.userprofile,
            files=request.FILES
        )

        if form.is_valid() and form2.is_valid():
            userdata = form.save(commit=False)
            userdata.save()
            profiledata = form2.save(commit=False)
            profiledata.user = userdata
            profiledata.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2)
            )

    # Make sure both model instances are grabbed from the database on GET request
    def get(self, request, *args, **kwargs):
        super(UserProfileUpdateView, self).get(request, *args, **kwargs)
        form = self.form_class(instance=request.user)
        form2 = self.second_form_class(instance=request.user.userprofile)
        return self.render_to_response(
            self.get_context_data(object=self.object, form=form, form2=form2)
        )

    # URL when POST is successful
    def get_success_url(self):
        messages.success(self.request, "Your profile has been successfully updated.")
        return reverse(
            'accounts:profile',
            kwargs={'username': self.request.user.username}
        )
