from rest_framework import generics, permissions

from ..serializers import RoomSerializer
from ..permissions import TrainerPermission


class RoomCreateAPIView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated, TrainerPermission)

    def perform_create(self, serializer):
        serializer.save(trainer=self.request.user.trainer)
