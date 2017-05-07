from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse


class Skill(models.Model):
    """User skills class."""
    ANDROID = 1
    DESIGNER = 2
    JAVA = 3
    PHP = 4
    PYTHON = 5
    RAILS = 6
    WORDPRESS = 7
    IOS = 8

    SKILL_CHOICES = (
        (str(ANDROID), 'Android Developer'),
        (str(DESIGNER), 'Designer'),
        (str(JAVA), 'Java Developer'),
        (str(PHP), 'PHP Developer'),
        (str(PYTHON), 'Python Developer'),
        (str(RAILS), 'Rails Developer'),
        (str(WORDPRESS), 'Wordpress Developer'),
        (str(IOS), 'iOS Developer')
    )

    name = models.CharField(choices=SKILL_CHOICES, max_length=8, default='')

    def __str__(self):
        return self.get_name_display()


class Project(models.Model):
    title = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    time_estimate = models.TextField(default='')
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    recruited = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.title()


class Position(models.Model):
    project = models.ForeignKey(Project, default='', on_delete=models.CASCADE, related_name='positions')
    name = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    related_skill = models.OneToOneField(Skill)

    def __str__(self):
        return '{} - {}'.format(self.project.title.title(), self.related_skill.name)


class Application(models.Model):
    applicant = models.OneToOneField(settings.AUTH_USER_MODEL)
    success = models.BooleanField(default=False)
    position = models.OneToOneField(Position)
