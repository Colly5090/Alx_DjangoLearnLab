from rest_framework import viewsets, permissions, generics, status, response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Posts.
    
    - Allows CRUD operations on posts.
    - Author is automatically assigned from request.user.
    - Uses global pagination and filtering from settings.py.
    - Permissions: Only post owner can edit/delete.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        """
        Assign the logged-in user as author of the post.
        """
        serializer.save(author=self.request.user)

    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if Like.objects.filter(user=user, post=post).exists():
            return response.Response({"detail": "You already liked this post."}, status=400)

        Like.objects.create(user=user, post=post)

        # Create notification
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb="liked your post",
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.id
            )

        return response.Response({"detail": "Post liked successfully."}, status=201)
    

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, post=post).first()

        if not like:
            return response.Response({"detail": "You have not liked this post."}, status=400)

        like.delete()

        content_type = ContentType.objects.get_for_model(post)

        #Remove like notification when unliked
        Notification.objects.filter(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            content_type=content_type,
            object_id=post.id
        ).delete()

        return response.Response({"detail": "Post unliked successfully."}, status=200)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comments.

    - Allows CRUD operations on comments.
    - Author is automatically assigned from request.user.
    - Permissions: Only comment owner can edit/delete.
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Assign the logged-in user as author of the comment.
        """
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    """
    GET /api/feed/
    Returns posts from users the current user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author__in=user.following.all()).order_by('-created_at')