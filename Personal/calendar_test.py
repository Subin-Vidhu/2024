import calendar
import datetime

def display_current_month_calendar():
    """
    Displays the calendar for the current month and highlights today's date.
    """
    now = datetime.datetime.now()
    month_name = calendar.month_name[now.month]
    year = now.year
    today = now.day

    print(f"Calendar for {month_name} {year}")
    month_calendar = calendar.monthcalendar(year, now.month)

    # Print the days of the week
    print("Mo Tu We Th Fr Sa Su")

    for week in month_calendar:
        for day in week:
            if day == 0:
                print("  ", end=" ")
            elif day == today:
                print(f"\033[92m{day:2}\033[0m", end=" ")
            else:
                print(f"{day:2}", end=" ")
        print()

if __name__ == "__main__":
    display_current_month_calendar()