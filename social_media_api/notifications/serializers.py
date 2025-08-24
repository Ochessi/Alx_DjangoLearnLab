from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField(read_only=True)
    actor_id = serializers.IntegerField(source='actor.id', read_only=True)
    recipient = serializers.StringRelatedField(read_only=True)
    recipient_id = serializers.IntegerField(source='recipient.id', read_only=True)
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_id', 'actor', 'actor_id',
            'verb', 'target', 'target_repr', 'unread', 'timestamp'
        ]

    def get_target_repr(self, obj):
        # human friendly representation of target if possible
        try:
            return str(obj.target)
        except Exception:
            return None
