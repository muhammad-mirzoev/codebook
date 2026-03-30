from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Author, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["icon", "name", "slug", "order", "books_count"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]

    def books_count(self, obj):
        return obj.books.count()
    books_count.short_description = "Книг"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "books_count", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def books_count(self, obj):
        return obj.books.count()
    books_count.short_description = "Книг"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["cover_preview", "title", "category", "author", "level", "is_featured", "is_new", "is_published", "views_count", "created_at"]
    list_filter = ["category", "level", "language", "is_featured", "is_new", "is_published"]
    search_fields = ["title", "description", "author__name"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_featured", "is_new", "is_published"]
    readonly_fields = ["views_count", "saves_count", "created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Основное", {
            "fields": ("title", "slug", "description", "cover")
        }),
        ("Связи", {
            "fields": ("category", "author")
        }),
        ("Детали", {
            "fields": ("level", "language", "pages", "published_year", "isbn", "file_url")
        }),
        ("Флаги", {
            "fields": ("is_featured", "is_new", "is_published")
        }),
        ("Статистика", {
            "fields": ("views_count", "saves_count", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" width="40" height="55" style="object-fit:cover;border-radius:4px">', obj.cover.url)
        return "—"
    cover_preview.short_description = "Обложка"
