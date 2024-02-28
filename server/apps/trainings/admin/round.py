from django.contrib import admin

from ..models import Round


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = (
        'room',
    )
