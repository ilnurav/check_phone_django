from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from phone_checker.management.commands.update_number_ranges import Command


def update_number_ranges():
    cmd = Command()
    cmd.handle()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Ежедневное обновление в 3:00
    scheduler.add_job(
        update_number_ranges,
        trigger="cron",
        hour=3,
        minute=0,
        id="update_number_ranges",
        max_instances=1,
        replace_existing=True,
    )

    # Очистка старых записей каждую неделю
    scheduler.add_job(
        delete_old_job_executions,
        trigger="cron",
        day_of_week="mon",
        hour=0,
        minute=0,
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )

    scheduler.start()