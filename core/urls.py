from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.viewsets import AttachmentViewSet, CommentViewSet, TicketViewSet

router = DefaultRouter()
router.register("tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "tickets/<int:ticket_pk>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="ticket-comments",
    ),
    path(
        "tickets/<int:ticket_pk>/attachments/",
        AttachmentViewSet.as_view({"get": "list", "post": "create"}),
        name="ticket-attachments",
    ),
]
