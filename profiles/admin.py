from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Friendships
from main.forms import RegisterForm


class MyUserAdmin(UserAdmin):
    model = User
    add_form = RegisterForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'bio',
                    'friends',
                    'avatar',
                )
            }
        )
    )


admin.site.register(User, MyUserAdmin)
admin.site.register(Friendships)
