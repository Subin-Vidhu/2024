import schedule
import time
from datetime import datetime

def job():
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"I'm working... Current time: {current_time}")

schedule.every().minute.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)