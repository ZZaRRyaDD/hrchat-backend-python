from datetime import datetime
from typing import Optional

from channels.db import database_sync_to_async

from apps.users.serializers import StudentSerializer
from apps.trainings.serializers import RoomSerializer, MessageSerializer
from .constants import Statuses, TIME_TO_WAIT, PASS_MESSAGE
from .queries import RoomQueries


class RoomService:

    @staticmethod
    @database_sync_to_async
    def get_room_info(data: dict) -> dict:
        return RoomSerializer(data).data

    @staticmethod
    @database_sync_to_async
    def get_status_room(start_time: Optional[str], is_started: bool) -> str:
        status = Statuses.NOT_STARTED
        if start_time is None and is_started:
            status = Statuses.STARTED
        elif start_time is not None:
            if ((
                datetime.now() - datetime.fromisoformat(start_time)
            ).total_seconds() < TIME_TO_WAIT):
                status = Statuses.WAIT
        return status


class StudentService:

    @staticmethod
    @database_sync_to_async
    def get_students_list(data: dict) -> list:
        return StudentSerializer(data, many=True).data


class MessageService:

    @staticmethod
    @database_sync_to_async
    def create_message(data: dict) -> dict:
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @classmethod
    @database_sync_to_async
    def get_list_messages(
        cls,
        data: dict,
        last_round_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> list:
        data = MessageSerializer(data, many=True).data
        if last_round_id and user_id:
            data = cls.hide_content(data, last_round_id, user_id)
        return data

    @staticmethod
    def hide_content(data: list[dict], last_round_id: int, user_id: int) -> list[dict]:
        trainer_id = RoomQueries.get_trainer_id_by_round(last_round_id)
        for message in data:
            if any([
                message['user'] == trainer_id == user_id,
                message['in_round'] != last_round_id,
            ]):
                continue
            if message['user'] != user_id:
                message['content'] = PASS_MESSAGE
        return data
