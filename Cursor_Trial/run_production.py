import json
import os
import subprocess
import sys

def load_system_info(filename='system_info.json'):
    """Load system configuration from JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: system_info.json not found. Please run system_info.py first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in system_info.json")
        sys.exit(1)

def run_production_server():
    """Run the production server using optimal configuration."""
    # Load system information
    info = load_system_info()
    server_config = info['server_config']
    
    # Print system summary
    print("\nSystem Summary:")
    print(f"OS: {info['system']['os']} {info['system']['architecture']}")
    print(f"CPU Cores: {info['cpu']['physical_cores']} physical, {info['cpu']['total_cores']} total")
    print(f"Server: {server_config['server']}")
    
    # Get the command from server configuration
    cmd = server_config['command']
    
    # Add environment variables for production
    env = os.environ.copy()
    env['FLASK_ENV'] = 'production'
    env['FLASK_DEBUG'] = '0'
    
    print(f"\nStarting production server with command:\n{cmd}")
    print("\nPress Ctrl+C to stop the server...")
    
    try:
        # Run the server
        process = subprocess.Popen(
            cmd.split(),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Stream the output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        rc = process.poll()
        return rc
        
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        process.terminate()
        try:
            process.wait(timeout=5)  # Give it 5 seconds to shutdown gracefully
        except subprocess.TimeoutExpired:
            process.kill()  # Force kill if it doesn't shutdown gracefully
        print("Server stopped.")
    except Exception as e:
        print(f"Error running server: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(run_production_server()) 