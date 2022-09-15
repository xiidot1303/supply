from apscheduler.schedulers.background import BackgroundScheduler
from scheduled_job import storage_job, statement_job

def start():
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    scheduler.add_job(storage_job.get_products, 'interval', minutes=5)
    scheduler.add_job(statement_job.cancel_overdue_statements, 'interval', minutes=30)
    scheduler.start()