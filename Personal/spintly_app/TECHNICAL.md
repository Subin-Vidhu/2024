# Technical Documentation - Spintly Time Calculator

## Architecture

The application follows a client-server architecture using Flask:
- Backend: Python Flask application
- Frontend: HTML with Bootstrap 5 and vanilla JavaScript
- Data Storage: CSV files for persistent storage

## Core Components

### 1. Main Application (`main.py`)
- Entry point for the application
- Configures the Flask server
- Handles browser launch
- Sets up working directories

### 2. Application Logic (`app.py`)
- Flask routes and core business logic
- Data processing and calculations
- File handling and session management

### 3. Frontend (`templates/index.html`)
- Responsive Bootstrap 5 interface
- AJAX-based form submission
- Real-time result updates
- Print-friendly styling

## Key Functions

### Time Calculation
```python
def calculate_time_spent(group: pd.DataFrame, current_time: datetime = None, truncate: bool = False) -> Dict[str, float]:
    """
    Calculates time spent in office with the following components:
    - Total time: Overall time between first entry and last exit
    - Office hours time: Time within standard office hours (7:30 AM - 7:30 PM)
    - Break time: Gaps between exit and next entry
    """
```

### Data Processing
```python
def load_data(file_path: str, sheet_name: str, skip_rows: int) -> pd.DataFrame:
    """
    Loads and preprocesses Excel data:
    1. Reads Excel file with pandas
    2. Converts date/time strings to datetime objects
    3. Sorts data by name and datetime
    """
```

### Summary Generation
```python
def generate_summary_tables(results: Dict[datetime.date, Dict[str, Dict[str, float]]], current_time: datetime) -> str:
    """
    Generates formatted summary tables:
    - One table with seconds precision
    - One table without seconds
    - Includes status indicators and time differences
    """
```

## Data Flow

1. **File Upload**:
   - Excel file → Temporary storage in uploads folder
   - File path stored in session

2. **Data Processing**:
   - Excel → Pandas DataFrame
   - DataFrame → Time calculations
   - Calculations → Summary tables

3. **Data Storage**:
   - Results → Local CSV
   - Session information → Flask session

## Configuration Constants

```python
# Time Constants
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds

# File Handling
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
UPLOAD_FOLDER = 'uploads'
CSV_STORAGE = 'data'
```

## Dependencies

```plaintext
flask==2.0.1
pandas==1.3.3
openpyxl==3.0.9
tabulate==0.8.9
colorama==0.4.4
Werkzeug==2.0.1
pillow==11.1.0
```

## Directory Structure

```
spintly_app/
├── main.py              # Entry point
├── app.py              # Core application
├── requirements.txt    # Dependencies
├── README.md          # User documentation
├── TECHNICAL.md       # Technical documentation
├── templates/         # HTML templates
│   └── index.html    # Main interface
├── uploads/          # Temporary file storage
└── data/             # CSV storage
```

## Error Handling

- File validation for Excel formats
- Exception handling for data processing
- User-friendly error messages
- Session management for file persistence

## Security Considerations

- Secure file uploads with `secure_filename`
- Session-based file tracking
- No sensitive data storage
- Input validation for all form fields

## Performance Optimization

- Efficient pandas operations
- Minimal database operations
- Client-side data handling
- Responsive UI design

## Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --add-data "data;data" --add-data "uploads;uploads" main.py
```

## Future Improvements

1. Database Integration
   - Replace CSV with proper database
   - Add user authentication

2. Enhanced Features
   - Multiple file processing
   - Custom time range definitions
   - Export in multiple formats

3. UI Enhancements
   - Interactive charts
   - Custom theme support
   - Mobile app version 