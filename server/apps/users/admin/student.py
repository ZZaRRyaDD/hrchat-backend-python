from django.contrib import admin

from ..models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'is_ready',
        'room',
        'is_kicked',
        'full_name',
    )
    search_fields = (
        'user',
        'is_ready',
        'is_kicked',
        'full_name',
    )
