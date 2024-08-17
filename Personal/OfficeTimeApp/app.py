from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from datetime import datetime, time, timedelta
import io
import os
from werkzeug.utils import secure_filename
from spintly_day_till_current_time import parse_datetime, calculate_time_spent, format_time, analyze_time_spent

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management
app.config['UPLOAD_FOLDER'] = os.path.join("static", 'temp_uploads')  # Folder to store temporary uploads

# Constants
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds

@app.route('/')
def index():
    return render_template('index.html', file_uploaded=session.get('file_uploaded', False))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'excel_file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['excel_file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        session['file_path'] = file_path
        session['file_uploaded'] = True
        return redirect(url_for('index'))

@app.route('/analyze', methods=['GET'])
def analyze():
    if 'file_path' not in session:
        return {'error': 'Please upload a file first.'}, 400
    
    date_string = request.args.get('date')
    date = datetime.strptime(date_string, '%Y-%m-%d').date()
    
    try:
        df = pd.read_excel(session['file_path'], sheet_name='Access History', skiprows=5)
        df['DateTime'] = df.apply(lambda row: parse_datetime(row['Date'], row['Time']), axis=1)
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y').dt.date
        df = df[['Date', 'DateTime', 'Name', 'Direction']].sort_values(by=['Name', 'DateTime'])
        
        time_spent = analyze_time_spent(df, date)
        
        if not time_spent:
            return {'error': 'No data found for the selected date.'}, 400
        
        results = []
        for name, times in time_spent.items():
            if '_no_seconds' in name:
                continue
            
            target_met = times['office'] >= TARGET_TIME
            difference = abs(TARGET_TIME - times['office'])
            
            results.append({
                'name': name,
                'total_time': format_time(times['total']),
                'office_time': format_time(times['office']),
                'break_time': format_time(times['break']),
                'target': '✓' if target_met else '✗',
                'target_met': target_met,
                'difference': f"{'+' if target_met else '-'}{format_time(difference)}",
                'last_exit': times['last_exit'].strftime("%I:%M:%S %p")
            })
        
        for name, times in time_spent.items():
            if '_no_seconds' not in name:
                continue
            
            target_met = times['office'] >= TARGET_TIME
            difference = abs(TARGET_TIME - times['office'])
            
            results.append({
                'name': name,
                'total_time': format_time(times['total']),
                'office_time': format_time(times['office']),
                'break_time': format_time(times['break']),
                'target': '✓' if target_met else '✗',
                'target_met': target_met,
                'difference': f"{'+' if target_met else '-'}{format_time(difference)}",
                'last_exit': times['last_exit'].strftime("%I:%M %p")
            })
        
        return {'results': results}
    
    except Exception as e:
        return {'error': f"Error processing file: {str(e)}"}, 500

@app.route('/clear', methods=['POST'])
def clear_file():
    if 'file_path' in session:
        os.remove(session['file_path'])
        session.pop('file_path', None)
    session['file_uploaded'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)