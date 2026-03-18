from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_verified', 'is_staff', 'created_at']
    list_filter = ['is_verified', 'is_staff', 'is_profile_public']
    search_fields = ['username', 'email']
    ordering = ['-created_at']

    fieldsets = UserAdmin.fieldsets + (
        ('Профиль', {
            'fields': ('avatar', 'cover', 'bio', 'location', 'date_of_birth')
        }),
        ('Соцсети', {
            'fields': ('vkontact', 'telegram')
        }),
        ('Приватность', {
            'fields': ('is_profile_public', 'show_email', 'is_verified')
        }),
        ('Статистика', {
            'fields': ('books_read_count', 'books_reading_count', 'books_saved_count', 'last_seen')
        }),
    )