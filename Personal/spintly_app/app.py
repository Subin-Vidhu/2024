from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session, jsonify
import os
from datetime import datetime, time, timedelta
import pandas as pd
from werkzeug.utils import secure_filename
from typing import Dict, List, Tuple
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

# Constants
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure CSV storage
CSV_STORAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(CSV_STORAGE):
    os.makedirs(CSV_STORAGE)
LOCAL_CSV_FILE = os.path.join(CSV_STORAGE, 'time_differences_local.csv')

# Configure allowed file extensions
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

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

    if current_time and isinstance(current_time, datetime):
        current_time = current_time.replace(tzinfo=None)

    for _, row in group.iterrows():
        dt = truncate_seconds(row['DateTime']) if truncate else row['DateTime']
        dt = dt.replace(tzinfo=None)

        if row['Direction'].lower() == 'entry':
            if first_entry_time is None:
                first_entry_time = dt
            entry_time = dt
        elif row['Direction'].lower() == 'exit' and entry_time:
            exit_time = dt
            last_exit_time = exit_time
            duration = (exit_time - entry_time).total_seconds()
            total_time += duration

            entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=OFFICE_START.hour, minute=OFFICE_START.minute, second=0))
            exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=OFFICE_END.hour, minute=OFFICE_END.minute, second=0))

            if entry_time_within_office_hours < exit_time_within_office_hours:
                office_duration = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
                total_office_hours_time += office_duration

            entry_time = None

    if entry_time and current_time:
        exit_time = truncate_seconds(current_time) if truncate else current_time
        last_exit_time = exit_time
        duration = (exit_time - entry_time).total_seconds()
        if duration > 0:
            total_time += duration

            entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=OFFICE_START.hour, minute=OFFICE_START.minute, second=0))
            exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=OFFICE_END.hour, minute=OFFICE_END.minute, second=0))

            if entry_time_within_office_hours < exit_time_within_office_hours:
                office_duration = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
                total_office_hours_time += office_duration

    if first_entry_time and last_exit_time:
        total_duration = (last_exit_time - first_entry_time).total_seconds()
        total_break_time = max(0, total_duration - total_time)

    return {
        'total': total_time,
        'office': total_office_hours_time,
        'break': total_break_time,
        'last_exit': last_exit_time
    }

def format_time(seconds: float) -> str:
    """Format time from seconds to HH:MM:SS"""
    return str(timedelta(seconds=int(seconds)))

def analyze_time_spent(df: pd.DataFrame, date: datetime.date, current_time: datetime = None) -> Tuple[Dict[str, Dict[str, float]], datetime.date]:
    """Analyze and calculate time spent for each user on the specified date"""
    time_spent = {}
    
    for name, group in df.groupby('Name'):
        group_by_date = group[group['Date'] == date]
        if not group_by_date.empty:
            time_spent[name] = calculate_time_spent(group_by_date, current_time=current_time)
            time_spent[f"{name}_no_seconds"] = calculate_time_spent(group_by_date, current_time=current_time, truncate=True)
    
    return time_spent, date

def calculate_leave_time(office_time: float, current_time: datetime, analyzed_date: datetime.date) -> Tuple[datetime, bool, str, timedelta]:
    time_left = max(TARGET_TIME - office_time, 0)
    is_current_day = analyzed_date == current_time.date()
    
    difference = timedelta(seconds=int(office_time - TARGET_TIME))
    
    if time_left == 0:
        return current_time, True, "Target met", difference
    else:
        if is_current_day:
            leave_time = current_time + timedelta(seconds=time_left)
            if leave_time.time() > time(19, 30):
                return datetime.combine(analyzed_date, time(19, 30)), False, "Leave by end of day", difference
            else:
                return leave_time, False, f"Leave by {leave_time.strftime('%I:%M:%S %p')}", difference
        else:
            return current_time, False, "Target not met", difference

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

