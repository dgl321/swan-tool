#!/usr/bin/env python3
"""
Run script for the SWAN Parameter Generator Flask application.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the Flask application."""
    try:
        from app import app
        
        print("=" * 60)
        print("SWAN Parameter Generator")
        print("=" * 60)
        print("Starting Flask application...")
        print("Access the web interface at: http://localhost:8080")
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the Flask app
        app.run(
            host='127.0.0.1',
            port=8080,
            debug=True,
            use_reloader=True
        )
        
    except ImportError as e:
        print(f"Error importing application: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 