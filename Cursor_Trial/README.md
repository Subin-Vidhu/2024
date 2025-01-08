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

## Technology Stack
- Backend: Flask 2.3.3 + SQLAlchemy 2.0.23 + Gunicorn 21.2.0
- Database: SQLite
- Frontend: Vanilla JavaScript + CSS
- Icons: Font Awesome 6.0.0
- No additional JavaScript frameworks required

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

6. Server Configuration (Recommended):
   ```
   # Generate optimal server configuration based on your system
   python system_info.py
   ```
   This will create a system_info.json file with recommended server settings based on your CPU cores and system specifications.

7. Production Mode (Recommended):
   ```
   # On Unix/MacOS/Linux
   gunicorn -w 4 -b 0.0.0.0:8000 app:app

   # On Windows (using waitress as Gunicorn is not supported)
   # Use 4-8 threads per CPU core. For a 4-core CPU, 16-32 threads would be reasonable
   waitress-serve --port=8000 --threads=16 app:app
   ```
   Note: Use the command provided by system_info.py for optimal configuration on your system.

8. Open your browser and navigate to:
   ```
   # For development mode
   http://localhost:5000

   # For production mode
   http://localhost:8000
   ```

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