from datetime import datetime
from .jobs import job
from apscheduler.schedulers.background import BackgroundScheduler

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'cron', day_of_week = 'mon-fri', hour = 11, minute = 00)
    scheduler.start()