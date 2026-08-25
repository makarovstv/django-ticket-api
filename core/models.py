from django.conf import settings
from django.db import models

from core.choices import TicketCategory, TicketPriority, TicketStatus


class Ticket(models.Model):
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=256,
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=16,
        choices=TicketStatus.choices,
        default=TicketStatus.NEW,
    )
    priority = models.CharField(
        verbose_name="Приоритет",
        max_length=16,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM,
    )
    category = models.CharField(
        verbose_name="Категория",
        max_length=16,
        choices=TicketCategory.choices,
        default=TicketCategory.OTHER,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Автор",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
        verbose_name="Исполнитель",
    )
    created_at = models.DateTimeField(
        verbose_name="Создана",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Обновлена",
        auto_now=True,
    )
    closed_at = models.DateTimeField(
        verbose_name="Закрыта",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"[{self.get_status_display()}] {self.title}"


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Заявка",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    created_at = models.DateTimeField(
        verbose_name="Создан",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author} on #{self.ticket_id}"


class Attachment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="Заявка",
    )
    file = models.FileField(
        verbose_name="Файл",
        upload_to="attachments/%Y/%m/",
    )
    filename = models.CharField(
        verbose_name="Имя файла",
        max_length=256,
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Загрузил",
    )
    uploaded_at = models.DateTimeField(
        verbose_name="Загружен",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"
        ordering = ["uploaded_at"]

    def __str__(self) -> str:
        return self.filename
