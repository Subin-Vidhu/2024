import os
import sys
import webbrowser
from threading import Timer
from app import app

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5555/')

def main():
    # Set the working directory to the script's location
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle
        application_path = sys._MEIPASS
    else:
        # If the application is run from a Python interpreter
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(application_path)
    
    # Open browser after 1.5 seconds
    Timer(1.5, open_browser).start()
    
    # Run the Flask app
    app.run(port=5555, debug=False)

if __name__ == '__main__':
    main() 