from django.db import models
from django.conf import settings


class Post(models.Model):
    """
    Post Model

    Represents a user-created post in the social media system.

    Fields:
    - author: The user who created the post (ForeignKey to CustomUser).
    - title: Title of the post.
    - content: Main body of the post.
    - created_at: Timestamp when the post was created.
    - updated_at: Timestamp when the post was last updated.
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    """
    Comment Model

    Represents a comment made by a user on a specific post.

    Fields:
    - post: The post being commented on.
    - author: The user who wrote the comment.
    - content: The text content of the comment.
    - created_at: Timestamp when the comment was created.
    - updated_at: Timestamp when the comment was last updated.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    """
    Tracks which user liked which post.
    Prevents duplicate likes using UniqueConstraint.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_like')
        ]
        ordering = ['-created_at']