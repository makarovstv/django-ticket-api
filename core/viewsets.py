import logging

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.choices import TicketStatus
from core.models import Attachment, Comment, Ticket
from core.permissions import IsManagerOrAdmin, IsOwnerOrManager
from core.serializers import (
    AttachmentSerializer,
    CommentSerializer,
    TicketCreateSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
)
from core.tasks import (
    notify_ticket_assigned,
    notify_ticket_created,
    notify_ticket_status_changed,
)

logger = logging.getLogger(__name__)


class TicketViewSet(viewsets.ModelViewSet):
    """Заявки — создание, просмотр, назначение, закрытие."""

    permission_classes = [IsAuthenticated, IsOwnerOrManager]
    tags = ["tickets"]

    def get_queryset(self):
        qs = Ticket.objects.select_related(
            "author", "assignee",
        ).prefetch_related("comments")
        if self.request.user.is_manager:
            return qs
        return qs.filter(author=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "create":
            return TicketCreateSerializer
        return TicketDetailSerializer

    def perform_create(self, serializer):
        ticket = serializer.save(author=self.request.user)
        notify_ticket_created.delay(
            ticket.pk,
            self.request.user.email,
            ticket.title,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsManagerOrAdmin],
        description="Назначить исполнителя на заявку",
    )
    def assign(self, request, pk=None):
        ticket = self.get_object()
        from accounts.models import User

        assignee_id = request.data.get("assignee_id")
        try:
            assignee = User.objects.get(pk=assignee_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ticket.assignee = assignee
        ticket.status = TicketStatus.IN_PROGRESS
        ticket.save(update_fields=["assignee", "status", "updated_at"])

        notify_ticket_assigned.delay(ticket.pk, assignee.email, ticket.title)
        return Response(TicketDetailSerializer(ticket).data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsOwnerOrManager],
        description="Закрыть заявку",
    )
    def close(self, request, pk=None):
        ticket = self.get_object()
        ticket.status = TicketStatus.CLOSED
        ticket.closed_at = timezone.now()
        ticket.save(update_fields=["status", "closed_at", "updated_at"])

        if ticket.author.email:
            notify_ticket_status_changed.delay(
                ticket.pk, "closed", ticket.author.email, ticket.title,
            )
        return Response(TicketDetailSerializer(ticket).data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        description="Статистика по заявкам",
    )
    def statistics(self, request):
        qs = self.get_queryset()
        stats = qs.aggregate(
            total=Count("id"),
            new=Count("id", filter=Q(status="new")),
            in_progress=Count("id", filter=Q(status="in_progress")),
            resolved=Count("id", filter=Q(status="resolved")),
            closed=Count("id", filter=Q(status="closed")),
        )
        return Response(stats)


class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Комментарии к заявкам."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    tags = ["comments"]

    def get_queryset(self):
        return Comment.objects.filter(
            ticket_id=self.kwargs["ticket_pk"],
        ).select_related("author")

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            ticket_id=self.kwargs["ticket_pk"],
        )


class AttachmentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вложения к заявкам."""

    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    tags = ["attachments"]

    def get_queryset(self):
        return Attachment.objects.filter(ticket_id=self.kwargs["ticket_pk"])

    def perform_create(self, serializer):
        file = self.request.FILES.get("file")
        serializer.save(
            uploaded_by=self.request.user,
            ticket_id=self.kwargs["ticket_pk"],
            filename=file.name if file else "",
        )
