import os
import sys
import pytest

def run_tests():
    """Run all tests with coverage report."""
    # Add current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Run pytest with coverage
    args = [
        '--verbose',
        '--cov=.',
        '--cov-report=term-missing',
        '--cov-report=html',
        'tests/'
    ]
    
    print("\nRunning tests with coverage report...")
    result = pytest.main(args)
    
    if result == 0:
        print("\n✅ All tests passed!")
        print("\nCoverage report has been generated in 'htmlcov' directory")
        print("Open htmlcov/index.html in your browser to view the detailed report")
    else:
        print("\n❌ Some tests failed!")
        print("Please fix the failing tests before deploying to production")
    
    return result

if __name__ == "__main__":
    sys.exit(run_tests()) 