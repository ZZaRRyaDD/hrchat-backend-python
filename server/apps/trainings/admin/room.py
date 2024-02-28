from django.contrib import admin

from ..models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        'uuid',
        'trainer',
        'max_students',
        'max_rounds',
        'max_duration_round',
        'is_started',
        'is_finished',
    )
    search_fields = (
        'uuid',
        'max_students',
        'max_rounds',
        'max_duration_round',
    )
