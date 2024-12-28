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
- Backend: Flask 3.0.0 + SQLAlchemy 2.0.23
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

5. Run the application:
   ```
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

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