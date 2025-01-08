import os
import json
import pytest
from system_info import get_lan_ip, get_system_info, save_system_info

def test_get_lan_ip():
    """Test LAN IP retrieval."""
    ip = get_lan_ip()
    assert ip is not None
    # Should be either a valid IP or the fallback
    assert ip == '0.0.0.0' or len(ip.split('.')) == 4

def test_get_system_info():
    """Test system information collection."""
    info = get_system_info()
    
    # Check CPU info
    assert 'cpu' in info
    assert info['cpu']['physical_cores'] > 0
    assert info['cpu']['total_cores'] >= info['cpu']['physical_cores']
    
    # Check memory info
    assert 'memory' in info
    assert info['memory']['total'] > 0
    assert info['memory']['available'] <= info['memory']['total']
    
    # Check system info
    assert 'system' in info
    assert info['system']['os'] in ['Windows', 'Linux', 'Darwin']
    assert info['system']['lan_ip'] is not None
    
    # Check server config
    assert 'server_config' in info
    if info['system']['os'].lower() == 'windows':
        assert info['server_config']['server'] == 'waitress'
        assert 'threads' in info['server_config']['command']
    else:
        assert info['server_config']['server'] == 'gunicorn'
        assert 'workers' in info['server_config']['command']

def test_save_system_info(tmp_path):
    """Test saving system information to file."""
    # Use temporary directory for test
    test_file = tmp_path / "test_system_info.json"
    
    # Save info
    result = save_system_info(str(test_file))
    assert result == True
    
    # Verify file exists and is valid JSON
    assert test_file.exists()
    with open(test_file) as f:
        data = json.load(f)
    
    # Check essential fields
    assert 'cpu' in data
    assert 'memory' in data
    assert 'system' in data
    assert 'server_config' in data
    
    # Check memory values are formatted
    assert isinstance(data['memory']['total'], str)
    assert 'GB' in data['memory']['total']
    
    # Check CPU frequency is formatted
    if data['cpu']['cpu_frequency']['max']:
        assert 'MHz' in data['cpu']['cpu_frequency']['max']

def test_server_command_generation():
    """Test server command generation for different platforms."""
    info = get_system_info()
    config = info['server_config']
    
    # Check command format
    assert 'command' in config
    assert '--port=8000' in config['command']
    assert config['url'].startswith('http://')
    
    # Check platform-specific settings
    if info['system']['os'].lower() == 'windows':
        assert 'waitress-serve' in config['command']
        assert '--threads=' in config['command']
    else:
        assert 'gunicorn' in config['command']
        assert '-w ' in config['command'] 