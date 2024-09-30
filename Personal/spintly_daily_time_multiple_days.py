import os
import pandas as pd
from tabulate import tabulate
from colorama import Fore, Style, init
from typing import Dict, Tuple
from datetime import datetime, time, timedelta
from typing import List, Dict, Tuple

init(autoreset=True)  # Initialize colorama

# Constants
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds
CSV_FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'time_differences.csv')  # Name of the CSV file to store differences

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

def format_time(seconds: float) -> str:
    """Format time from seconds to HH:MM:SS"""
    return str(timedelta(seconds=int(seconds)))

def calculate_leave_time(office_time: float, current_time: datetime, analyzed_date: datetime.date) -> Tuple[datetime, bool, str, timedelta]:
    time_left = max(TARGET_TIME - office_time, 0)
    is_current_day = analyzed_date == current_time.date()
    
    difference = timedelta(seconds=int(office_time - TARGET_TIME))
    
    if time_left == 0:
        return current_time, True, "Target met", difference
    else:
        if is_current_day:
            leave_time = current_time + timedelta(seconds=time_left)
            if leave_time.time() > time(19, 30):  # If leave time is after office hours
                return datetime.combine(analyzed_date, time(19, 30)), False, "Leave by end of day", difference
            else:
                return leave_time, False, f"Leave by {leave_time.strftime('%I:%M:%S %p')}", difference
        else:
            return current_time, False, "Target not met", difference

def generate_summary_table(time_spent: Dict[str, Dict[str, float]], current_time: datetime, analyzed_date: datetime.date, use_seconds: bool = True) -> str:
    headers = ['Name', 'Total Time', 'Office Hours Time', 'Break Time', 'Target', 'Difference', 'Last Exit', 'Status']
    table = []

    for name, times in time_spent.items():
        if (use_seconds and '_no_seconds' in name) or (not use_seconds and '_no_seconds' not in name):
            continue

        last_exit_time = times['last_exit']
        is_current_day = analyzed_date == current_time.date()

        leave_time, target_met, status, difference = calculate_leave_time(times['office'], current_time, analyzed_date)

        difference_str = format_time(abs(difference.total_seconds()))
        last_exit_time_str = last_exit_time.strftime("%I:%M:%S %p") if use_seconds else last_exit_time.strftime("%I:%M %p")
        
        if is_current_day and not target_met:
            time_left_str = f"-{difference_str}"
            status_color = Fore.YELLOW
        elif target_met:
            time_left_str = f"+{difference_str}" if difference.total_seconds() > 0 else "00:00:00"
            status_color = Fore.GREEN
        else:
            time_left_str = f"-{difference_str}"
            status_color = Fore.RED

        table.append([
            name,
            format_time(times['total']),
            format_time(times['office']),
            format_time(times['break']),
            '✓' if target_met else '✗',
            f"{status_color}{time_left_str}{Style.RESET_ALL}",
            last_exit_time_str,
            f"{status_color}{status}{Style.RESET_ALL}"
        ])

    return tabulate(table, headers, tablefmt="pretty")


CSV_FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'time_differences_multiple.csv')
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds

def format_time(seconds: float) -> str:
    """Format time from seconds to HH:MM:SS"""
    return str(timedelta(seconds=int(seconds)))
