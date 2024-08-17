# app.py
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime, time, timedelta
import io
from spintly_day_till_current_time import parse_datetime, calculate_time_spent, format_time, analyze_time_spent

app = Flask(__name__)

# Constants
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds

# Helper functions (parse_datetime, calculate_time_spent, format_time) go here
# You can copy these from your original script

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'excel_file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['excel_file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    date_str = request.form['date_select']
    if date_str == 'today':
        date = datetime.now().date()
    elif date_str == 'yesterday':
        date = datetime.now().date() - timedelta(days=1)
    else:
        date = datetime.strptime(request.form['custom_date'], '%Y-%m-%d').date()
    
    try:
        df = pd.read_excel(file, sheet_name='Access History', skiprows=5)
        df['DateTime'] = df.apply(lambda row: parse_datetime(row['Date'], row['Time']), axis=1)
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y').dt.date
        df = df[['Date', 'DateTime', 'Name', 'Direction']].sort_values(by=['Name', 'DateTime'])
        
        time_spent = analyze_time_spent(df, date)
        
        if not time_spent:
            return render_template('index.html', error="No data found for the selected date.")
        
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
        
        return render_template('index.html', date=date.strftime('%b %d, %Y'), results=results)
    
    except Exception as e:
        return render_template('index.html', date=date.strftime('%b %d, %Y'), error=f"Error processing file: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)