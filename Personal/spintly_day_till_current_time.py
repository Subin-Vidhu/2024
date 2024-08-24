import pandas as pd
from datetime import datetime, time, timedelta
from tabulate import tabulate
from colorama import Fore, Style, init
from typing import Dict, Tuple

init(autoreset=True)  # Initialize colorama

# Constants
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds

def parse_datetime(date: str, time_str: str) -> datetime:
    """Parse datetime from date and time strings"""
    return datetime.strptime(f"{date} {time_str.split('(')[0].strip()}", "%b %d, %Y %I:%M:%S %p")

def load_data(file_path: str, sheet_name: str, skip_rows: int) -> pd.DataFrame:
    """Load Excel data and preprocess it"""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skip_rows)
        df['DateTime'] = df.apply(lambda row: parse_datetime(row['Date'], row['Time']), axis=1)
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y').dt.date
        return df[['Date', 'DateTime', 'Name', 'Direction']].sort_values(by=['Name', 'DateTime'])
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def truncate_seconds(dt: datetime) -> datetime:
    """Truncate seconds from datetime"""
    return dt.replace(second=0, microsecond=0)

def calculate_time_spent(group: pd.DataFrame, current_time: datetime = None, truncate: bool = False) -> Dict[str, float]:
    """Calculate time spent in office"""
    total_time, total_office_hours_time, total_break_time = 0, 0, 0
    entry_time, first_entry_time, last_exit_time = None, None, None

    for _, row in group.iterrows():
        dt = truncate_seconds(row['DateTime']) if truncate else row['DateTime']

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
                total_office_hours_time += (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()

            entry_time = None

    # Handle open entry without exit
    if entry_time and current_time:
        exit_time = truncate_seconds(current_time) if truncate else current_time
        last_exit_time = exit_time
        total_time += (exit_time - entry_time).total_seconds()

        # Office hours calculation
        entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=OFFICE_START.hour, minute=OFFICE_START.minute, second=0))
        exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=OFFICE_END.hour, minute=OFFICE_END.minute, second=0))

        if entry_time_within_office_hours < exit_time_within_office_hours:
            total_office_hours_time += (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()

    # Calculate total break time
    if first_entry_time and last_exit_time:
        total_duration = (last_exit_time - first_entry_time).total_seconds()
        total_break_time = total_duration - total_time

    return {
        'total': total_time,
        'office': total_office_hours_time,
        'break': total_break_time,
        'last_exit': last_exit_time
    }

def format_time(seconds: float) -> str:
    """Format time from seconds to hh:mm:ss"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def analyze_time_spent(df: pd.DataFrame, date: datetime.date, current_time: datetime = None) -> Tuple[Dict[str, Dict[str, float]], datetime.date]:
    """Analyze and calculate time spent for each user on the specified date"""
    time_spent = {}
    
    for name, group in df.groupby('Name'):
        group_by_date = group[group['Date'] == date]
        if not group_by_date.empty:
            time_spent[name] = calculate_time_spent(group_by_date, current_time=current_time)
            time_spent[f"{name}_no_seconds"] = calculate_time_spent(group_by_date, current_time=current_time, truncate=True)
    
    return time_spent, date

def calculate_leave_time(office_time: float, current_time: datetime) -> Tuple[datetime, bool]:
    time_left = max(TARGET_TIME - office_time, 0)
    if time_left == 0:
        return current_time, True
    else:
        leave_time = current_time + timedelta(seconds=time_left)
        return leave_time, False

def generate_summary_table(time_spent: Dict[str, Dict[str, float]], current_time: datetime, analyzed_date: datetime.date, use_seconds: bool = True) -> str:
    """Generate a summary table from time spent data"""
    headers = ['Name', 'Total Time', 'Office Hours Time', 'Break Time', 'Target', 'Difference', 'Last Exit', 'Leave By']
    table = []

    for name, times in time_spent.items():
        if (use_seconds and '_no_seconds' in name) or (not use_seconds and '_no_seconds' not in name):
            continue

        last_exit_time = times['last_exit']
        is_past_date = analyzed_date < current_time.date()

        if is_past_date:
            leave_time, target_met = calculate_leave_time(times['office'], last_exit_time)
        else:
            leave_time, target_met = calculate_leave_time(times['office'], current_time)

        difference_str = format_time(abs(TARGET_TIME - times['office']))
        last_exit_time_str = last_exit_time.strftime("%I:%M:%S %p") if use_seconds else last_exit_time.strftime("%I:%M %p")
        leave_time_str = leave_time.strftime("%I:%M:%S %p") if use_seconds else leave_time.strftime("%I:%M %p")
        time_left_str = f"{'+' if target_met else '-'}{difference_str}"

        leave_by_str = (f"{Fore.GREEN}Left at {last_exit_time_str}{Style.RESET_ALL}" if target_met else \
                        f"{Fore.RED}Should have left by {leave_time_str}{Style.RESET_ALL}") if is_past_date else \
                       (f"{Fore.GREEN}Could have left at {leave_time_str}{Style.RESET_ALL}" if target_met else \
                        f"{Fore.YELLOW}Leave by {leave_time_str}{Style.RESET_ALL}")

        table.append([
            name,
            format_time(times['total']),
            format_time(times['office']),
            format_time(times['break']),
            '✓' if target_met else '✗',
            f"{Fore.GREEN}{time_left_str}{Style.RESET_ALL}" if target_met else f"{Fore.RED}{time_left_str}{Style.RESET_ALL}",
            last_exit_time_str,
            leave_by_str
        ])

    return tabulate(table, headers, tablefmt="pretty")

def main(file_path: str, date_str: str) -> None:
    sheet_name = 'Access History'
    skip_rows = 5
    date = datetime.strptime(date_str, "%b %d, %Y").date()
    current_time = datetime.now()

    df = load_data(file_path, sheet_name, skip_rows)
    if df is not None:
        time_spent, analyzed_date = analyze_time_spent(df, date, current_time=current_time)
        print("\n" + f"{('Time Spent on ' + analyzed_date.strftime('%b %d, %Y')).center(80)}" + "\n")
        print(generate_summary_table(time_spent, current_time, analyzed_date, use_seconds=True))
        print("\n" + "-"*80 + "\n")
        print(generate_summary_table(time_spent, current_time, analyzed_date, use_seconds=False))

if __name__ == "__main__":
    file_path = r'c:\Users\Subin-PC\Downloads\subin.xlsx'
    # file_path = r'c:\Users\Subin-PC\Downloads\chippy.xlsx'
    date_str = "Aug 24, 2024"
    main(file_path, date_str)