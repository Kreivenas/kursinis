from django_cron import CronJobBase, Schedule
from datetime import datetime
from pinigai.models import Family 

class DeleteExpiredFamilies(CronJobBase):
    RUN_EVERY_MINS = 60 * 24

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, at="0:14")
    code = 'pinigai.delete_expired_families'

    def do(self):
        current_date = datetime.now()
        Family.objects.filter(expiration_date__lt=current_date).delete()
    def do(self):
        current_date = datetime.now()
        families_to_delete = Family.objects.filter(expiration_date__lt=current_date)
        for family in families_to_delete:
            family_name = family.name
            family.delete()
            print(f"Šeima {family_name} ištrinta.")
