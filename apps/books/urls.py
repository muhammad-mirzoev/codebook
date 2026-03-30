from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('books/', views.books_list_view, name='books_list'),
    path('books/search/', views.search_view, name='search'),
    path('books/<slug:slug>/', views.book_detail_view, name='book_detail'),
    path('category/<slug:slug>/', views.category_view, name='category'),
]
