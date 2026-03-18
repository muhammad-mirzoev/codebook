from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):

    # --- Основное ---
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    cover = models.ImageField(upload_to='covers/%Y/%m/', blank=True, null=True)

    # --- О себе ---
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # --- Соцсети ---
    vkontact = models.CharField(max_length=100, blank=True)
    telegram = models.CharField(max_length=100, blank=True)

    # --- Настройки приватности ---
    is_profile_public = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)

    # --- Статистика (автоматически) ---
    books_read_count = models.PositiveIntegerField(default=0)
    books_reading_count = models.PositiveIntegerField(default=0)
    books_saved_count = models.PositiveIntegerField(default=0)

    # --- Системное ---
    is_verified = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.username} ({self.email})'

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return '/static/img/default_avatar.png'

    def get_cover(self):
        if self.cover:
            return self.cover.url
        return '/static/img/default_cover.jpg'

    def get_online_status(self):
        now = timezone.now()
        diff = now - self.last_seen
        if diff.seconds < 300:  # меньше 5 минут
            return 'online'
        return 'offline'
