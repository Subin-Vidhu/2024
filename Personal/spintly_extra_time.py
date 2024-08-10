import pandas as pd
from datetime import datetime, time, timedelta

# Load the data from the Excel file
file_path = r'c:\Users\Subin-PC\Downloads\subin_july.xlsx'
df = pd.read_excel(file_path, sheet_name='Access History', skiprows=5)

# Function to parse datetime
def parse_datetime(date, time_str):
    return datetime.strptime(f"{date} {time_str.split('(')[0].strip()}", "%b %d, %Y %I:%M:%S %p")

# Parse the DateTime column
df['DateTime'] = df.apply(lambda row: parse_datetime(row['Date'], row['Time']), axis=1)

# Convert Date column to datetime for proper sorting
df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

# Filter for relevant columns and sort the data by Name and DateTime
df = df[['Date', 'DateTime', 'Name', 'Direction']].sort_values(by=['Name', 'DateTime'])

# Define office hours and standard workday duration
office_start = time(7, 30)
office_end = time(19, 30)
standard_workday_seconds = (8 * 60 + 30) * 60  # 8 hours and 30 minutes in seconds

# Function to calculate time spent inside office during office hours
def calculate_time_spent(group):
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
            entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=office_start.hour, minute=office_start.minute, second=0))
            exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=office_end.hour, minute=office_end.minute, second=0))

            if entry_time_within_office_hours < exit_time_within_office_hours:
                duration_office_hours = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
                total_office_hours_time += duration_office_hours

            entry_time = None

    return total_time, total_office_hours_time

# Function to check if a date is a weekend
def is_weekend(date):
    return date.weekday() >= 5  # 5 = Saturday, 6 = Sunday

# Calculate time spent in office
time_spent = {}
total_extra_time = 0
total_extra_office_hours_time = 0

# Calculate time spent in office excluding weekends
time_spent_excluding_weekends = {}
total_extra_time_excluding_weekends = 0
total_extra_office_hours_time_excluding_weekends = 0

for name, group in df.groupby('Name'):
    if name not in time_spent:
        time_spent[name] = {}
        time_spent_excluding_weekends[name] = {}

    for date, group_by_date in group.groupby('Date'):
        daily_total_time, daily_office_hours_time = calculate_time_spent(group_by_date)
        time_spent[name][date] = {
            'total_time': daily_total_time,
            'office_hours_time': daily_office_hours_time
        }

        # Calculate extra time
        extra_time = daily_total_time - standard_workday_seconds
        extra_office_hours_time = daily_office_hours_time - standard_workday_seconds

        if extra_time > 0:
            total_extra_time += extra_time
        if extra_office_hours_time > 0:
            total_extra_office_hours_time += extra_office_hours_time

        # Exclude weekends
        if not is_weekend(date):
            time_spent_excluding_weekends[name][date] = {
                'total_time': daily_total_time,
                'office_hours_time': daily_office_hours_time
            }

            if extra_time > 0:
                total_extra_time_excluding_weekends += extra_time
            if extra_office_hours_time > 0:
                total_extra_office_hours_time_excluding_weekends += extra_office_hours_time

# Print the result in hours, minutes, and seconds
def print_time_spent(time_spent, title):
    print(title)
    for name, dates in time_spent.items():
        print(f"\n{name}:")
        for date in sorted(dates):
            total_seconds = dates[date]['total_time']
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"  {date.strftime('%b %d, %Y')}: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

def print_extra_time_spent(time_spent, title):
    print(title)
    for name, dates in time_spent.items():
        print(f"\n{name}:")
        for date in sorted(dates):
            total_seconds = dates[date]['total_time']
            extra_time = total_seconds - standard_workday_seconds
            if extra_time > 0:
                hours, remainder = divmod(extra_time, 3600)
                minutes, seconds = divmod(remainder, 60)
                print(f"  {date.strftime('%b %d, %Y')}: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds extra")
            else:
                print(f"  {date.strftime('%b %d, %Y')}: No extra time")

def print_total_extra_time(title, total_extra_time):
    print(title)
    hours, remainder = divmod(total_extra_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"  {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds extra")

# Printing the results
# print_time_spent(time_spent, "Total time spent in office for each date:")
# print_time_spent(time_spent, "\nTotal time spent in office during office hours (8:30 AM to 6:45 PM) for each date:")
# print_extra_time_spent(time_spent, "\nExtra time spent in office for each date:")
# print_extra_time_spent(time_spent, "\nExtra time spent in office during office hours (8:30 AM to 6:45 PM) for each date:")
print_total_extra_time("\nTotal extra time spent in office:", total_extra_time)
print_total_extra_time("\nTotal extra time spent in office during office hours (8:30 AM to 6:45 PM):", total_extra_office_hours_time)

# print_time_spent(time_spent_excluding_weekends, "\nTotal time spent in office excluding weekends for each date:")
# print_time_spent(time_spent_excluding_weekends, "\nTotal time spent in office during office hours (8:30 AM to 6:45 PM) excluding weekends for each date:")
# print_extra_time_spent(time_spent_excluding_weekends, "\nExtra time spent in office excluding weekends for each date:")
# print_extra_time_spent(time_spent_excluding_weekends, "\nExtra time spent in office during office hours (8:30 AM to 6:45 PM) excluding weekends for each date:")
print_total_extra_time("\nTotal extra time spent in office excluding weekends:", total_extra_time_excluding_weekends)
print_total_extra_time("\nTotal extra time spent in office during office hours (8:30 AM to 6:45 PM) excluding weekends:", total_extra_office_hours_time_excluding_weekends)
