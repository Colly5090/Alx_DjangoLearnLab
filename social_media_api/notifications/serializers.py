from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source='actor.username')

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'is_read', 'timestamp']
        read_only_fields = fields