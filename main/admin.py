from django.contrib import admin, messages
from django.utils.translation import ngettext

from main.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'date_created', 'is_closed',)
    search_fields = ('fullname', 'email', 'message',)
    ordering = ('id', 'fullname',)
    list_filter = ('is_closed',)

    actions = ["close_feedback"]

    @admin.action(description="Close selected feedbacks")
    def close_feedback(self, request, queryset):
        updated = queryset.update(is_closed=True)
        self.message_user(
            request,
            ngettext(
                "%d feedback closed",
                "%d feedbacks closed",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
