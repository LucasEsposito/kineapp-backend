from django.db import models
from ffmpy import FFmpeg

from kinesioapp.utils.django_server import DjangoServerConfiguration
from users.models import User


class VideoQuerySet(models.QuerySet):
    def accessible_by(self, user: User) -> models.QuerySet:
        return self.filter(owner=user.related_medic)

    def create(self, medic_id: int, **kwargs) -> models.Model:
        video = super().create(owner=User.objects.get(id=medic_id), **kwargs)
        video.generate_thumbnail()
        return video


class Video(models.Model):
    name = models.CharField(max_length=255)
    content = models.FileField(upload_to='')
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = VideoQuerySet.as_manager()

    @property
    def url(self) -> str:
        return f'http://{DjangoServerConfiguration().base_url}{self.content.url}'

    @property
    def thumbnail_url(self) -> str:
        return f'{self.url}_thumb.jpg'

    def can_edit_and_delete(self, user: User) -> bool:
        return self.owner == user

    def can_view(self, user: User) -> bool:
        return self.owner == user.related_medic

    def generate_thumbnail(self) -> None:
        video_file_path = self.content.path
        output_file_path = f'{video_file_path}_thumb.jpg'
        command = FFmpeg(inputs={video_file_path: None},
                         outputs={output_file_path: ['-ss', '00:00:04', '-vframes', '1']})
        command.run()