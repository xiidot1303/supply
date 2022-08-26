from apscheduler.schedulers.background import BackgroundScheduler
from scheduled_job import storage_job

def start():
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    scheduler.add_job(storage_job.get_products, 'interval', minutes=5)
    scheduler.start()