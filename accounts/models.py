from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "user", "Пользователь"
        MANAGER = "manager", "Менеджер"
        ADMIN = "admin", "Администратор"

    role = models.CharField(
        verbose_name="Роль",
        max_length=16,
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username

    @property
    def is_manager(self) -> bool:
        return self.role in (self.Role.MANAGER, self.Role.ADMIN)

    @property
    def is_admin_role(self) -> bool:
        return self.role == self.Role.ADMIN
