from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from digitalmarket.mixins import AjaxRequiredMixin
from notifications.models import NotificationBox, NotificationItem


class NotificationBoxView(LoginRequiredMixin, View):
    """
        Displays notification box.
        
        (LoginRequiredMixin, View)
        
        :model:`notifications.NotificationBox`
        
        **Context**
        
        :model:`notifications.NotificationBox`
        
        ``box``: notification box which belongs to user
        
        **Template**
        
        :template:`notifications/notifications_box.html`
        
        """
    model = NotificationBox
    template_name = "notifications/notifications_box.html"

    def get(self, request, *args, **kwargs):
        try:
            notification_box = request.user.notification_box
        except Exception:
            notification_box = None

        context = {
            "box": notification_box
        }
        template = self.template_name
        return render(request, template, context)


class NotificationUpdateView(LoginRequiredMixin, AjaxRequiredMixin, View):
    """
        update notifications (such as switching between read and unread)
        """
    def update_notification(self, request, notification, action):
        if not notification.belongs_to_user(request.user):
            data = {
                'success': False,
                'errorCode': '401',
                'errorMsg': 'Not authorized',
                'error': 'Notification does not belong to user'
            }
            return JsonResponse(data=data)

        if action == "read":
            notification.read = True
            notification.save()
        elif action == "unread":
            notification.read = False
            notification.save()
        elif action == "archive":
            notification.read = True
            notification.archived = True
            notification.save()

        data = {
            'success': True
        }

        return JsonResponse(data=data)

    def update_all_notifications(self, request, action):
        notifications = request.user.notification_box.notifications.filter(archived=False)

        if action == "read":
            notifications.update(read=True)
        elif action == "unread":
            notifications.update(read=False)
        elif action == "archive":
            notifications.update(read=True, archived=True)

        for notification in notifications:
            notification.save()

        data = {
            'success': True
        }
        return JsonResponse(data=data)

    def put(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            action = kwargs['action']
            return self.update_all_notifications(request, action)
        else:
            pk = kwargs['pk']
            action = kwargs['action']
            notification = NotificationItem.objects.get(pk=pk)

            return self.update_notification(request, notification, action)
