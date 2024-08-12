import pandas as pd
from datetime import datetime, time, timedelta
import argparse
from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

# Constants
# FILE_PATH = r'c:\Users\Subin-PC\Downloads\subin_july.xlsx'
FILE_PATH = r'c:\Users\Subin-PC\Downloads\chippy.xlsx'
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
                    'total': daily_total_time,
                    'office': daily_office_hours_time,
                    'current_total': current_total_time,
                    'current_office': current_office_hours_time
                }

    if not time_spent:
        print(f"No data available for {date_str}.")
        return

    print_results(time_spent, date_str)

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
                total_time, office_hours_time = calculate_time_spent(group_by_date, current_time=current_time)
                
                time_spent[name] = {
                    'total': total_time,
                    'office': office_hours_time,
                }

    if not time_spent:
        print(f"No data available for {date_str}.")
        return

    print_results(time_spent, date_str, current_time)

def get_status_and_diff(time_value):
    if time_value >= TARGET_TIME:
        extra_time = time_value - TARGET_TIME
        return Fore.GREEN + "✓" + Style.RESET_ALL, f"+{format_time(extra_time)}"
    else:
        remaining_time = TARGET_TIME - time_value
        return Fore.RED + "✗" + Style.RESET_ALL, f"-{format_time(remaining_time)}"

def print_results(time_spent, date_str, current_time):
    headers = ["Name", "Total Time", "Office Hours Time", "Target", "Difference"]
    table_data = []

    for name, data in time_spent.items():
        status, diff = get_status_and_diff(data['office'])
        row = [
            name,
            format_time(data['total']),
            format_time(data['office']),
            status,
            diff
        ]
        table_data.append(row)

    print(f"\nTime spent summary for {date_str}:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    target_time_str = format_time(TARGET_TIME)
    office_start_str = OFFICE_START.strftime("%I:%M %p")
    office_end_str = OFFICE_END.strftime("%I:%M %p")
    current_time_str = current_time.strftime("%I:%M:%S %p")
    print(f"\nOffice hours: {office_start_str} to {office_end_str}")
    print(f"Target time: {target_time_str}")
    print(f"Calculation made at: {current_time_str}")
    print("✓ = Target met (extra time shown), ✗ = Target not met (remaining time shown)")
    print("Total Time includes time spent outside office hours")

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