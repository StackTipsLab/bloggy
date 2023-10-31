from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.html import format_html

from bloggy.models import User


@admin.register(User)
class MyUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username', 'email_display', 'full_name_display', 'is_staff', 'is_active', 'date_joined', 'last_login',
        'profile_photo_tag', 'articles_count_display',)
    list_filter = ('is_staff', 'is_superuser', 'groups', 'is_active')
    search_fields = ('username',)
    ordering = ('-date_joined',)
    readonly_fields = ['profile_photo_tag', 'date_joined', 'last_login']
    fieldsets = (
        ("Account details", {'fields': ('username', 'password', 'name')}),
        ("Permissions", {
            'fields': ('is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions',)
        }),
        ('Personal details', {
            'fields': (
                'website', 'twitter', 'linkedin', 'youtube', 'github', 'bio',
                'profile_photo_tag', 'profile_photo', 'date_joined', 'last_login'),
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    def email_display(self, queryset):
        return format_html(f'<small>{queryset.email}</small>')

    email_display.short_description = "Email"

    def full_name_display(self, queryset):
        return format_html(f'<small>{queryset.name}</small>')

    full_name_display.short_description = "Name"

    def articles_count_display(self, queryset):
        return queryset.articles.count()

    articles_count_display.short_description = "Articles"