def get_dates_in_month(year: int, month: int) -> List[datetime.date]:
    """Get all dates in the specified month and year."""
    start_date = datetime(year, month, 1).date()
    end_date = (datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)).date() - timedelta(days=1)
    return [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

def process_multiple_dates(df: pd.DataFrame, dates: List[datetime.date], current_time: datetime) -> Dict[datetime.date, Dict[str, Dict[str, float]]]:
    """Process multiple dates and return time spent data for each date."""
    results = {}
    for date in dates:
        time_spent, _ = analyze_time_spent(df, date, current_time=current_time)
        results[date] = time_spent
    return results
def save_differences_to_csv(time_spent: Dict[str, Dict[str, float]], analyzed_date: datetime.date, current_time: datetime) -> None:
    csv_file = CSV_FILE_NAME
    data = []

    for name in time_spent:
        if "_no_seconds" in name:
            continue

        time_with_seconds = time_spent[name]['office']
        time_without_seconds = time_spent[f"{name}_no_seconds"]['office']

        leave_time_with_seconds, target_met_with_seconds, status_with_seconds, difference_with_seconds = calculate_leave_time(time_with_seconds, current_time, analyzed_date)
        leave_time_without_seconds, target_met_without_seconds, _, difference_without_seconds = calculate_leave_time(time_without_seconds, current_time, analyzed_date)

        # Adjust the sign of the difference based on whether the target was met
        sign_with_seconds = '+' if difference_with_seconds.total_seconds() >= 0 else '-'
        sign_without_seconds = '+' if difference_without_seconds.total_seconds() >= 0 else '-'

        # Cap the difference at 1 hour if it's greater than that
        def cap_difference(difference: timedelta, sign: str) -> Tuple[str, str, str]:
            if sign == '+' and difference > timedelta(hours=1):
                return '+', '01:00:00', 'Only 1 hour/day can be considered extra'
            else:
                return sign, format_time(abs(difference.total_seconds())), ''

        sign_with_seconds, diff_with_seconds, msg_with_seconds = cap_difference(difference_with_seconds, sign_with_seconds)
        sign_without_seconds, diff_without_seconds, msg_without_seconds = cap_difference(difference_without_seconds, sign_without_seconds)

        # Add data for CSV output
        data.append({
            'Date': analyzed_date,
            'Name': name,
            'Office Time With Seconds': format_time(time_with_seconds),
            'Office Time Without Seconds': format_time(time_without_seconds),
            'Sign With Seconds': sign_with_seconds,
            'Difference With Seconds': diff_with_seconds,
            'Sign Without Seconds': sign_without_seconds,
            'Difference Without Seconds': diff_without_seconds,
            'Status': status_with_seconds,
            'Message With Seconds': msg_with_seconds,
            'Message Without Seconds': msg_without_seconds
        })

    # Load existing CSV if it exists, otherwise create a new DataFrame
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        df = pd.DataFrame()

    # Convert the new data to a DataFrame
    new_df = pd.DataFrame(data)

    # Remove any existing rows for the same Date and Name (to avoid duplicates)
    df = df[~((df['Date'] == str(analyzed_date)) & (df['Name'].isin(new_df['Name'])))]

    # Append new data and reset the index
    df = pd.concat([df, new_df]).reset_index(drop=True)

    # Ensure the columns are in the correct order
    df = df[['Date', 'Name', 'Office Time With Seconds', 'Office Time Without Seconds',
             'Sign With Seconds', 'Difference With Seconds', 
             'Sign Without Seconds', 'Difference Without Seconds',
             'Status', 'Message With Seconds', 'Message Without Seconds']]

    # Save the DataFrame to CSV
    df.to_csv(csv_file, index=False)

def save_multiple_dates_to_csv(results: Dict[datetime.date, Dict[str, Dict[str, float]]], current_time: datetime) -> None:
    """Save time differences for multiple dates to CSV."""
    for date, time_spent in results.items():
        save_differences_to_csv(time_spent, date, current_time)
    print(f"\nTime differences saved to {CSV_FILE_NAME}\n")

def generate_summary_tables(results: Dict[datetime.date, Dict[str, Dict[str, float]]], current_time: datetime) -> str:
    """Generate summary tables for multiple dates."""
    summary = ""
    for date, time_spent in results.items():
        summary += "\n" + f"{('Time Spent on ' + date.strftime('%b %d, %Y')).center(80)}" + "\n"
        summary += generate_summary_table(time_spent, current_time, date, use_seconds=True)
        summary += "\n" + "-"*80 + "\n"
        summary += generate_summary_table(time_spent, current_time, date, use_seconds=False)
        summary += "\n\n"
    return summary

def main(file_path: str, year: int, month: int, start_day: int, end_day: int) -> None:
    sheet_name = 'Access History'
    skip_rows = 5
    current_time = datetime.now()

    df = load_data(file_path, sheet_name, skip_rows)
    if df is not None:
        all_dates = get_dates_in_month(year, month)
        selected_dates = [date for date in all_dates if start_day <= date.day <= end_day]
        
        results = process_multiple_dates(df, selected_dates, current_time)
        
        print(generate_summary_tables(results, current_time))
        
        save_multiple_dates_to_csv(results, current_time)
def calculate_total_difference_from_csv(csv_file: str):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Parse the 'Difference With Seconds' and 'Difference Without Seconds' columns to timedelta
        def parse_time_difference(time_str):
            h, m, s = map(int, time_str.split(':'))
            return timedelta(hours=h, minutes=m, seconds=s)
        
        df['Difference With Seconds'] = df['Difference With Seconds'].apply(parse_time_difference)
        df['Difference Without Seconds'] = df['Difference Without Seconds'].apply(parse_time_difference)
        
        # Initialize cumulative total
        total_diff_with_seconds = timedelta()
        total_diff_without_seconds = timedelta()
        
        # Loop through each row and add the positive differences only
        for index, row in df.iterrows():
            if row['Sign With Seconds'] == '+':
                total_diff_with_seconds += row['Difference With Seconds']
            if row['Sign Without Seconds'] == '+':
                total_diff_without_seconds += row['Difference Without Seconds']
        
        # Print the total difference (cumulative for all days)
        print(f"Total Cumulative Difference With Seconds: {total_diff_with_seconds}")
        print(f"Total Cumulative Difference Without Seconds: {total_diff_without_seconds}")
        
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    file_path = r'c:\Users\Subin-PC\Downloads\subin.xlsx'
    year = 2024
    month = 9
    start_day = 30
    end_day = 30
    main(file_path, year, month, start_day, end_day)
    calculate_total_difference_from_csv(CSV_FILE_NAME)