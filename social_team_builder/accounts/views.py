from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from . import forms


class SignUpView(SuccessMessageMixin, generic.CreateView):
    """View to allow user to sign up."""
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('home')
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
        return super(LogoutView, self).get(request, *args, **kwargs)
