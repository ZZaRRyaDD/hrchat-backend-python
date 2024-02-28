from typing import Final


TIME_TO_WAIT = 20
PASS_MESSAGE = 'Содержимое скрыто'
NORMAL_CLOSE = 1000


class Statuses:
    NOT_STARTED: Final[str] = 'not started'
    STARTED: Final[str] = 'started'
    WAIT: Final[str] = 'wait'


class Actions:
    USER_LIST: Final[str] = 'user_list'
    ROOM_INFO: Final[str] = 'room_info'
    START_TRAINING: Final[str] = 'start_training'
    KICK_UNREADY_STUDENTS: Final[str] = 'kick_unready_students'
    SET_STUDENT_IS_READY: Final[str] = 'set_student_is_ready'
    FINISH_TRAINING: Final[str] = 'finish_training'
    START_ROUND: Final[str] = 'start_round'
    FINISH_ROUND: Final[str] = 'finish_round'
    MESSAGE_SEND: Final[str] = 'message_send'
    TOGGLE_MESSAGE: Final[str] = 'toggle_message'
    KICK_STUDENT: Final[str] = 'kick_student'


class Events:
    ROOM_INFO_RETRIEVED: Final[str] = 'room_info_retrieved'
    USERS_LIST_RETRIEVED: Final[str] = 'users_list_retrieved'
    ALERT_START_TRAINING: Final[str] = 'alert_start_training'
    SYSTEM_KICK_UNREADY_STUDENTS: Final[str] = 'system_kick_unready_students'
    TRAINING_WAS_FINISHED: Final[str] = 'training_was_finished'
    ALERT_START_ROUND: Final[str] = 'alert_start_round'
    ALERT_TIME_OUT: Final[str] = 'alert_time_out'
    ALERT_FINISH_ROUND: Final[str] = 'alert_finish_round'
    MESSAGE_NEW: Final[str] = 'message_new'
    ALERT_TOGGLE_MESSAGE: Final[str] = 'alert_toggle_message'
    KICK_STUDENT_BY_TRAINER: Final[str] = 'kick_student_by_trainer'


class Errors:
    ROOM_NOT_FOUND: Final[str] = 'Комната с таким UUID не существует'
    ROOM_IS_FINISHED: Final[str] = 'Тренинг закончился'

    USER_IS_NOT_AUTHENTICATED: Final[str] = 'Пользователь не авторизирован'
    YOU_ARE_KICKED: Final[str] = 'Вы были удалены из чата тренером'
