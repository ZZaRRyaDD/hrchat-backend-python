from django.contrib import admin


from ..models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        'content',
        'is_right',
        'user',
        'in_round',
        'created_at',
    )
    search_fields = (
        'content',
        'is_right',
        'created_at',
    )
