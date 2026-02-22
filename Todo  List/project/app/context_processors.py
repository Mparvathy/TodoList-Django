from django.utils import timezone
from .models import Task

def task_notifications(request):
    if request.user.is_authenticated:
        today = timezone.now().date()

        due_today_tasks = Task.objects.filter(
            user=request.user,
            status='running',
            due_date=today
        )

        expired_tasks = Task.objects.filter(
            user=request.user,
            status='running',
            due_date__lt=today
        )

        return {
            'due_today_tasks': due_today_tasks,
            'expired_tasks': expired_tasks,
            'notification_count': due_today_tasks.count() + expired_tasks.count()
        }

    return {
        'due_today_tasks': [],
        'expired_tasks': [],
        'notification_count': 0
    }
