from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    Automatically assigns the logged-in user as the author.
    """
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_title(self, value):
        """
        Field-specific validation for title.
        """
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 255:
            raise serializers.ValidationError("Title cannot exceed 255 characters.")
        return value

    def validate_content(self, value):
        """
        Field-specific validation for content.
        """
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    Automatically assigns logged-in user as author.
    """
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_content(self, value):
        """
        Ensure comment is not empty and not just whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        if len(value) > 1000:
            raise serializers.ValidationError("Comment cannot exceed 1000 characters.")
        return value

    def validate(self, data):
        """
        Object-level validation.
        """
        # Example: you could prevent comments on deleted posts
        post = data.get('post')
        if not post:
            raise serializers.ValidationError("Comment must be associated with a valid post.")
        return data