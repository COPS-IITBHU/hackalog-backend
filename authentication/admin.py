from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class ProfileInline(admin.StackedInline):
  model = UserProfile
  can_delete=False

class UserAdmin(BaseUserAdmin):
  inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)