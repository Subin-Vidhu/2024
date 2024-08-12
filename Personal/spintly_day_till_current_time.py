import pandas as pd
from datetime import datetime, time, timedelta

# Load the data from the Excel file
FILE_PATH = r'c:\Users\Subin-PC\Downloads\subin_july.xlsx'
# FILE_PATH = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\chippy.xlsx'
SHEET_NAME = 'Access History'
SKIP_ROWS = 5

# Define office hours
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)

# Define target time
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds


def parse_datetime(date, time_str):
    """Parse datetime from date and time strings"""
    return datetime.strptime(f"{date} {time_str.split('(')[0].strip()}", "%b %d, %Y %I:%M:%S %p")
def calculate_time_spent(group, current_time=None):
    """Calculate time spent in office"""
    total_time = 0
    total_office_hours_time = 0
    entry_time = None

    for _, row in group.iterrows():
        if row['Direction'] == 'entry':
            entry_time = row['DateTime']
        elif row['Direction'] == 'exit' and entry_time:
            exit_time = row['DateTime']
            duration = (exit_time - entry_time).total_seconds()
            total_time += duration

            # Calculate time during office hours
            entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=OFFICE_START.hour, minute=OFFICE_START.minute, second=0))
            exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=OFFICE_END.hour, minute=OFFICE_END.minute, second=0))

            if entry_time_within_office_hours < exit_time_within_office_hours:
                duration_office_hours = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
                total_office_hours_time += duration_office_hours

            entry_time = None

    # If there's an open entry without an exit, calculate the time till the current time
    if entry_time and current_time:
        exit_time = current_time
        duration = (exit_time - entry_time).total_seconds()
        total_time += duration

        # Calculate time during office hours
        entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=OFFICE_START.hour, minute=OFFICE_START.minute, second=0))
        exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=OFFICE_END.hour, minute=OFFICE_END.minute, second=0))

        if entry_time_within_office_hours < exit_time_within_office_hours:
            duration_office_hours = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
            total_office_hours_time += duration_office_hours

    return total_time, total_office_hours_time

def get_time_spent_on_date(date_str):
    """Get time spent in office on a specific date"""
    try:
        # Normalize the input by adding a space after the comma if not present
        if ',' in date_str and not date_str[date_str.index(',') + 1].isspace():
            date_str = date_str[:date_str.index(',') + 1] + ' ' + date_str[date_str.index(',') + 1:].strip()
        date = datetime.strptime(date_str, "%b %d, %Y")
    except ValueError:
        print("Invalid date format. Please use 'MMM DD, YYYY' format.")
        return

    time_spent = {}
    current_time = datetime.now()  # Get current time
    for name, group in df.groupby('Name'):
        for group_date, group_by_date in group.groupby('Date'):
            if group_date == date:
                # Calculate time till the last recorded exit
                daily_total_time, daily_office_hours_time = calculate_time_spent(group_by_date)
                
                # Calculate time till the current time
                current_total_time, current_office_hours_time = calculate_time_spent(group_by_date, current_time=current_time)
                
                if name not in time_spent:
                    time_spent[name] = {}
                time_spent[name][date] = {
                    'total_time': daily_total_time,
                    'office_hours_time': daily_office_hours_time,
                    'current_total_time': current_total_time,
                    'current_office_hours_time': current_office_hours_time
                }

    if not time_spent:
        print(f"No data available for {date_str}.")
        return

    print(f"\nTime spent in office on {date_str}:")
    for name, dates in time_spent.items():
        for date in dates:
            total_seconds = dates[date]['total_time']
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"  {name}: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

    print(f"\nTime spent in office during office hours (7:30 AM to 7:30 PM) on {date_str}:")
    for name, dates in time_spent.items():
        for date in dates:
            total_seconds = dates[date]['office_hours_time']
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"  {name}: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

            # Check if target time is met
            if total_seconds >= TARGET_TIME:
                extra_time = total_seconds - TARGET_TIME
                extra_hours, extra_remainder = divmod(extra_time, 3600)
                extra_minutes, extra_seconds = divmod(extra_remainder, 60)
                print(f"  {name} has met the target time of {divmod(TARGET_TIME, 3600)[0]} hours and {divmod(TARGET_TIME, 3600)[1]// 60} minutes with {int(extra_hours)} hours, {int(extra_minutes)} minutes, {int(extra_seconds)} seconds extra.")
            else:
                remaining_time = TARGET_TIME - total_seconds
                remaining_hours, remaining_remainder = divmod(remaining_time, 3600)
                remaining_minutes, remaining_seconds = divmod(remaining_remainder, 60)
                print(f"  {name} has not met the target time of 8 hours 30 minutes. Remaining time: {int(remaining_hours)} hours, {int(remaining_minutes)} minutes, {int(remaining_seconds)} seconds.")

    print(f"\nTime spent in office till the current time on {date_str}:")
    for name, dates in time_spent.items():
        for date in dates:
            total_seconds = dates[date]['current_total_time']
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"  {name}: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

    print(f"\nTime spent in office during office hours (7:30 AM to 7:30 PM) till the current time on {date_str}:")
    for name, dates in time_spent.items():
        for date in dates:
            total_seconds = dates[date]['current_office_hours_time']
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"  {name}: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

            # Check if target time is met
            if total_seconds >= TARGET_TIME:
                extra_time = total_seconds - TARGET_TIME
                extra_hours, extra_remainder = divmod(extra_time, 3600)
                extra_minutes, extra_seconds = divmod(extra_remainder, 60)
                print(f"  {name} has met the target time of {divmod(TARGET_TIME, 3600)[0]} hours and {divmod(TARGET_TIME, 3600)[1]// 60} minutes with {int(extra_hours)} hours, {int(extra_minutes)} minutes, {int(extra_seconds)} seconds extra.")
            else:
                remaining_time = TARGET_TIME - total_seconds
                remaining_hours, remaining_remainder = divmod(remaining_time, 3600)
                remaining_minutes, remaining_seconds = divmod(remaining_remainder, 60)
                print(f"  {name} has not met the target time of 8 hours 30 minutes. Remaining time: {int(remaining_hours)} hours, {int(remaining_minutes)} minutes, {int(remaining_seconds)} seconds.")

# Load the data from the Excel file
df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME, skiprows=SKIP_ROWS)

# Parse the DateTime column
df['DateTime'] = df.apply(lambda row: parse_datetime(row['Date'], row['Time']), axis=1)

# Convert Date column to datetime for proper sorting
df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

# Filter for relevant columns and sort the data by Name and DateTime
df = df[['Date', 'DateTime', 'Name', 'Direction']].sort_values(by=['Name', 'DateTime'])

# Get user input
user_date = input("Enter the date (MMM DD, YYYY): ").strip()
get_time_spent_on_date(user_date)