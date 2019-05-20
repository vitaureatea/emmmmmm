import os
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpserver.settings')
import django
django.setup()

# jobstores = {
#     'eazyops': RedisJobStore(db=5,
#                              host='127.0.0.1',
#                              port=6379,
#                              password='')
# }
#
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(5)
# }
#
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 5
# }
scheduler = BackgroundScheduler()
#scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler.add_jobstore(DjangoJobStore(), 'eazyops')
#scheduler.start()
register_events(scheduler)

