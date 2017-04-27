from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    """Create a user on signup page."""
    class Meta:
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        )
        model = get_user_model()
