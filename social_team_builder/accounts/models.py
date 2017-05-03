from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse

from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            username = email.split('@')[0]

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username=None):
        user = self.create_user(
            email,
            username,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True, default='')
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.username

    def get_long_name(self):
        return "@{} ({})".format(self.username, self.email)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    firstname = models.CharField(max_length=40, default='', blank=True)
    lastname = models.CharField(max_length=40, default='', blank=True)
    bio = models.TextField(blank=True, default='')
    avatar = fields.ImageField(blank=True, null=True, upload_to='avatar_photos/',
                               dependencies=[
        FileDependency(attname='avatar_png', processor=ImageProcessor(
            format='PNG', scale={'max_width': 150, 'max_height': 150})),
    ])
    skills = models.ManyToManyField('projects.Skill', blank=True, default='', related_name='skills')

    def get_absolute_url(self):
        return reverse("accounts:profile", {'username': self.user.username})

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)


def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile object when a new user is created."""
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
