from .queries import RoomQueries, UserQueries
from .constants import PASS_MESSAGE, NORMAL_CLOSE


class RoomEventsMixin:

    async def room_info_retrieved(self, event: dict) -> None:
        await self.send_event_response(event)

    async def users_list_retrieved(self, event: dict) -> None:
        await self.send_event_response(event)

    async def alert_start_training(self, event: dict) -> None:
        await self.send_event_response(event)

    async def system_kick_unready_students(self, event: dict) -> None:
        is_ready = await UserQueries.is_ready(self.user.id)
        if not is_ready:
            await self.send_event_response(event)
            await self.disconnect(close_code=NORMAL_CLOSE)
        else:
            await self.send_event_response(event)

    async def training_was_finished(self, event: dict) -> None:
        await self.send_event_response(event)
        await self.disconnect(close_code=NORMAL_CLOSE)

    async def alert_start_round(self, event: dict) -> None:
        await self.send_event_response(event)

    async def alert_finish_round(self, event: dict) -> None:
        await self.send_event_response(event)

    async def alert_time_out(self, event: dict) -> None:
        await self.send_event_response(event)

    async def message_new(self, event: dict) -> None:
        user_id = event['body']['message']['user']
        is_trainer_message = await UserQueries.is_trainer(user_id)
        is_trainer_user = await UserQueries.is_trainer(self.user.id)
        message = await RoomQueries.get_message(
            event['body']['message']['id'],
        )
        event['body']['message']['content'] = message.content
        if all([
            not is_trainer_user, not is_trainer_message, user_id != self.user.id,
        ]):
            event['body']['message']['content'] = PASS_MESSAGE
        await self.send_event_response(event)

    async def alert_toggle_message(self, event: dict) -> None:
        await self.send_event_response(event)

    async def kick_student_by_trainer(self, event: dict) -> None:
        if self.user.id == event['body']['user']:
            await self.send_event_response(event)
            await self.disconnect(close_code=NORMAL_CLOSE)
        await self.send_event_response(event)
