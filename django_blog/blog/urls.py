from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, ProfileView, HomeView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CreateCommentView, UpdateCommentView, DeleteCommentView, PostsByTagView, SearchView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login', extra_context={'message': 'You have successfully logged out.'}), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/comments/new/', CreateCommentView.as_view(), name='comment-create'),
    path('comments/<int:pk>/edit/', UpdateCommentView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', DeleteCommentView.as_view(), name='comment-delete'),
    path('tags/<slug:tag_slug>/', PostsByTagView.as_view(), name='posts-by-tag'),
    path('search/', SearchView.as_view(), name='search'),
]