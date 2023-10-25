from django.utils import timezone
from .models import Family
from django_q.tasks import async_task

def delete_expired_families():
    current_time = timezone.now()
    expired_families = Family.objects.filter(expiration_date__lte=current_time)
    expired_families.delete()

# Užduoti funkciją na fone naudojant Django-Q
async_task(delete_expired_families)
