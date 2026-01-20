from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, CheckStockView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:book_id>/check-stock/', CheckStockView.as_view(), name='check-stock'),
]
