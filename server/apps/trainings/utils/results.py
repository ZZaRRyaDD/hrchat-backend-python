from typing import Union

import openpyxl
from django.db.models import Count, Q

from ..constants import ResultsTraining
from ..models import Room


def get_key(results: dict[str, int], indexes: list[bool]) -> str:
    return ', '.join([
        list(results.keys())[index]
        for index, value in enumerate(indexes)
        if value
    ])


def get_answered_info(room: Room) -> dict[str, int]:
    right_answered = room.students.filter(is_kicked=False).annotate(
        is_right_messages_count=Count(
            'user__messages',
            filter=Q(user__messages__is_right=True),
        ),
    ).values('full_name', 'is_right_messages_count')
    answered = dict([(student.values()) for student in right_answered])
    new_results = {}
    for points in list(set(answered.values()))[::-1]:
        indexes = list(value == points for value in answered.values())
        new_results[get_key(answered, indexes)] = points
    return new_results


def get_kicked(room: Room) -> dict[str, str]:
    return dict([
        (item['full_name'], ResultsTraining.STATUS_KICKED)
        for item in list(room.students.filter(is_kicked=True).values(
            'full_name',
        ))
    ])


def get_results(room: Room) -> dict[str, Union[str, int]]:
    results = {}
    results.update(get_answered_info(room))
    results.update(get_kicked(room))
    return results


def get_finish_training_results(room: Room) -> str:
    members = [
        f'{key} - {value}\n' for key, value in get_results(room).items()
    ]
    return 'Результаты тренинга:\n' + ''.join(members)


def get_results_training(room: Room, filename: str) -> None:
    results = get_results(room)
    workbook = openpyxl.Workbook()
    sheet = workbook.create_sheet(
        title=ResultsTraining.SHEET_NAME,
        index=0,
    )
    sheet['A1'] = ResultsTraining.PLACE_NAME
    sheet['B1'] = ResultsTraining.NAME_NAME
    sheet['C1'] = ResultsTraining.RESULT_NAME
    for index, students in enumerate(list(results.keys()), 2):
        sheet[f'A{index}'] = index - 1
        sheet[f'B{index}'] = students
        sheet[f'C{index}'] = results[students]
    workbook.save(filename=filename)
