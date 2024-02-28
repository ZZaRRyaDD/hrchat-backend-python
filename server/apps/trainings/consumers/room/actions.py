from datetime import datetime

from asgiref.sync import sync_to_async
from django.core.cache import cache

from .constants import Events, TIME_TO_WAIT
from .queries import RoomQueries, UserQueries
from .services import RoomService, StudentService, MessageService
from ...tasks import kick_unready, continue_round
from ...utils import get_finish_training_results


class RoomActionsMixin:

    async def user_list(self) -> None:
        students = await RoomQueries.get_students_list(
            self.room_uuid,
            is_kicked=False,
        )
        body = {'students': await StudentService.get_students_list(students)}
        await self.response_to_group(Events.USERS_LIST_RETRIEVED, body)

    async def room_info(self) -> None:
        room = await RoomQueries.get_room(self.room_uuid)
        can_send_message = await RoomQueries.can_send_message(
            self.room_uuid,
            self.user.id,
        )
        is_started = await RoomQueries.is_started(self.room_uuid)
        messages = await MessageService.get_list_messages(
            await RoomQueries.get_messages_without_last_round(self.room_uuid),
            await RoomQueries.get_last_round_id(self.room_uuid),
            self.user.id,
        )
        body = {
            'room': await RoomService.get_room_info(room),
            'can_send_message': can_send_message,
            'is_started': is_started,
            'status': await RoomService.get_status_room(
                cache.get(self.group_name),
                is_started,
            ),
            'current_round': await RoomQueries.get_count_rounds(self.room_uuid),
            'messages': messages,
        }
        await self.response_to_user(Events.ROOM_INFO_RETRIEVED, body)

    async def set_student_is_ready(self) -> None:
        await UserQueries.update_student(self.user.id, is_ready=True)

    async def kick_unready_students(self) -> None:
        await self.response_to_group(
            Events.SYSTEM_KICK_UNREADY_STUDENTS,
            {},
        )

    async def start_training(self) -> None:
        if await UserQueries.is_trainer(self.user.id):
            cache.add(self.group_name, str(datetime.now()))
            await RoomQueries.update_room(self.room_uuid, is_started=True)
            body = {'message': 'Training soon will be start'}
            await self.response_to_group(
                Events.ALERT_START_TRAINING,
                body,
            )
            kick_unready.apply_async(
                args=(
                    self.room_uuid,
                    self.group_name,
                ),
                countdown=TIME_TO_WAIT,
            )

    async def finish_training(self) -> None:
        await RoomActionsMixin.finish_round(self)
        if await UserQueries.is_trainer(self.user.id):
            body = {
                'message': 'Training was finished',
                'results': await sync_to_async(get_finish_training_results)(
                    await RoomQueries.get_room(self.room_uuid),
                ),
            }
            await self.response_to_group(Events.TRAINING_WAS_FINISHED, body)
            await RoomQueries.update_room(self.room_uuid, is_finished=True)

    async def finish_round(self) -> None:
        if await RoomQueries.get_count_rounds(self.room_uuid):
            if self.continue_round_task:
                self.continue_round_task.revoke()
            if self.key_round:
                cache.delete(self.key_round)
            messages = await RoomQueries.get_messages_by_last_round(
                self.room_uuid,
            )
            body = {
                'messages': await MessageService.get_list_messages(messages),
            }
            await self.response_to_group(Events.ALERT_FINISH_ROUND, body)

    async def start_round(self) -> None:
        is_trainer = await UserQueries.is_trainer(self.user.id)
        is_started = await RoomQueries.is_started(self.room_uuid)
        count_rounds = await RoomQueries.get_count_rounds(self.room_uuid)
        max_rounds = await RoomQueries.get_max_rounds(self.room_uuid)
        if is_trainer and is_started and count_rounds < max_rounds:
            await RoomActionsMixin.finish_round(self)
            number = await RoomQueries.create_round(self.room_uuid)
            messages = await RoomQueries.get_messages_without_last_round(
                self.room_uuid,
            )
            body = {
                'current_round': number,
                'messages': await MessageService.get_list_messages(messages),
            }
            await self.response_to_group(
                Events.ALERT_START_ROUND,
                body,
            )

    async def message_send(self, body: dict[str, str]) -> None:
        can_send = await RoomQueries.can_send_message(
            self.room_uuid,
            self.user.id,
        )
        if can_send:
            is_trainer = await UserQueries.is_trainer(self.user.id)
            is_right = None if is_trainer else False
            data = {
                'user': self.user.id,
                'is_right': is_right,
                'in_round': await RoomQueries.get_last_round_id(
                    self.room_uuid,
                ),
                'content': body.get('content', None),
            }
            body = {'message': await MessageService.create_message(data)}
            await self.response_to_group(Events.MESSAGE_NEW, body)
            if is_trainer:
                duration = await RoomQueries.get_max_duration_round(
                    self.room_uuid,
                )
                last_round_id = await RoomQueries.get_last_round_id(
                    self.room_uuid,
                )
                self.key_round = f'{self.group_name}_{last_round_id}'
                cache.add(self.key_round, str(datetime.now()))
                self.continue_round_task = continue_round.apply_async(
                    args=(self.group_name, self.key_round),
                    countdown=duration,
                )

    async def toggle_message(self, body: dict[str, int]) -> None:
        if await UserQueries.is_trainer(self.user.id):
            message_id = body['message_id']
            from_active_round = await RoomQueries.message_from_active_round(
                message_id,
                self.room_uuid,
            )
            is_trainer_message = await RoomQueries.is_trainer_message(
                message_id,
            )
            if from_active_round and not is_trainer_message:
                await RoomQueries.toggle_message(message_id)
                await self.response_to_group(
                    Events.ALERT_TOGGLE_MESSAGE,
                    body,
                )

    async def kick_student(self, body: dict[str, int]) -> None:
        is_trainer = await UserQueries.is_trainer(self.user.id)
        is_started = await RoomQueries.is_started(self.room_uuid)
        if is_trainer and is_started:
            await UserQueries.update_student( body['user'], is_kicked=True)
            await self.response_to_group(
                Events.KICK_STUDENT_BY_TRAINER,
                body,
            )
            await RoomActionsMixin.user_list(self)
