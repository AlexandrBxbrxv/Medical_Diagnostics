from django.contrib import admin, messages
from django.utils.translation import ngettext

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'fullname', 'is_active')
    search_fields = ('fullname', 'email',)
    ordering = ('id', 'fullname',)
    list_filter = ('is_active',)

    actions = ['ban_users']

    @admin.action(description='Ban selected users')
    def ban_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext(
                "%d user banned",
                "%d users banned",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
