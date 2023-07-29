from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, User

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Unregister the default UserAdmin and register CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)