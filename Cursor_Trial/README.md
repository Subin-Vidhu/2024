# Modern Radiologist Task Manager

A modern, responsive task management application built specifically for radiologists, featuring a clean UI with medical-themed design elements. This application helps radiologists organize their workflow efficiently with real-time updates and a beautiful glass-morphism design.

## Features

### Core Functionality
- Add, complete, and delete tasks with real-time updates
- Batch operations: Complete all tasks or delete all tasks at once
- Duplicate task detection to prevent redundancy
- Task history tracking with detailed activity logs
- Admin-protected history clearing functionality

### User Interface
- Modern glass-morphism design with medical theme
- Responsive layout optimized for all devices
- Smooth animations and transitions
- Toast notifications for all actions
- Loading indicators for async operations
- Empty state handling
- Floating action buttons for quick access
- Medical-themed color scheme

### Technical Features
- Real-time updates without page refreshes
- Data persistence using SQLite
- Automatic timestamps in Indian Standard Time (IST)
- SQL injection prevention through SQLAlchemy
- Form validation and error handling
- Error boundary handling
- Comprehensive test suite with coverage reporting

## Technology Stack
- Backend: Flask 2.3.3 + SQLAlchemy 2.0.23 + Gunicorn 21.2.0
- Database: SQLite
- Frontend: Vanilla JavaScript + CSS
- Icons: Font Awesome 6.0.0
- No additional JavaScript frameworks required

## Testing

### Running Tests
Before deploying to production, run the test suite to ensure everything works correctly:
```bash
python run_tests.py
```

This will:
1. Run all test cases
2. Generate a coverage report
3. Show test results in the terminal
4. Create a detailed HTML coverage report

### Test Coverage
The test suite measures code coverage, which indicates how thoroughly your code is being tested:

#### Coverage Metrics
- **Line Coverage**: Which lines of code were executed during tests
- **Branch Coverage**: Whether each conditional branch (if/else) was tested
- **Function Coverage**: Which functions were called during tests
- **Statement Coverage**: Which statements were executed

#### Current Coverage Status
```
Component          Coverage    Notes
----------------|-----------|-------------------
app.py              97%      Core application code
system_info.py      82%      System configuration
test files         100%      Test suite itself
Overall            80%      Total codebase
```

#### Understanding Coverage Reports
1. **Terminal Report**:
   - Shows pass/fail status for each test
   - Displays overall coverage percentage
   - Lists untested lines of code

2. **HTML Report** (in htmlcov/index.html):
   - Interactive coverage visualization
   - Line-by-line coverage analysis
   - Color-coded coverage indicators:
     - Green: Covered code
     - Red: Uncovered code
     - Yellow: Partially covered branches

3. **Missing Coverage**:
   - Startup/shutdown code
   - Error handling edge cases
   - Some system configuration paths

### Test Categories
The test suite includes:
- API endpoint tests
- Database operation tests
- System configuration tests
- Error handling tests
- Edge case testing

### Test Reports
After running tests:
1. View the terminal output for quick results
2. Open `htmlcov/index.html` in your browser for:
   - Detailed coverage analysis
   - Line-by-line code coverage
   - Missing coverage identification
   - Branch coverage visualization

### Interpreting Test Results

#### Terminal Output
```
=========================================== test session starts ===========================================
platform win32 -- Python 3.9.12, pytest-8.0.0, pluggy-1.5.0
collected 12 items

tests/test_api.py::test_index_page PASSED                   [  8%]
tests/test_api.py::test_add_task PASSED                     [ 16%]
...
============================================ 12 passed in 6.81s =========================================
```

- ✅ PASSED: Test completed successfully
- ❌ FAILED: Test encountered an error
- 🔸 SKIPPED: Test was not run
- ⚠️ WARNING: Potential issues detected

#### Coverage Report
```
Name                    Stmts   Miss  Cover   Missing
-------------------------------------------------
app.py                    108      3    97%   216-217, 223
system_info.py            60     11    82%   18-19, 75-78
```

