import json
import os
import platform
import psutil
import multiprocessing

def get_system_info():
    """Collect system information relevant for server configuration."""
    
    # Get CPU information
    cpu_info = {
        'physical_cores': psutil.cpu_count(logical=False),
        'total_cores': psutil.cpu_count(logical=True),
        'cpu_frequency': {
            'max': psutil.cpu_freq().max if psutil.cpu_freq() else None,
            'current': psutil.cpu_freq().current if psutil.cpu_freq() else None
        },
        'cpu_usage_percent': psutil.cpu_percent(interval=1)
    }
    
    # Get memory information
    memory = psutil.virtual_memory()
    memory_info = {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'free': memory.free,
        'percent_used': memory.percent
    }
    
    # Get system information
    system_info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'python_version': platform.python_version()
    }
    
    # Calculate recommended server configuration
    is_windows = system_info['os'].lower() == 'windows'
    
    if is_windows:
        # Waitress configuration (threads)
        min_threads = cpu_info['physical_cores'] * 4
        max_threads = cpu_info['physical_cores'] * 8
        recommended_threads = min(max(min_threads, 16), max_threads)
        server_config = {
            'server': 'waitress',
            'min_threads': min_threads,
            'max_threads': max_threads,
            'recommended_threads': recommended_threads,
            'command': f'waitress-serve --port=8000 --threads={recommended_threads} app:app'
        }
    else:
        # Gunicorn configuration (workers)
        min_workers = cpu_info['physical_cores'] * 2
        max_workers = cpu_info['physical_cores'] * 4
        recommended_workers = min(max(min_workers, 4), max_workers)
        server_config = {
            'server': 'gunicorn',
            'min_workers': min_workers,
            'max_workers': max_workers,
            'recommended_workers': recommended_workers,
            'command': f'gunicorn -w {recommended_workers} -b 0.0.0.0:8000 app:app'
        }
    
    # Combine all information
    full_info = {
        'cpu': cpu_info,
        'memory': memory_info,
        'system': system_info,
        'server_config': server_config,
        'timestamp': psutil.datetime.datetime.now().isoformat()
    }
    
    return full_info

def save_system_info(filename='system_info.json'):
    """Save system information to a JSON file."""
    try:
        info = get_system_info()
        
        # Convert memory values to GB for better readability
        for key in ['total', 'available', 'used', 'free']:
            info['memory'][key] = f"{info['memory'][key] / (1024**3):.2f} GB"
        
        # Format CPU frequency to MHz
        if info['cpu']['cpu_frequency']['max']:
            info['cpu']['cpu_frequency']['max'] = f"{info['cpu']['cpu_frequency']['max']:.0f} MHz"
        if info['cpu']['cpu_frequency']['current']:
            info['cpu']['cpu_frequency']['current'] = f"{info['cpu']['cpu_frequency']['current']:.0f} MHz"
        
        with open(filename, 'w') as f:
            json.dump(info, f, indent=4)
        
        print(f"System information has been saved to {filename}")
        print("\nRecommended server configuration:")
        print(f"Server: {info['server_config']['server']}")
        if info['server_config']['server'] == 'waitress':
            print(f"Recommended threads: {info['server_config']['recommended_threads']}")
        else:
            print(f"Recommended workers: {info['server_config']['recommended_workers']}")
        print(f"Command: {info['server_config']['command']}")
        
        return True
    except Exception as e:
        print(f"Error saving system information: {str(e)}")
        return False

if __name__ == "__main__":
    save_system_info() 