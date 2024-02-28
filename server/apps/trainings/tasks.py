from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from config.celery import app
from .models import Room


@app.task
def kick_unready(room_uuid: str, group_name: str) -> None:
    from django.core.cache import cache
    from .consumers.room.constants import Events

    Room.objects.get(uuid=room_uuid).students.filter(
        is_ready=False,
    ).update(is_kicked=True)
    cache.delete(group_name)
    async_to_sync(get_channel_layer().group_send)(group_name, {
        'type': Events.SYSTEM_KICK_UNREADY_STUDENTS,
    })


@app.task
def continue_round(group_name: str, key: str) -> None:
    from django.core.cache import cache
    from .consumers.room.constants import Events

    cache.delete(key)
    async_to_sync(get_channel_layer().group_send)(group_name, {
        'type': Events.ALERT_TIME_OUT,
        'body': {'message': 'Время вышло'},
    })
