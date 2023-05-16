from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import arrow
import pytz


scheduler = BackgroundScheduler()


def queue_status(bot):
    from derp.commands.prom import QueueLengths

    queue_lengths = QueueLengths()
    response = queue_lengths(["@scheduler", "queues", {}])
    if callable(response):
        response.args["channel"] = "#general"
        now = arrow.now.format("MM-DD HH:mm")
        response.args["title"] = f"Queue Lengths as of {now}"
        response(bot)


def register_queue_job(bot):
    def queue_status_job():
        queue_status(bot)

    scheduler.add_job(
        queue_status_job,
        trigger=CronTrigger(
            year="*",
            month="*",
            day="*",
            hour="*",
            minute="0",
            timezone=pytz.timezone("US/Eastern"),
        ),
    )
