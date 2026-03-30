from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=7, default="#4f8ef7")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})


class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="authors/%Y/%m/", blank=True, null=True)
    telegram = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Author.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_photo(self):
        if self.photo:
            return self.photo.url
        return "/static/img/default_author.png"


class Book(models.Model):

    LEVEL_CHOICES = [
        ("beginner", "Для начинающих"),
        ("intermediate", "Средний уровень"),
        ("advanced", "Продвинутый"),
    ]

    LANGUAGE_CHOICES = [
        ("ru", "Русский"),
        ("en", "English"),
    ]

    # Основное
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField()
    cover = models.ImageField(upload_to="books/covers/%Y/%m/", blank=True, null=True)

    # Связи
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books"
    )

    # Детали
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="beginner")
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default="ru")
    pages = models.PositiveIntegerField(default=0)
    published_year = models.PositiveIntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True)

    # Файл/ссылка на pdf или внешний ресурс
    file_url = models.URLField(blank=True)

    # Статистика
    views_count = models.PositiveIntegerField(default=0)
    saves_count = models.PositiveIntegerField(default=0)

    # Флаги
    is_featured = models.BooleanField(default=False)  # на главной
    is_new = models.BooleanField(default=False)  # бейдж "Новинка"
    is_published = models.BooleanField(default=True)

    # Даты
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = str(uuid.uuid4())[:8]
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"slug": self.slug})

    def get_cover(self):
        if self.cover:
            return self.cover.url
        return "/static/img/default_book.png"

    def get_level_display_icon(self):
        icons = {
            "beginner": "🟢",
            "intermediate": "🟡",
            "advanced": "🔴",
        }
        return icons.get(self.level, "⚪")
