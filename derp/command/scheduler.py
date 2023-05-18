from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
import tomllib
import os.path
import os
import logging


logger = logging.getLogger(__name__)


scheduler = BackgroundScheduler()


def initialize_scheduler(
    bot, schedule_path=os.getenv("DERP_SCHEDULE_PATH", "schedule.toml")
):
    logger.debug("Initializing scheduled jobs from %r", schedule_path)

    try:
        config = load_config(schedule_path)
        register_jobs(bot, config)
    except FileNotFoundError:
        logger.warn("Schedule file not found. No jobs registered with the scheduler.")

    scheduler.start()


def load_config(filename):
    with open(filename, "rb") as f:
        return tomllib.load(f)


class SchedulerRequest:
    def __init__(self, text, user, channel):
        self.text = text
        self.user = user
        self.channel = channel

    def to_dict(self):
        return {
            "payload": {
                "event": {
                    "text": self.text,
                    "user": self.user,
                    "channel": self.channel,
                    "subtype": "scheduled_event",
                }
            }
        }


def register_jobs(bot, config):
    for job, job_config in config["jobs"].items():
        logger.debug("Registering scheduled job %r with config %r", job, job_config)

        def run_job():
            logger.debug("Running scheduled job %r", job)
            req = SchedulerRequest(
                f"<@mention> {job_config['command']}", "@scheduler", "#general"
            )
            bot.handle_request(req)

        triggers = {
            "cron": CronTrigger,
            "date": DateTrigger,
            "interval": IntervalTrigger,
        }

        trigger_klass = triggers[job_config["trigger"]]
        kwargs = job_config["trigger_args"]
        trigger = trigger_klass(**kwargs)

        scheduler.add_job(run_job, trigger=trigger)
