import pandas as pd
from datetime import datetime, time, timedelta
from tabulate import tabulate
from colorama import Fore, Style, init
from typing import Dict, Tuple

init(autoreset=True)  # Initialize colorama

# Constants
FILE_PATH = r'c:\Users\Subin-PC\Downloads\subin_july.xlsx'
# FILE_PATH = r'c:\Users\Subin-PC\Downloads\chippy.xlsx'
SHEET_NAME = 'Access History'
SKIP_ROWS = 5
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds

def parse_datetime(date: str, time_str: str) -> datetime:
    """Parse datetime from date and time strings"""
    return datetime.strptime(f"{date} {time_str.split('(')[0].strip()}", "%b %d, %Y %I:%M:%S %p")

def load_data() -> pd.DataFrame:
    try:
        df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME, skiprows=SKIP_ROWS)
        df['DateTime'] = df.apply(lambda row: parse_datetime(row['Date'], row['Time']), axis=1)
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y').dt.date
        return df[['Date', 'DateTime', 'Name', 'Direction']].sort_values(by=['Name', 'DateTime'])
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def truncate_seconds(dt: datetime) -> datetime:
    """Truncate seconds from datetime"""
    return dt.replace(second=0, microsecond=0)

def calculate_time_spent(group: pd.DataFrame, current_time: datetime = None, truncate: bool = False) -> Tuple[float, float, float, datetime]:
    """Calculate time spent in office"""
    total_time = 0
    total_office_hours_time = 0
    total_break_time = 0
    entry_time = None
    last_exit_time = None
    first_entry_time = None

    for _, row in group.iterrows():
        if truncate:
            dt = truncate_seconds(row['DateTime'])
        else:
            dt = row['DateTime']

        if row['Direction'] == 'entry':
            if first_entry_time is None:
                first_entry_time = dt
            entry_time = dt
        elif row['Direction'] == 'exit' and entry_time:
            exit_time = dt
            last_exit_time = exit_time
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
        if truncate:
            exit_time = truncate_seconds(current_time)
        else:
            exit_time = current_time
        last_exit_time = exit_time
        duration = (exit_time - entry_time).total_seconds()
        total_time += duration

        # Calculate time during office hours
        entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=OFFICE_START.hour, minute=OFFICE_START.minute, second=0))
        exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=OFFICE_END.hour, minute=OFFICE_END.minute, second=0))

        if entry_time_within_office_hours < exit_time_within_office_hours:
            duration_office_hours = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
            total_office_hours_time += duration_office_hours

    # Calculate total break time
    if first_entry_time and last_exit_time:
        total_duration = (last_exit_time - first_entry_time).total_seconds()
        total_break_time = total_duration - total_time

    return total_time, total_office_hours_time, total_break_time, last_exit_time

def format_time(seconds: float) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def get_time_spent_on_date(df: pd.DataFrame, date_str: str) -> None:
    try:
        date = datetime.strptime(date_str, "%b %d, %Y").date()
    except ValueError:
        print("Invalid date format. Please use 'MMM DD, YYYY' format.")
        return

    time_spent_with_seconds: Dict[str, Dict[str, float]] = {}
    time_spent_no_seconds: Dict[str, Dict[str, float]] = {}
    current_time = datetime.now()

    for name, group in df.groupby('Name'):
        for group_date, group_by_date in group.groupby('Date'):
            if group_date == date:  # Compare with the date, not datetime
                total_time, office_hours_time, total_break_time, last_exit_time = calculate_time_spent(group_by_date, current_time=current_time)
                time_spent_with_seconds[name] = {
                    'total': total_time,
                    'office': office_hours_time,
                    'break': total_break_time,
                    'last_exit': last_exit_time
                }
                
                total_time_no_seconds, office_hours_time_no_seconds, total_break_time_no_seconds, last_exit_time_no_seconds = calculate_time_spent(group_by_date, current_time=current_time, truncate=True)
                time_spent_no_seconds[name] = {
                    'total': total_time_no_seconds,
                    'office': office_hours_time_no_seconds,
                    'break': total_break_time_no_seconds,
                    'last_exit': last_exit_time_no_seconds
                }

    if not time_spent_with_seconds:
        print(f"No data available for {date_str}.")
        return

    print_results(time_spent_with_seconds, date_str, current_time, use_seconds=True)
    print("\n" + "-"*80 + "\n")
    print_results(time_spent_no_seconds, date_str, current_time, use_seconds=False)

def print_results(time_spent: Dict[str, Dict[str, float]], date_str: str, current_time: datetime, use_seconds: bool) -> None:
    """Prints the results in a formatted table"""
    if use_seconds:
        headers = ['Name', 'Total Time', 'Office Hours Time', 'Break Time', 'Target', 'Difference', 'Last Exit']
    else:
        headers = ['Name', 'Total Time (No Seconds)', 'Office Hours Time (No Seconds)', 'Break Time', 'Target', 'Difference', 'Last Exit']

    table = []

    for name, times in time_spent.items():
        time_left = max(TARGET_TIME - times['office'], 0)
        target_met = time_left == 0
        difference_str = format_time(abs(TARGET_TIME - times['office']))
        last_exit_time_str = times['last_exit'].strftime("%I:%M:%S %p") if use_seconds else times['last_exit'].strftime("%I:%M %p")
        time_left_str = f"{'+' if target_met else '-'}{difference_str}"
        
        table.append([
            name,
            format_time(times['total']),
            format_time(times['office']),
            format_time(times['break']),
            '✓' if target_met else '✗',
            f"{Fore.GREEN}{time_left_str}{Style.RESET_ALL}" if target_met else f"{Fore.RED}{time_left_str}{Style.RESET_ALL}",
            last_exit_time_str
        ])

    summary_title = "Time spent summary with seconds" if use_seconds else "Time spent summary without seconds"
    print(f"{summary_title} for {date_str}:")
    print(tabulate(table, headers, tablefmt="pretty"))

    print(f"\nOffice hours: {OFFICE_START.strftime('%I:%M %p')} to {OFFICE_END.strftime('%I:%M %p')}")
    print(f"Target time: {format_time(TARGET_TIME)}")
    print(f"Calculation made at: {current_time.strftime('%I:%M:%S %p') if use_seconds else current_time.strftime('%I:%M %p')}")
    print("✓ = Target met (extra time shown), ✗ = Target not met (remaining time shown)")
    print("Total Time includes time spent outside office hours")
    print("Break Time is calculated as the total duration minus the actual time spent in office.")

def main() -> None:
    date_str = input("Enter the date (MMM DD, YYYY): ")

    df = load_data()
    if df is not None:
        print(f"Calculating time spent for {date_str}...\n")
        get_time_spent_on_date(df, date_str)

if __name__ == "__main__":
    main()