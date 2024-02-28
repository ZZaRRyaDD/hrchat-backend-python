from rest_framework import permissions

from ..models import Room


class TrainerPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if uuid := request.parser_context['kwargs'].get('room_uuid', None):
            if room := Room.objects.filter(uuid=uuid).first():
                return room.trainer.user == request.user
        return request.user.is_trainer
