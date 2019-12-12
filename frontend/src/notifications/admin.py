from django.contrib import admin

# Register your models here.
from .models import NotificationBox, NotificationItem


class NotificationItemInline(admin.TabularInline):
    model = NotificationItem


class NotificationBoxAdmin(admin.ModelAdmin):
    inlines = [
        NotificationItemInline
    ]

    class Meta:
        model = NotificationBox


admin.site.register(NotificationBox, NotificationBoxAdmin)
