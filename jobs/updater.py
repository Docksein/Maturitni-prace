from datetime import datetime
from .jobs import job
from apscheduler.schedulers.background import BackgroundScheduler

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'cron', day_of_week = 'mon', hour = 11, minute = 30)
    scheduler.start()