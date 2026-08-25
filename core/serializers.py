from rest_framework import serializers

from accounts.serializers import UserSerializer
from core.models import Attachment, Comment, Ticket


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "ticket", "author", "text", "created_at")
        read_only_fields = ("id", "author", "created_at")


class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = Attachment
        fields = ("id", "ticket", "file", "filename", "uploaded_by", "uploaded_at")
        read_only_fields = ("id", "uploaded_by", "uploaded_at", "filename")


class TicketListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id", "title", "status", "priority", "category",
            "author", "assignee", "comments_count",
            "created_at", "updated_at",
        )


class TicketDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id", "title", "description", "status", "priority", "category",
            "author", "assignee", "comments", "attachments",
            "created_at", "updated_at", "closed_at",
        )
        read_only_fields = ("id", "author", "created_at", "updated_at", "closed_at")


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "title", "description", "priority", "category")
        read_only_fields = ("id",)


class AssignSerializer(serializers.Serializer):
    assignee_id = serializers.IntegerField()
