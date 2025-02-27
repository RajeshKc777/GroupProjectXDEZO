from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        OFFICE_WORKER = 'OFFICE_WORKER', _('Office Worker')
        INTERN = 'INTERN', _('Intern')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OFFICE_WORKER,
    )
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_office_worker(self):
        return self.role == self.Role.OFFICE_WORKER

    @property
    def is_intern(self):
        return self.role == self.Role.INTERN
