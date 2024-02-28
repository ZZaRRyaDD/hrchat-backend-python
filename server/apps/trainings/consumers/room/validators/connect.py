from typing import Optional

from django.contrib.auth.models import User

from ....models import Room
from ..constants import Errors
from ..queries import RoomQueries, UserQueries


class ConnectValidation:

    @staticmethod
    async def validate(user: User, room_uuid: str) -> Optional[str]:
        if not user.is_authenticated:
            return Errors.USER_IS_NOT_AUTHENTICATED

        if await UserQueries.is_kicked(user.id):
            return Errors.YOU_ARE_KICKED

        try:
            await RoomQueries.get_room(room_uuid)
        except Room.DoesNotExist:
            return Errors.ROOM_NOT_FOUND

        if await RoomQueries.is_finished(room_uuid):
            return Errors.ROOM_IS_FINISHED
