from apscheduler.schedulers.background import BackgroundScheduler
from scraper import get_average_value
import json
import time

def save_average_value():
    average_value = get_average_value()
    with open('/tmp/average_value.json', 'w') as f:
        json.dump({'average': average_value, 'timestamp': time.time()}, f)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(save_average_value, 'interval', minutes=240)
    scheduler.start()
