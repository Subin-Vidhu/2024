# Spintly Time Calculator

A web-based application that calculates and tracks office hours from Spintly access logs. The application provides detailed time summaries, including office hours, break times, and cumulative time differences.

## Features

- **Excel File Upload**: Upload Spintly access log files in Excel format (.xlsx, .xls)
- **Date Range Selection**: Calculate time for specific dates or date ranges
- **Detailed Time Analysis**:
  - Total time spent in office
  - Office hours during standard working hours (7:30 AM - 7:30 PM)
  - Break time calculations
  - Target completion status
- **Two Calculation Modes**:
  - With Seconds: Precise time calculations including seconds
  - Without Seconds: Rounded calculations for general overview
- **Visual Indicators**:
  - ✓ (Green): Target met
  - ✗ (Red): Target not met
  - Yellow: Current day, target not yet met
- **Data Export**: Saves calculations to CSV for record keeping
- **Responsive Design**: Works on both desktop and mobile devices

## Getting Started

1. **Installation**:
   ```bash
   # Clone the repository
   git clone [repository-url]
   cd spintly_app

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Running the Application**:
   ```bash
   python main.py
   ```
   The application will automatically open in your default web browser at http://127.0.0.1:5555

3. **Using the Application**:
   - Upload your Spintly access log Excel file
   - Select the year, month, and date range
   - Click "Calculate Time" to view results
   - Use "Start New Calculation" to process another date range
   - Print results using the "Print Results" button

## Requirements

- Python 3.9 or higher
- Excel files from Spintly access logs with the following columns:
  - Date
  - Time
  - Name
  - Direction (Entry/Exit)

## Target Time Configuration

- Standard office hours: 7:30 AM - 7:30 PM
- Target working hours: 8 hours 30 minutes per day
- Maximum extra hours considered: 1 hour per day

## Support

For issues, questions, or suggestions, please contact [your-contact-info] 