def save_differences_to_csv(time_spent: Dict[str, Dict[str, float]], analyzed_date: datetime.date, current_time: datetime, csv_file: str = None) -> None:
    """Save time differences to CSV file."""
    if csv_file is None:
        csv_file = LOCAL_CSV_FILE
        
    data = []

    for name in time_spent:
        if "_no_seconds" in name:
            continue

        time_with_seconds = time_spent[name]['office']
        time_without_seconds = time_spent[f"{name}_no_seconds"]['office']

        leave_time_with_seconds, target_met_with_seconds, status_with_seconds, difference_with_seconds = calculate_leave_time(time_with_seconds, current_time, analyzed_date)
        leave_time_without_seconds, target_met_without_seconds, _, difference_without_seconds = calculate_leave_time(time_without_seconds, current_time, analyzed_date)

        sign_with_seconds = '+' if difference_with_seconds.total_seconds() >= 0 else '-'
        sign_without_seconds = '+' if difference_without_seconds.total_seconds() >= 0 else '-'

        def cap_difference(difference: timedelta, sign: str) -> Tuple[str, str, str]:
            if sign == '+' and difference > timedelta(hours=1):
                return '+', '01:00:00', 'Only 1 hour/day can be considered extra'
            else:
                return sign, format_time(abs(difference.total_seconds())), ''

        sign_with_seconds, diff_with_seconds, msg_with_seconds = cap_difference(difference_with_seconds, sign_with_seconds)
        sign_without_seconds, diff_without_seconds, msg_without_seconds = cap_difference(difference_without_seconds, sign_without_seconds)

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

    new_df = pd.DataFrame(data)

    try:
        df = pd.read_csv(csv_file)
        df = df[~((df['Date'] == str(analyzed_date)) & (df['Name'].isin(new_df['Name'])))]
        df = pd.concat([df, new_df]).reset_index(drop=True)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = new_df

    df = df[['Date', 'Name', 'Office Time With Seconds', 'Office Time Without Seconds',
             'Sign With Seconds', 'Difference With Seconds', 
             'Sign Without Seconds', 'Difference Without Seconds',
             'Status', 'Message With Seconds', 'Message Without Seconds']]

    df.to_csv(csv_file, index=False)

def save_multiple_dates_to_csv(results: Dict[datetime.date, Dict[str, Dict[str, float]]], current_time: datetime, csv_file: str = None) -> None:
    """Save time differences for multiple dates to CSV."""
    if csv_file is None:
        csv_file = LOCAL_CSV_FILE
        
    for date, time_spent in results.items():
        save_differences_to_csv(time_spent, date, current_time, csv_file)

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
        last_exit_time_str = "No exit" if last_exit_time is None else (
            last_exit_time.strftime("%I:%M:%S %p") if use_seconds else last_exit_time.strftime("%I:%M %p")
        )
        
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

    from tabulate import tabulate
    return tabulate(table, headers, tablefmt="pretty")

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

def calculate_total_difference_from_csv(csv_file: str, start_date: datetime.date = None, end_date: datetime.date = None):
    try:
        df = pd.read_csv(csv_file)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        
        if start_date and end_date:
            df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        
        def parse_time_difference(time_str):
            h, m, s = map(int, time_str.split(':'))
            return timedelta(hours=h, minutes=m, seconds=s)
        
        df['Difference With Seconds'] = df['Difference With Seconds'].apply(parse_time_difference)
        df['Difference Without Seconds'] = df['Difference Without Seconds'].apply(parse_time_difference)
        
        total_diff_with_seconds = timedelta()
        total_diff_without_seconds = timedelta()
        
        for index, row in df.iterrows():
            if row['Sign With Seconds'] == '+':
                total_diff_with_seconds += row['Difference With Seconds']
            if row['Sign Without Seconds'] == '+':
                total_diff_without_seconds += row['Difference Without Seconds']
        
        result = {
            "Total Cumulative Difference With Seconds": str(total_diff_with_seconds),
            "Total Cumulative Difference Without Seconds": str(total_diff_without_seconds)
        }
        
        return result
        
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_total_difference(total_diff):
    """Format the total difference output to be more readable"""
    if not total_diff:
        return "No cumulative difference calculated"
    
    with_seconds = total_diff.get("Total Cumulative Difference With Seconds", "0:00:00")
    without_seconds = total_diff.get("Total Cumulative Difference Without Seconds", "0:00:00")
    
    return {
        "with_seconds": with_seconds,
        "without_seconds": without_seconds
    }

def clear_local_csv():
    """Clear the local CSV file"""
    try:
        if os.path.exists(LOCAL_CSV_FILE):
            os.remove(LOCAL_CSV_FILE)
    except Exception as e:
        print(f"Error clearing local CSV: {e}")

def format_summary_for_web(summary_text: str) -> str:
    """Convert terminal-style summary to HTML table format"""
    tables_html = []
    current_table = []
    
    lines = summary_text.split('\n')
    in_table = False
    date_header = ""
    
    for line in lines:
        if 'Time Spent on' in line:
            if current_table:
                tables_html.append(create_table_html(current_table, date_header))
                current_table = []
            date_header = line.strip()
            in_table = False
        elif '|' in line and not line.strip().startswith('-') and not line.strip().startswith('+'):
            # This is a data line
            cells = [cell.strip() for cell in line.split('|')]
            cells = [cell for cell in cells if cell]  # Remove empty cells
            if not in_table:
                # This is a header row
                in_table = True
            current_table.append(cells)
    
    if current_table:
        tables_html.append(create_table_html(current_table, date_header))
    
    return '\n'.join(tables_html)

