from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session, jsonify
import os
from datetime import datetime
import pandas as pd
from werkzeug.utils import secure_filename
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spintly_daily_time_multiple_days import (
    load_data, process_multiple_dates, generate_summary_tables,
    save_multiple_dates_to_csv, calculate_total_difference_from_csv
)

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