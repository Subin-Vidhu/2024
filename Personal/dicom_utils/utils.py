"""
Utility functions for DICOM processing
"""

import json

def get_orig_value_format(value):
    """
    Get original value format for proper serialization
    to maintain exact numeric representation (e.g., "70" vs "70.0")
    
    Args:
        value: The value to format
    
    Returns:
        String representation of the value
    """
    if isinstance(value, (int, float)):
        return str(value)
    return value

def format_numeric_value(value, original_str):
    """
    Format numeric value to match original string format exactly
    
    Args:
        value: The numeric value to format
        original_str: The original string representation to match
    
    Returns:
        Formatted value
    """
    if isinstance(value, (int, float)) and isinstance(original_str, str):
        # If original has no decimal point but is a float, remove the .0
        if '.' not in original_str and str(value).endswith('.0'):
            return int(value)
        # If original is in scientific notation, match that format
        if 'e' in original_str.lower():
            # Try to match the exact scientific notation
            original_e_pos = original_str.lower().find('e')
            original_exp = original_str[original_e_pos:]
            # Handle differences in exponent notation (e-012 vs e-12)
            if '-0' in original_exp:
                return float(str(value).replace('e-', 'e-0'))
    return value 