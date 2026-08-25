from celery import shared_task
from django.core.mail import send_mail


@shared_task
def notify_ticket_created(ticket_id, author_email, title):
    send_mail(
        subject=f"Новая заявка #{ticket_id}: {title}",
        message=f"Вы создали заявку #{ticket_id}: {title}",
        from_email="noreply@ticketapi.local",
        recipient_list=[author_email],
        fail_silently=True,
    )


@shared_task
def notify_ticket_assigned(ticket_id, assignee_email, title):
    send_mail(
        subject=f"Назначена заявка #{ticket_id}: {title}",
        message=f"Вам назначена заявка #{ticket_id}: {title}",
        from_email="noreply@ticketapi.local",
        recipient_list=[assignee_email],
        fail_silently=True,
    )


@shared_task
def notify_ticket_status_changed(ticket_id, new_status, author_email, title):
    send_mail(
        subject=f"Заявка #{ticket_id}: статус изменён",
        message=f"Заявка #{ticket_id} ({title}) — новый статус: {new_status}",
        from_email="noreply@ticketapi.local",
        recipient_list=[author_email],
        fail_silently=True,
    )
