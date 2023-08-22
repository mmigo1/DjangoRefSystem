from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user']


admin.site.register(Profile, ProfileAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('phone', 'is_staff', 'is_active',)
    list_filter = ('phone', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('phone',)
    ordering = ('phone',)


admin.site.register(CustomUser, CustomUserAdmin)
