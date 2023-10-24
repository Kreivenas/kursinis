from django_cron import CronJobBase, Schedule
from datetime import datetime
from pinigai.models import Family 

class DeleteExpiredFamilies(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'pinigai.delete_expired_families'

    def do(self):
        current_date = datetime.now()
        Family.objects.filter(expiration_date__lt=current_date).delete()