def create_table_html(table_data, date_header):
    """Create HTML table from data"""
    if not table_data:
        return ""
    
    html = f'<div class="date-header">{date_header}</div>'
    html += '<div class="table-responsive"><table class="table table-dark table-hover">'
    
    # Headers
    html += '<thead><tr>'
    for header in table_data[0]:
        html += f'<th>{header}</th>'
    html += '</tr></thead>'
    
    # Data rows
    html += '<tbody>'
    for row in table_data[1:]:
        html += '<tr>'
        for cell in row:
            cell_class = ''
            if '✓' in cell:
                cell_class = 'class="table-success"'
            elif '✗' in cell:
                cell_class = 'class="table-danger"'
            
            # Handle colored text (assuming it contains time differences)
            if '[33m' in cell:  # Yellow
                cell_class = 'class="text-warning"'
            elif '[32m' in cell:  # Green
                cell_class = 'class="text-success"'
            elif '[31m' in cell:  # Red
                cell_class = 'class="text-danger"'
            
            # Clean up ANSI color codes
            cell = cell.replace('[33m', '').replace('[32m', '').replace('[31m', '').replace('[0m', '')
            
            html += f'<td {cell_class}>{cell}</td>'
        html += '</tr>'
    html += '</tbody></table></div>'
    
    return html

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get current date for default values
    current_date = datetime.now()
    default_data = {
        'year': current_date.year,
        'month': current_date.month,
        'start_day': current_date.day,
        'end_day': current_date.day
    }
    
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files and 'last_file' not in session:
            return jsonify({'error': 'No file selected'})
        
        file = request.files.get('file')
        if file and file.filename == '' and 'last_file' not in session:
            return jsonify({'error': 'No file selected'})
        
        # Use the last file if no new file is uploaded
        if not file or file.filename == '':
            file_path = session.get('last_file')
            if not file_path or not os.path.exists(file_path):
                return jsonify({'error': 'Please upload the file again'})
        else:
            if allowed_file(file.filename):
                # Save the uploaded file
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                session['last_file'] = file_path
                session['original_filename'] = file.filename
            else:
                return jsonify({'error': 'Invalid file type. Please upload an Excel file (.xlsx or .xls)'})
        
        # Get form data
        try:
            year = int(request.form.get('year', current_date.year))
            month = int(request.form.get('month', current_date.month))
            start_day = int(request.form.get('start_day', current_date.day))
            end_day = int(request.form.get('end_day', current_date.day))
        except ValueError:
            return jsonify({'error': 'Invalid date values'})
        
        try:
            # Clear local CSV before new calculation
            clear_local_csv()
            
            # Process the data
            df = load_data(file_path, 'Access History', 5)
            if df is not None:
                all_dates = [datetime(year, month, day).date() 
                           for day in range(start_day, end_day + 1)]
                
                results = process_multiple_dates(df, all_dates, current_date)
                summary = generate_summary_tables(results, current_date)
                
                # Convert terminal-style summary to web format
                web_summary = format_summary_for_web(summary)
                
                # Save results to both CSVs
                save_multiple_dates_to_csv(results, current_date, LOCAL_CSV_FILE)  # Local storage
                save_multiple_dates_to_csv(results, current_date)  # Original location
                
                # Calculate total difference
                start_date = datetime(year, month, start_day).date()
                end_date = datetime(year, month, end_day).date()
                
                total_diff = calculate_total_difference_from_csv(LOCAL_CSV_FILE, start_date, end_date)
                formatted_total_diff = format_total_difference(total_diff)
                
                return jsonify({
                    'success': True,
                    'summary': web_summary,
                    'total_difference_local': formatted_total_diff,
                    'current_file': session.get('original_filename', 'No file selected')
                })
            else:
                return jsonify({'error': 'Error processing the file'})
                
        except Exception as e:
            return jsonify({'error': f'Error: {str(e)}'})
    
    return render_template('index.html', 
                         default_data=default_data,
                         current_file=session.get('original_filename', 'No file selected'))

@app.route('/clear-session', methods=['POST'])
def clear_session():
    """Clear only the results but keep the file information"""
    # Don't remove the file or file information from session
    # Just hide the results on the frontend
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True) 