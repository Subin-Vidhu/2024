import calendar
import datetime

now = datetime.datetime.now()
print(f"Calendar for {calendar.month_name[now.month]} {now.year}")
print(calendar.month(now.year, now.month))