from rest_framework import serializers

from ..models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'id',
            'content',
            'is_right',
            'user',
            'in_round',
            'created_at',
        )
        read_only_fields = (
            'id',
            'created_at',
        )
