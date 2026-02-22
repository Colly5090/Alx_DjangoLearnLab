from django.urls import path
from .views import list_books, LibraryDetailView, RegisterView, UserLoginView, UserLogoutView, admin_view, librarian_view, member_view
from . import views

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
    path('books/add/', views.add_book, name='book-add'),
    path('books/edit/<int:pk>', views.edit_book, name='book-edit'),
    path('books/<int:pk>/delete/', views.delete_book, name='book-delete'),
]