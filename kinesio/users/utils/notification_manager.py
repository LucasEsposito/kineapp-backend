from pyfcm import FCMNotification
from django.conf import settings
import logging

from ..models import User
from .singleton import Singleton


class NotificationManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.firebase_connector = FCMNotification(api_key=settings.FIREBASE_API_KEY)

    def _send_notification(self, user: User, title: str, body: str) -> None:
        if user.firebase_device_id:
            self.firebase_connector.notify_single_device(registration_id=user.firebase_device_id,
                                                         message_title=title,
                                                         message_body=body)
        else:
            logging.info(f'The user {user} has no firebase_device_id.')

    def routine_changed(self, user: User) -> None:
        self._send_notification(user,
                                'Cambios en tu rutina',
                                'Tu médico ha realizado modificaciones a tu rutina de ejercicios.')

    def send_exercise_reminder(self, exercise) -> None:
        self._send_notification(exercise.patient.user,
                                f'Recordá hacer {exercise.name}!',
                                f'{exercise.description}')
