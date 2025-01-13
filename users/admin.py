from django.contrib import admin, messages
from django.utils.translation import ngettext

from users.models import User, Cart, History, Request


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


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'analysis', 'users_appointment',)
    search_fields = ('analysis', 'users_appointment',)
    ordering = ('id',)
    list_filter = ('owner',)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'payment_daytime', 'price', 'result',)
    search_fields = ('service_info', 'result',)
    ordering = ('id', 'payment_daytime', 'price',)
    list_filter = ('owner',)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'speciality', 'date', 'from_time', 'to_time', 'fullname', 'phone_number', 'email',)
    search_fields = ('speciality', 'fullname',)
    ordering = ('id', '-date',)
    list_filter = ('owner',)
