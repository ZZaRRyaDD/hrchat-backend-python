from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TrainerAuthSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Errors:
        NOT_TRAINER = _('Пользователь не является тренером')

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_trainer:
            raise serializers.ValidationError(
                self.Errors.NOT_TRAINER,
            )
        return {
            'refresh': validated_data['refresh'],
            'access': validated_data['access'],
        }
