from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models, transaction
from django.conf import settings


class SecretQuestion(models.Model):
    description = models.CharField(max_length=255)


class UserQuerySet(models.QuerySet):
    def medics(self):
        return self.exclude(medic__isnull=True)

    def patients(self):
        return self.exclude(patient__isnull=True)


class MedicManager(models.Manager):
    def _fixed_license(self, license):
        if license is not None:
            license = license.strip() if license.strip() != '' else None
        return license

    def create(self, user, license, **kwargs):
        return super().create(user=user, license=self._fixed_license(license), **kwargs)


class UserManager(DjangoUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def _fixed_license(self, license):
        if license is not None:
            license = license.strip() if license.strip() != '' else None
        return license

    def create_user(self, username, license=None, current_medic=None, **kwargs):
        with transaction.atomic():
            user = super().create_user(username,  **kwargs)
            if license is not None:
                Medic.objects.create(pk=user.pk, id=user.id, user=user, license=license)
            else:
                Patient.objects.create(pk=user.pk, id=user.id, user=user, current_medic=current_medic)
        return user

    def patients(self):
        return self.get_queryset().patients()

    def medics(self):
        return self.get_queryset().medics()


class User(AbstractUser):
    secret_question = models.ForeignKey(SecretQuestion, null=True, on_delete=models.SET_NULL)
    tries = models.IntegerField(default=0)
    birth_day = models.DateTimeField(default=None, null=True)
    gender = models.CharField(max_length=1, default=None, null=True)
    photo = models.BinaryField(default=None, null=True)
    dni = models.CharField(max_length=10, default=None, null=True)

    objects = UserManager()

    def log_valid_try(self):
        self.tries = 0
        self.save()

    def log_invalid_try(self):
        self.tries += 1
        if self.tries >= settings.MAX_PASSWORD_TRIES:
            self.is_active = False
        self.save()

    @property
    def is_patient(self):
        try:
            self.patient
            return True
        except Patient.DoesNotExist:
            return False

    @property
    def is_medic(self):
        # We can not do "return not self.is_patient" because during the first save, the user doesn't have a type.
        try:
            self.medic
            return True
        except Medic.DoesNotExist:
            return False

    @property
    def type(self):
        if self.is_patient:
            return self.patient
        elif self.is_medic:
            return self.medic
        else:
            return None

    @property
    def related_patients(self):
        return self.type.related_patients

    def __str__(self):
        return f'{"Dr." if self.is_medic else "Pac."} {self.last_name}, {self.first_name}'


class Medic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license = models.CharField(max_length=100)

    objects = MedicManager()

    @property
    def related_patients(self) -> [User]:
        return User.objects.filter(id__in=self.user.patients.values('id'))


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    current_medic = models.ForeignKey(User, related_name='patients', on_delete=models.SET_NULL,
                                      default=None, blank=True, null=True)

    @property  # Just for Lean until he fixes something
    def videos(self):
        return []

    @property
    def related_patients(self) -> [User]:
        return User.objects.filter(id=self.user.id)
