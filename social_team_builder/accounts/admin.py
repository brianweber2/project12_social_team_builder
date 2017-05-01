from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


class UserProfileInline(admin.StackedInline):
    model = models.UserProfile
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email', 'userprofile__firstname',
                'userprofile__lastname']
    list_display = ['username', 'email', 'get_firstname', 'get_lastname',
    'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    inlines = (UserProfileInline, )

    def get_firstname(self, obj):
        return obj.userprofile.firstname
    get_firstname.short_description = 'First Name'
    get_firstname.admin_order_field = 'userprofile'

    def get_lastname(self, obj):
        return obj.userprofile.lastname
    get_lastname.short_description = 'Last Name'
    get_firstname.admin_order_field = 'userprofile'

admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserProfile)
