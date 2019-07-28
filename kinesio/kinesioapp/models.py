from django.db import models
from users.models import User
from encrypted_model_fields.fields import EncryptedCharField

PENDING = 'pending'
FINISHED = 'finished'
CANCELLED = 'cancelled'


class Homework(models.Model):
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    periodicity = models.IntegerField()


class HomeworkExercise(models.Model):
    HOMEWORK_SESSION_STATUS_CHOICES = [
        ('P', 'PENDING'),
        ('D', 'DONE'),
        ('C', 'CANCELLED')
    ]

    date = models.DateTimeField()
    number_of_homework_session = models.IntegerField()
    status = models.CharField(max_length=100, choices=HOMEWORK_SESSION_STATUS_CHOICES, default='PENDING')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, null=True)


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    homework_exercise = models.ForeignKey(HomeworkExercise, on_delete=models.CASCADE, null=True)


class Video(models.Model):
    name = models.CharField(max_length=255)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True)


class ClinicalHistory(models.Model):
    CLINICAL_HISTORY_STATUS_CHOICES = [
        ('P', 'PENDING'),
        ('F', 'FINISHED'),
        ('C', 'CANCELLED')
    ]

    date = models.DateTimeField()
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=CLINICAL_HISTORY_STATUS_CHOICES, default='PENDING')
    patient = models.ForeignKey(User, on_delete=models.CASCADE)


class ClinicalSession(models.Model):
    SESSION_STATUS_CHOICES = [
        ('P', 'PENDING'),
        ('F', 'FINISHED'),
        ('C', 'CANCELLED')
    ]
    date = models.DateTimeField()
    status = models.CharField(max_length=100, choices=SESSION_STATUS_CHOICES, default='PENDING')
    homework = models.OneToOneField(Homework, on_delete=models.CASCADE, default=True, blank=True, null=True)
    clinical_history = models.ForeignKey(ClinicalHistory, related_name='clinical_sessions', on_delete=models.CASCADE)


class Image(models.Model):
    content = EncryptedCharField(max_length=9000000)
    description = models.CharField(max_length=255, null=True)
    date = models.DateTimeField()
    clinical_session = models.ForeignKey(ClinicalSession, on_delete=models.CASCADE, null=True)
