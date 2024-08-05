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

# Define office hours
office_start = time(7, 30)
office_end = time(19, 30)

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

# Function to get user input date and return time spent in office
def get_time_spent_on_date(date_str):
    try:
        # Normalize the input by adding a space after the comma if not present
        if ',' in date_str and not date_str[date_str.index(',') + 1].isspace():
            date_str = date_str[:date_str.index(',') + 1] + ' ' + date_str[date_str.index(',') + 1:].strip()
        date = datetime.strptime(date_str, "%b %d, %Y")
    except ValueError:
        print("Invalid date format. Please use 'MMM DD, YYYY' format.")
        return

    time_spent = {}
    for name, group in df.groupby('Name'):
        for group_date, group_by_date in group.groupby('Date'):
            if group_date == date:
                daily_total_time, daily_office_hours_time = calculate_time_spent(group_by_date)
                if name not in time_spent:
                    time_spent[name] = {}
                time_spent[name][date] = {
                    'total_time': daily_total_time,
                    'office_hours_time': daily_office_hours_time
                }

    if not time_spent:
        print(f"No data available for {date_str}.")
        return

    target_time = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds

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
            if total_seconds >= target_time:
                extra_time = total_seconds - target_time
                extra_hours, extra_remainder = divmod(extra_time, 3600)
                extra_minutes, extra_seconds = divmod(extra_remainder, 60)
                print(f"  {name} has met the target time of {divmod(target_time, 3600)[0]} hours and {divmod(target_time, 3600)[1]// 60} minutes with {int(extra_hours)} hours, {int(extra_minutes)} minutes, {int(extra_seconds)} seconds extra.")
            else:
                remaining_time = target_time - total_seconds
                remaining_hours, remaining_remainder = divmod(remaining_time, 3600)
                remaining_minutes, remaining_seconds = divmod(remaining_remainder, 60)
                print(f"  {name} has not met the target time of 8 hours 30 minutes. Remaining time: {int(remaining_hours)} hours, {int(remaining_minutes)} minutes, {int(remaining_seconds)} seconds.")

# Get user input
user_date = input("Enter the date (MMM DD, YYYY): ").strip()
get_time_spent_on_date(user_date)
# import pandas as pd
# from datetime import datetime, time, timedelta

# # Load the data from the Excel file
# file_path = r'c:\Users\Subin-PC\Downloads\Access history report - 25-07-2024 to 28-07-2024.xlsx'
# df = pd.read_excel(file_path, sheet_name='Access History', skiprows=5)

# # Function to parse datetime
# def parse_datetime(date, time_str):
#     return datetime.strptime(f"{date} {time_str.split('(')[0].strip()}", "%b %d, %Y %I:%M:%S %p")

# # Parse the DateTime column
# df['DateTime'] = df.apply(lambda row: parse_datetime(row['Date'], row['Time']), axis=1)

# # Convert Date column to datetime for proper sorting
# df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

# # Filter for relevant columns and sort the data by Name and DateTime
# df = df[['Date', 'DateTime', 'Name', 'Direction']].sort_values(by=['Name', 'DateTime'])

# # Define office hours
# office_start = time(8, 30)
# office_end = time(18, 45)

# # Function to calculate time spent inside office during office hours
# def calculate_time_spent(group):
#     total_time = 0
#     total_office_hours_time = 0
#     entry_time = None

#     for _, row in group.iterrows():
#         if row['Direction'] == 'entry':
#             entry_time = row['DateTime']
#         elif row['Direction'] == 'exit' and entry_time:
#             exit_time = row['DateTime']
#             duration = (exit_time - entry_time).total_seconds()
#             total_time += duration

#             # Calculate time during office hours
#             entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=office_start.hour, minute=office_start.minute, second=0))
#             exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=office_end.hour, minute=office_end.minute, second=0))

#             if entry_time_within_office_hours < exit_time_within_office_hours:
#                 duration_office_hours = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
#                 total_office_hours_time += duration_office_hours

#             entry_time = None

#     return total_time, total_office_hours_time

# # Function to get user input date and return time spent in office
# def get_time_spent_on_date(date_str):
#     try:
#         # Normalize the input by adding a space after the comma if not present
#         if ',' in date_str and not date_str[date_str.index(',') + 1].isspace():
#             date_str = date_str[:date_str.index(',') + 1] + ' ' + date_str[date_str.index(',') + 1:].strip()
#         date = datetime.strptime(date_str, "%b %d, %Y")
#     except ValueError:
#         print("Invalid date format. Please use 'MMM DD, YYYY' format.")
#         return

#     time_spent = {}
#     for name, group in df.groupby('Name'):
#         for group_date, group_by_date in group.groupby('Date'):
#             if group_date == date:
#                 daily_total_time, daily_office_hours_time = calculate_time_spent(group_by_date)
#                 if name not in time_spent:
#                     time_spent[name] = {}
#                 time_spent[name][date] = {
#                     'total_time': daily_total_time,
#                     'office_hours_time': daily_office_hours_time
#                 }

#     if not time_spent:
#         print(f"No data available for {date_str}.")
#         return

#     print(f"\nTime spent in office on {date_str}:")
#     for name, dates in time_spent.items():
#         for date in dates:
#             total_seconds = dates[date]['total_time']
#             hours, remainder = divmod(total_seconds, 3600)
#             minutes, seconds = divmod(remainder, 60)
#             print(f"  {name}: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

#     print(f"\nTime spent in office during office hours (8:30 AM to 6:45 PM) on {date_str}:")
#     for name, dates in time_spent.items():
#         for date in dates:
#             total_seconds = dates[date]['office_hours_time']
#             hours, remainder = divmod(total_seconds, 3600)
#             minutes, seconds = divmod(remainder, 60)
#             print(f"  {name}: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

# # Get user input
# user_date = input("Enter the date (MMM DD, YYYY): ").strip()
# get_time_spent_on_date(user_date)