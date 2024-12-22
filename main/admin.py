from django.contrib import admin

from main.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'date_created', 'is_closed',)
    search_fields = ('fullname', 'email', 'message',)
    ordering = ('id', 'fullname',)
    list_filter = ('is_closed',)
