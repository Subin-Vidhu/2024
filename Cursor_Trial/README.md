# Modern Radiologist Task Manager

A modern, responsive task management application built specifically for radiologists, featuring a clean UI with medical-themed design elements.

## Features
- Add, complete, and delete tasks
- Real-time updates without page refreshes
- Duplicate task detection
- Toast notifications for all actions
- Modern glass-morphism design
- Responsive layout for all devices
- Loading indicators for all actions
- Data persistence using SQLite
- Medical-themed color scheme
- Error handling with visual feedback

## Technology Stack
- Backend: Flask + SQLAlchemy
- Database: SQLite
- Frontend: Vanilla JavaScript + CSS
- Icons: Font Awesome

## Setup and Running

1. Activate the virtual environment:
   ```
   D:\2024\Cursor_Trial\venv\Scripts\activate  # On Windows
   source venv/bin/activate                    # On Unix/MacOS
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## UI Features
- Glass-morphism effect for cards
- Smooth animations and transitions
- Top-right toast notifications
- Loading spinners for async operations
- Medical-themed color palette
- Intuitive task management interface
- Empty state handling

## Data Features
- Automatic timestamp for each task
- Duplicate task prevention
- Real-time task updates
- Persistent storage
- Error handling and validation

## Security
- SQL injection prevention through SQLAlchemy
- Form validation
- Error boundary handling