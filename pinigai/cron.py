from django_cron import CronJobBase, Schedule
from models import Family 
from django.utils import timezone


class DeleteExpiredFamilies(CronJobBase):
    RUN_EVERY_MINS = 60 * 24

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, at="00:00")
    code = 'pinigai.delete_expired_families'

    def do(self):
        families_to_delete = Family.objects.filter(expiration_date__lt=timezone.now())
        for family in families_to_delete:
            family_name = family.name
            family.delete()
            print(f"Fondas {family_name} ištrintas.")
