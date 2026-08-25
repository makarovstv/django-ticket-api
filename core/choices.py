from django.db import models


class TicketStatus(models.TextChoices):
    NEW = "new", "Новая"
    IN_PROGRESS = "in_progress", "В работе"
    RESOLVED = "resolved", "Решена"
    CLOSED = "closed", "Закрыта"


class TicketPriority(models.TextChoices):
    LOW = "low", "Низкий"
    MEDIUM = "medium", "Средний"
    HIGH = "high", "Высокий"
    CRITICAL = "critical", "Критический"


class TicketCategory(models.TextChoices):
    BUG = "bug", "Ошибка"
    FEATURE = "feature", "Запрос"
    QUESTION = "question", "Вопрос"
    OTHER = "other", "Другое"
