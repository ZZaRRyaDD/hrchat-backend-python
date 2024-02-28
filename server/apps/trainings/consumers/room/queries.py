from typing import Optional

from channels.db import database_sync_to_async
from django.core.cache import cache
from django.db.models import QuerySet

from apps.users.models import User, Trainer, Student
from ...models import Room, Round, Message


class RoomQueries:

    @staticmethod
    @database_sync_to_async
    def can_send_message(room_uuid: str, user_id: int) -> bool:
        room = Room.objects.get(uuid=room_uuid)
        if not room.is_started or room.is_finished:
            return False
        if last_round := room.rounds.order_by('id').last():
            has_trainer_message = last_round.messages.filter(
                user__id=room.trainer.id,
            ).exists()
            if user_id == room.trainer.id and not has_trainer_message:
                return True
            has_user_message = not last_round.messages.filter(
                user__id=user_id,
            ).exists()
            group_name = f'room_{room_uuid}_{last_round.id}'
            return has_user_message and has_trainer_message and bool(cache.get(group_name))
        return False

    @staticmethod
    @database_sync_to_async
    def get_last_round_id(room_uuid: str) -> Optional[int]:
        if last_round := Room.objects.get(uuid=room_uuid).rounds.order_by('id').last():
            return last_round.id
        return None

    @staticmethod
    @database_sync_to_async
    def get_trainer_id_by_round(round_id: int) -> int:
        return Round.objects.get(id=round_id).room.trainer.user.id

    @staticmethod
    @database_sync_to_async
    def get_room(room_uuid: str) -> Room:
        return Room.objects.get(uuid=room_uuid)

    @staticmethod
    @database_sync_to_async
    def is_finished(room_uuid: str) -> bool:
        return Room.objects.get(uuid=room_uuid).is_finished

    @staticmethod
    @database_sync_to_async
    def is_started(room_uuid: str) -> bool:
        return Room.objects.get(uuid=room_uuid).is_started

    @staticmethod
    @database_sync_to_async
    def get_students_list(
        room_uuid: str,
        is_ready: Optional[bool] = None,
        is_kicked: Optional[bool] = None,
    ) -> QuerySet:
        students = Room.objects.get(uuid=room_uuid).students.all()
        if is_ready is not None:
            students = students.filter(is_ready=is_ready)
        if is_kicked is not None:
            students = students.filter(is_kicked=is_kicked)
        return students

    @staticmethod
    @database_sync_to_async
    def get_trainer(room_uuid: str) -> Trainer:
        return Room.objects.get(uuid=room_uuid).trainer

    @staticmethod
    @database_sync_to_async
    def update_room(room_uuid: str, **kwargs) -> None:
        Room.objects.filter(uuid=room_uuid).update(**kwargs)

    @staticmethod
    @database_sync_to_async
    def set_unready(room_uuid: str) -> None:
        Room.objects.get(uuid=room_uuid).students.filter(
            is_ready=False,
        ).update(is_kicked=True)

    @staticmethod
    @database_sync_to_async
    def create_round(room_uuid: str) -> int:
        Round.objects.create(room=Room.objects.get(uuid=room_uuid))
        return Room.objects.get(uuid=room_uuid).rounds.order_by('id').count()

    @staticmethod
    @database_sync_to_async
    def get_count_rounds(room_uuid: str) -> int:
        return Room.objects.get(uuid=room_uuid).rounds.order_by('id').count()

    @staticmethod
    @database_sync_to_async
    def get_max_duration_round(room_uuid: str) -> int:
        return Room.objects.get(uuid=room_uuid).max_duration_round

    @staticmethod
    @database_sync_to_async
    def get_messages_without_last_round(room_uuid: str) -> QuerySet:
        round_ids = list(Round.objects.filter(room__uuid=room_uuid).order_by(
            'id',
        ).values_list(
            'id',
            flat=True,
        ))[:-1]
        return Message.objects.filter(in_round__id__in=round_ids)

    @staticmethod
    @database_sync_to_async
    def get_messages_by_last_round(room_uuid: str) -> QuerySet:
        room = Room.objects.prefetch_related(
            'rounds',
            'rounds__messages',
        ).get(uuid=room_uuid)
        return room.rounds.order_by('id').last().messages.all()

    @staticmethod
    @database_sync_to_async
    def get_message(message_id: int) -> Message:
        return Message.objects.get(id=message_id)

    @staticmethod
    @database_sync_to_async
    def message_from_active_round(message_id: int, room_uuid: str) -> bool:
        room = Room.objects.prefetch_related(
            'rounds',
            'rounds__messages',
        ).get(uuid=room_uuid)
        message = Message.objects.get(id=message_id)
        messages_by_last_round = list(
            room.rounds.order_by('id').last().messages.all(),
        )
        return message in messages_by_last_round

    @staticmethod
    @database_sync_to_async
    def toggle_message(message_id: int) -> None:
        message = Message.objects.get(id=message_id)
        message.is_right = not message.is_right
        message.save()

    @staticmethod
    @database_sync_to_async
    def is_trainer_message(message_id: int) -> bool:
        return Message.objects.get(id=message_id).user.is_trainer

    @staticmethod
    @database_sync_to_async
    def get_max_rounds(room_uuid: str) -> int:
        return Room.objects.get(uuid=room_uuid).max_rounds


class UserQueries:

    @staticmethod
    @database_sync_to_async
    def is_ready(user_id: int) -> bool:
        if Trainer.objects.filter(user__id=user_id).exists():
            return True
        return Student.objects.get(user__id=user_id).is_ready

    @staticmethod
    @database_sync_to_async
    def get_user(user_id: int):
        return User.objects.get(id=user_id)

    @staticmethod
    @database_sync_to_async
    def get_id_kicked_students(room_uuid: str) -> list:
        return Student.objects.filter(
            room__uuid=room_uuid,
            is_kicked=True,
        ).values_list('user__id', flat=True)

    @staticmethod
    @database_sync_to_async
    def is_trainer(user_id: int) -> bool:
        return User.objects.get(id=user_id).is_trainer

    @staticmethod
    @database_sync_to_async
    def is_kicked(user_id: int) -> bool:
        user = User.objects.get(id=user_id)
        if user.is_trainer:
            return False
        return user.student.is_kicked

    @staticmethod
    @database_sync_to_async
    def update_student(user_id: int, **kwargs) -> None:
        Student.objects.filter(user__id=user_id).update(**kwargs)
