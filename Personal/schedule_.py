import schedule
import time
from datetime import datetime

def job_every_sec():
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"I'm working every sec... Current time: {current_time}")

def job_every_min():
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"I'm working every min... Current time: {current_time}")

schedule.every(1).seconds.do(job_every_sec)
schedule.every(1).minutes.do(job_every_min)

while True:
    schedule.run_pending()
    time.sleep(0.1)  # Run pending tasks more frequently