from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.trainings.models import Room
from ..models import User, Student


class StudentAuthSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    uuid = serializers.UUIDField()

    class Errors:
        STUDENT_ALREADY_IN_ROOM = _('Такой никнейм уже используется')
        ROOM_DONT_EXISTS = _('Неправильный UUID комнаты')
        TRAINING_HAS_STARTED = _('Тренинг уже начался')
        TRAINING_HAS_FINISHED = _('Тренинг уже закончился')
        ROOM_IS_OVERFLOW = _(
            'Комната имеет максимальное количество участников',
        )
        YOU_ARE_KICKED = _('Вас удалили из комнаты')

    def validate_uuid(self, uuid: str) -> str:
        if room := Room.objects.filter(uuid=uuid).first():
            if room.is_started:
                raise serializers.ValidationError(
                    self.Errors.TRAINING_HAS_STARTED,
                )
            if room.is_finished:
                raise serializers.ValidationError(
                    self.Errors.TRAINING_HAS_FINISHED,
                )
            if room.students.count() == room.max_students:
                raise serializers.ValidationError(
                    self.Errors.ROOM_IS_OVERFLOW,
                )
            return uuid
        raise serializers.ValidationError(
            self.Errors.ROOM_DONT_EXISTS,
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=f"{validated_data['full_name']}_{validated_data['uuid']}",
        )
        user.set_unusable_password()
        student = Student.objects.create(
            user=user,
            full_name=validated_data['full_name'],
            room=Room.objects.get(uuid=validated_data['uuid']),
        )
        return student

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance.user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        if (
            student :=
            Student.objects.filter(full_name=attrs['full_name']).first()
        ):
            if student.is_kicked:
                raise serializers.ValidationError(
                    self.Errors.YOU_ARE_KICKED,
                )
            if student.room.uuid == attrs['uuid']:
                raise serializers.ValidationError(
                    self.Errors.STUDENT_ALREADY_IN_ROOM,
                )
        return attrs


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'full_name',
            'user',
        )
