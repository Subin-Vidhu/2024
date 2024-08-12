import pandas as pd
from datetime import datetime, time, timedelta
import argparse
from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

# Constants
FILE_PATH = r'c:\Users\Subin-PC\Downloads\subin_july.xlsx'
SHEET_NAME = 'Access History'
SKIP_ROWS = 5
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate office time from Excel sheet.")
    parser.add_argument("--date", help="Date to calculate (MMM DD, YYYY)")
    return parser.parse_args()

def parse_datetime(date, time_str):
    """Parse datetime from date and time strings"""
    return datetime.strptime(f"{date} {time_str.split('(')[0].strip()}", "%b %d, %Y %I:%M:%S %p")

def load_data():
    try:
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME, skiprows=SKIP_ROWS)
        df['DateTime'] = df.apply(lambda row: parse_datetime(row['Date'], row['Time']), axis=1)
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
        return df[['Date', 'DateTime', 'Name', 'Direction']].sort_values(by=['Name', 'DateTime'])
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

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

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def get_time_spent_on_date(df, date_str):
    try:
        date = datetime.strptime(date_str, "%b %d, %Y")
    except ValueError:
        print("Invalid date format. Please use 'MMM DD, YYYY' format.")
        return

    time_spent = {}
    current_time = datetime.now()

    for name, group in df.groupby('Name'):
        for group_date, group_by_date in group.groupby('Date'):
            if group_date.date() == date.date():
                daily_total_time, daily_office_hours_time = calculate_time_spent(group_by_date)
                current_total_time, current_office_hours_time = calculate_time_spent(group_by_date, current_time=current_time)
                
                time_spent[name] = {
                    'total_time': daily_total_time,
                    'office_hours_time': daily_office_hours_time,
                    'current_total_time': current_total_time,
                    'current_office_hours_time': current_office_hours_time
                }

    if not time_spent:
        print(f"No data available for {date_str}.")
        return

    print(f"\nTime spent in office on {date_str}:")
    print_table(time_spent, 'total_time', 'Total Time')

    print(f"\nTime spent in office during office hours (7:30 AM to 7:30 PM) on {date_str}:")
    print_table(time_spent, 'office_hours_time', 'Office Hours Time')

    print(f"\nTime spent in office till the current time on {date_str}:")
    print_table(time_spent, 'current_total_time', 'Current Total Time')

    print(f"\nTime spent in office during office hours (7:30 AM to 7:30 PM) till the current time on {date_str}:")
    print_table(time_spent, 'current_office_hours_time', 'Current Office Hours Time')

def print_table(time_spent, time_key, time_label):
    table_data = []
    for name, data in time_spent.items():
        time_value = data[time_key]
        formatted_time = format_time(time_value)
        status = get_status(time_value)
        table_data.append([name, formatted_time, status])
    
    headers = ["Name", time_label, "Status"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def get_status(time_value):
    if time_value >= TARGET_TIME:
        extra_time = time_value - TARGET_TIME
        return Fore.GREEN + f"Met target (+{format_time(extra_time)})" + Style.RESET_ALL
    else:
        remaining_time = TARGET_TIME - time_value
        return Fore.RED + f"Need {format_time(remaining_time)} more" + Style.RESET_ALL

def main():
    args = parse_args()
    df = load_data()
    if df is None:
        return

    if args.date:
        date_str = args.date
    else:
        date_str = input("Enter the date (MMM DD, YYYY): ").strip()

    get_time_spent_on_date(df, date_str)

if __name__ == "__main__":
    main()