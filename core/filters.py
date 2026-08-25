import django_filters

from core.choices import TicketCategory, TicketPriority, TicketStatus
from core.models import Ticket


class TicketFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=TicketStatus.choices)
    priority = django_filters.ChoiceFilter(choices=TicketPriority.choices)
    category = django_filters.ChoiceFilter(choices=TicketCategory.choices)
    assignee = django_filters.NumberFilter(field_name="assignee_id")
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte",
    )

    class Meta:
        model = Ticket
        fields = ("status", "priority", "category", "assignee")