- **Stmts**: Total lines of code
- **Miss**: Untested lines
- **Cover**: Percentage of code tested
- **Missing**: Line numbers not covered

#### Common Issues
1. **Failed Tests**:
   - Check the error message
   - Look for assertion failures
   - Verify test data setup

2. **Low Coverage**:
   - Identify uncovered code
   - Add missing test cases
   - Test edge conditions

3. **Warnings**:
   - Deprecation notices
   - Configuration issues
   - Best practice violations

### Continuous Testing
Run tests:
- After making code changes
- Before deploying to production
- When updating dependencies
- After system configuration changes

### Improving Coverage
To improve test coverage:
1. Add tests for uncovered lines
2. Test error conditions
3. Add edge case scenarios
4. Test configuration variations

## Setup and Running

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the application:
   - Create a `config.json` file in the root directory with the following structure:
     ```json
     {
       "database": {
         "uri": "sqlite:///instance/todo.db"
       },
       "flask": {
         "secret_key": "your-secret-key",
         "debug": true
       },
       "admin": {
         "history_clear_code": "your-admin-code"
       }
     }
     ```

5. Development Mode:
   ```
   python app.py
   ```
   The development server will be accessible:
   - Locally: http://localhost:5000
   - Over LAN: http://<your-ip>:5000

6. Server Configuration (Recommended):
   ```
   # Generate optimal server configuration based on your system
   python system_info.py
   ```
   This will create a system_info.json file with:
   - CPU information (cores, frequency, usage)
   - Memory statistics
   - OS and system details
   - Network information (LAN IP)
   - Recommended server configuration (Gunicorn/Waitress)
   - Optimal number of workers/threads for your hardware
   - Ready-to-use server command

   Example output:
   ```
   System information has been saved to system_info.json

   System Network Information:
   LAN IP: 192.168.1.100

   Recommended server configuration:
   Server: waitress
   Recommended threads: 16
   Command: waitress-serve --port=8000 --threads=16 --host=192.168.1.100 app:app

   Access your application at: http://192.168.1.100:8000
   ```

7. Production Mode (Recommended):
   ```
   # Run the production server with optimal configuration
   python run_production.py
   ```
   This will automatically:
   - Use the optimal configuration from system_info.json
   - Set proper production environment variables
   - Use Gunicorn on Unix/Linux or Waitress on Windows
   - Configure optimal number of workers/threads for your CPU
   - Make the application accessible over LAN
   - Provide graceful shutdown on Ctrl+C

   Manual commands (if needed):
   ```
   # On Unix/MacOS/Linux
   gunicorn -w 4 -b <your-ip>:8000 app:app

   # On Windows
   waitress-serve --port=8000 --threads=16 --host=<your-ip> app:app
   ```

8. Access the Application:
   ```
   # For development mode
   Local: http://localhost:5000
   LAN: http://<your-ip>:5000

   # For production mode
   Local: http://localhost:8000
   LAN: http://<your-ip>:8000
   ```
   Replace <your-ip> with your actual LAN IP (shown by system_info.py)

### Production Deployment Notes
- Use Gunicorn in production with multiple workers (2-4x number of CPU cores)
- Configure a reverse proxy (Nginx/Apache) in front of Gunicorn
- Set debug=False in config.json for production
- Use environment variables for sensitive configuration

## Usage

### Task Management
- Add tasks using the input field at the top
- Click the circle icon to mark tasks as complete/incomplete
- Click the trash icon to delete individual tasks
- Use floating buttons to:
  - View task history
  - Complete all tasks at once
  - Delete all tasks at once

### History Management
- Click the "View History" button to see all task activities
- History shows creation, completion, and deletion of tasks
- Admin can clear history using a protected code

## Security
- SQL injection prevention through SQLAlchemy
- Form validation for all inputs
- Admin code protection for sensitive operations
- Error boundary handling for all operations

## Browser Compatibility
- Works on all modern browsers (Chrome, Firefox, Safari, Edge)
- Responsive design works on mobile devices
- Minimum recommended screen width: 320px

## License
© 2024 Radiologist Task Manager. All rights reserved.