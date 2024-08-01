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
office_start = time(8, 30)
office_end = time(18, 45)
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

# Initialize dictionaries to store results
time_spent = {}
total_extra_time = 0
total_extra_office_hours_time = 0

time_spent_excluding_weekends = {}
total_extra_time_excluding_weekends = 0
total_extra_office_hours_time_excluding_weekends = 0

# Variables to track lack of time
total_lack_of_time = 0
total_lack_of_time_excluding_weekends = 0

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

        # Calculate extra time and lack of time
        extra_time = daily_total_time - standard_workday_seconds
        extra_office_hours_time = daily_office_hours_time - standard_workday_seconds

        if extra_time > 0:
            total_extra_time += extra_time
        elif extra_time < 0:
            total_lack_of_time -= extra_time  # Subtracting because extra_time is negative

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
            elif extra_time < 0:
                total_lack_of_time_excluding_weekends -= extra_time  # Subtracting because extra_time is negative

            if extra_office_hours_time > 0:
                total_extra_office_hours_time_excluding_weekends += extra_office_hours_time

# Convert seconds to hours, minutes, seconds
def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"

# Create DataFrames for saving to Excel
def create_detailed_df(time_spent, include_weekends):
    rows = []
    for name, dates in time_spent.items():
        for date, times in dates.items():
            total_time_seconds = times['total_time']
            office_hours_time_seconds = times['office_hours_time']
            extra_time = max(total_time_seconds - standard_workday_seconds, 0)
            lack_of_time = max(standard_workday_seconds - total_time_seconds, 0)
            extra_office_hours_time = max(office_hours_time_seconds - standard_workday_seconds, 0)
            lack_of_office_hours_time = max(standard_workday_seconds - office_hours_time_seconds, 0)
            rows.append({
                'Name': name,
                'Date': date.strftime('%b %d, %Y'),
                'Total Time': format_time(total_time_seconds),
                'Office Hours Time': format_time(office_hours_time_seconds),
                'Extra Time': format_time(extra_time),
                'Lack of Time': format_time(lack_of_time),
                'Extra Office Hours Time': format_time(extra_office_hours_time),
                'Lack of Office Hours Time': format_time(lack_of_office_hours_time),
            })
    return pd.DataFrame(rows)

# Save results to Excel
output_file_path = r'c:\Users\Subin-PC\Downloads\Office_Time_Report_Detailed.xlsx'
with pd.ExcelWriter(output_file_path) as writer:
    # Create and write DataFrames to Excel
    df_detailed_includes_weekends = create_detailed_df(time_spent, include_weekends=True)
    df_detailed_excludes_weekends = create_detailed_df(time_spent_excluding_weekends, include_weekends=False)

    df_detailed_includes_weekends.to_excel(writer, sheet_name='Detailed Report Including Weekends', index=False)
    df_detailed_excludes_weekends.to_excel(writer, sheet_name='Detailed Report Excluding Weekends', index=False)

print(f"Detailed results have been saved to {output_file_path}")

# Print overall time differences
def print_total_time_difference(total_extra_time, total_lack_of_time, include_weekends=True):
    total_time_difference = total_extra_time - total_lack_of_time
    title = "\nOverall time difference for the month (including weekends):" if include_weekends else "\nOverall time difference for the month (excluding weekends):"
    if total_time_difference > 0:
        hours, remainder = divmod(total_time_difference, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{title}\n  {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds extra")
    else:
        lack_of_time = -total_time_difference
        hours, remainder = divmod(lack_of_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{title}\n  {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds lacking")
def print_total_extra_time(title, total_extra_time):
    print(title)
    hours, remainder = divmod(total_extra_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"  {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds extra")

def print_total_lack_of_time(title, total_lack_of_time):
    print(title)
    hours, remainder = divmod(total_lack_of_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"  {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds lacking")

# Printing the results
print_total_extra_time("\nTotal extra time spent in office:", total_extra_time)
print_total_extra_time("\nTotal extra time spent in office during office hours (8:30 AM to 6:45 PM):", total_extra_office_hours_time)
print_total_extra_time("\nTotal extra time spent in office excluding weekends:", total_extra_time_excluding_weekends)
print_total_extra_time("\nTotal extra time spent in office during office hours (8:30 AM to 6:45 PM) excluding weekends:", total_extra_office_hours_time_excluding_weekends)

print_total_lack_of_time("\nTotal lack of time in office:", total_lack_of_time)
print_total_lack_of_time("\nTotal lack of time in office excluding weekends:", total_lack_of_time_excluding_weekends)

print_total_time_difference(total_extra_time, total_lack_of_time, include_weekends=True)
print_total_time_difference(total_extra_time_excluding_weekends, total_lack_of_time_excluding_weekends, include_weekends=False)
