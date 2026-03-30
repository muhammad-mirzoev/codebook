from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Book, Category
from apps.users.models import CustomUser


def home_view(request):
    featured_books = Book.objects.filter(is_featured=True, is_published=True).select_related('category', 'author')[:10]
    new_books = Book.objects.filter(is_new=True, is_published=True).select_related('category', 'author')[:10]
    popular_books = Book.objects.filter(is_published=True).order_by('-views_count').select_related('category', 'author')[:10]
    categories = Category.objects.all()

    context = {
        'featured_books': featured_books,
        'new_books': new_books,
        'popular_books': popular_books,
        'categories': categories,
        'total_books': Book.objects.filter(is_published=True).count(),
        'total_categories': Category.objects.count(),
        'total_users': CustomUser.objects.count(),
    }
    return render(request, 'home.html', context)


def books_list_view(request):
    books = Book.objects.filter(is_published=True).select_related('category', 'author')
    categories = Category.objects.all()

    # Фильтры
    category_slug = request.GET.get('category')
    level = request.GET.get('level')
    language = request.GET.get('language')
    sort = request.GET.get('sort', '-created_at')

    if category_slug:
        books = books.filter(category__slug=category_slug)
    if level:
        books = books.filter(level=level)
    if language:
        books = books.filter(language=language)

    sort_options = ['-created_at', '-views_count', '-saves_count', 'title']
    if sort in sort_options:
        books = books.order_by(sort)

    context = {
        'books': books,
        'categories': categories,
        'selected_category': category_slug,
        'selected_level': level,
        'selected_language': language,
        'selected_sort': sort,
        'level_choices': Book.LEVEL_CHOICES,
    }
    return render(request, 'books/list.html', context)


def book_detail_view(request, slug):
    book = get_object_or_404(Book, slug=slug, is_published=True)

    # Увеличиваем счётчик просмотров
    Book.objects.filter(pk=book.pk).update(views_count=book.views_count + 1)

    # Похожие книги (та же категория)
    related_books = Book.objects.filter(
        category=book.category,
        is_published=True
    ).exclude(pk=book.pk).select_related('category', 'author')[:6]

    # Статус книги у текущего пользователя
    user_book_status = None
    if request.user.is_authenticated:
        from apps.library.models import UserBook
        user_book = UserBook.objects.filter(user=request.user, book=book).first()
        if user_book:
            user_book_status = user_book.status

    context = {
        'book': book,
        'related_books': related_books,
        'user_book_status': user_book_status,
    }
    return render(request, 'books/detail.html', context)


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category, is_published=True).select_related('author')
    categories = Category.objects.all()

    sort = request.GET.get('sort', '-created_at')
    sort_options = ['-created_at', '-views_count', 'title']
    if sort in sort_options:
        books = books.order_by(sort)

    context = {
        'category': category,
        'books': books,
        'categories': categories,
        'selected_sort': sort,
    }
    return render(request, 'books/category.html', context)


def search_view(request):
    query = request.GET.get('q', '').strip()
    format_type = request.GET.get('format', 'html')
    books = []

    if query:
        books = Book.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__name__icontains=query) |
            Q(category__name__icontains=query)
        ).select_related('category', 'author').distinct()[:20]

    # JSON ответ для живого поиска в navbar
    if format_type == 'json':
        results = [
            {
                'title': book.title,
                'url': book.get_absolute_url(),
                'cover': book.get_cover(),
                'category': book.category.name if book.category else '',
            }
            for book in books[:6]
        ]
        return JsonResponse({'results': results})

    context = {
        'query': query,
        'books': books,
        'count': len(books) if query else 0,
    }
    return render(request, 'books/search.html', context)
