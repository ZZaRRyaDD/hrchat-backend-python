from channels.exceptions import DenyConnection

from apps.common.consumer import BaseConsumer
from .actions import RoomActionsMixin
from .constants import Actions
from .events import RoomEventsMixin
from .validators import ConnectValidation


class ChatConsumer(
    RoomActionsMixin,
    RoomEventsMixin,
    BaseConsumer,
):
    ACTION_MAP = {
        Actions.USER_LIST: RoomActionsMixin.user_list,
        Actions.ROOM_INFO: RoomActionsMixin.room_info,
        Actions.START_TRAINING: RoomActionsMixin.start_training,
        Actions.SET_STUDENT_IS_READY: RoomActionsMixin.set_student_is_ready,
        Actions.KICK_UNREADY_STUDENTS: RoomActionsMixin.kick_unready_students,
        Actions.FINISH_TRAINING: RoomActionsMixin.finish_training,
        Actions.START_ROUND: RoomActionsMixin.start_round,
        Actions.FINISH_ROUND: RoomActionsMixin.finish_round,
        Actions.MESSAGE_SEND: RoomActionsMixin.message_send,
        Actions.TOGGLE_MESSAGE: RoomActionsMixin.toggle_message,
        Actions.KICK_STUDENT: RoomActionsMixin.kick_student,
    }

    async def connect(self):
        self.room_uuid = self.scope['url_route']['kwargs']['chat_uuid']
        self.group_name = f'room_{self.room_uuid}'
        self.user = self.scope['user']
        await self.accept()
        if error := await ConnectValidation.validate(
            self.user,
            self.room_uuid,
        ):
            await self.send_error(error)
            raise DenyConnection()
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await RoomActionsMixin.user_list(self)
        await RoomActionsMixin.room_info(self)
        self.continue_round_task, self.key_round = None, ''

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )
        await self.close()
