# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models

admin.site.register(models.Skill)
admin.site.register(models.Project)
admin.site.register(models.Application)
admin.site.register(models.Position)
