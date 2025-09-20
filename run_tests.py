#!/usr/bin/env python3
"""
Test runner script for the Zomato Restaurant Price Prediction application
"""
import subprocess
import sys
import os
import argparse


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {description}:")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Run tests for Zomato Restaurant Price Prediction App')
    parser.add_argument('--type', choices=['unit', 'integration', 'model', 'all'], 
                       default='all', help='Type of tests to run')
    parser.add_argument('--coverage', action='store_true', 
                       help='Run with coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Verbose output')
    parser.add_argument('--file', help='Run specific test file')
    
    args = parser.parse_args()
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("Error: app.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Build pytest command
    pytest_cmd = "pytest tests/"
    
    if args.file:
        pytest_cmd += f"/{args.file}"
    else:
        if args.type == 'unit':
            pytest_cmd += " -m unit"
        elif args.type == 'integration':
            pytest_cmd += " -m integration"
        elif args.type == 'model':
            pytest_cmd += " -m model"
        else:  # all
            pytest_cmd += ""
    
    if args.verbose:
        pytest_cmd += " -v"
    
    if args.coverage:
        pytest_cmd += " --cov=. --cov-report=html --cov-report=term-missing"
    
    # Run the tests
    success = run_command(pytest_cmd, "Running tests")
    
    if success:
        print(f"\n{'='*60}")
        print("✅ All tests completed successfully!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/index.html")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("❌ Some tests failed!")
        print(f"{'='*60}")
        sys.exit(1)


if __name__ == '__main__':
    main()
