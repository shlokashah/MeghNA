from apscheduler.schedulers.background import BackgroundScheduler
from BackgroundJobs import nowcast

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(nowcast.updateDetails, 'interval', minutes=0.1)
    scheduler.start()