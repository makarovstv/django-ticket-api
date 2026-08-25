from django.contrib import admin

from core.models import Attachment, Comment, Ticket


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("author", "text", "created_at")


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    readonly_fields = ("filename", "uploaded_by", "uploaded_at")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "status",
        "priority",
        "category",
        "author",
        "assignee",
        "created_at",
    )
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at", "closed_at")
    inlines = [CommentInline, AttachmentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "ticket", "author", "created_at")
    search_fields = ("text",)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("pk", "filename", "ticket", "uploaded_by", "uploaded_at")
