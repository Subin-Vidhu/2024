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