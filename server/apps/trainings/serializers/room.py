from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from ..models import Room


class RoomSerializer(serializers.ModelSerializer):

    class Errors:
        COUNT_NOT_FINISHED_ROUNDS = _(
            'Тренер не может иметь более одного незавершенного чемпионата',
        )

    class Meta:
        model = Room
        fields = (
            'uuid',
            'max_students',
            'max_rounds',
            'max_duration_round',
        )
        read_only_fields = (
            'uuid',
        )

    def validate(self, attrs):
        trainer = self.context['request'].user.trainer
        if trainer.rooms.filter(is_finished=False):
            raise serializers.ValidationError(
                self.Errors.COUNT_NOT_FINISHED_ROUNDS,
            )
        return attrs


class ResultsTrainingParamsSerializer(serializers.Serializer):
    room_uuid = serializers.UUIDField()

    class Errors:
        ROOM_NOT_FOUND = _('Комната не найдена')

    def validate_room_uuid(self, room_uuid) -> str:
        if Room.objects.filter(uuid=room_uuid).exists():
            return room_uuid
        raise serializers.ValidationError(
            self.Errors.ROOM_NOT_FOUND,
        )
