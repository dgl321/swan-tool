#!/usr/bin/env python3
"""
Simple test script for the SWAN Parameter Generator Flask application.
"""

import os
import sys
import tempfile
import zipfile
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from app import app, allowed_file
        print("✓ Flask app imported successfully")
        
        from parsers.txw_parser import TXWParser
        print("✓ TXW parser imported successfully")
        
        from parsers.report_parser import ReportParser
        print("✓ Report parser imported successfully")
        
        from generators.tpf_generator import TPFGenerator
        print("✓ TPF generator imported successfully")
        
        from generators.bat_generator import BATGenerator
        print("✓ BAT generator imported successfully")
        
        from utils.zip_util import ZipUtil
        print("✓ ZIP utility imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_parsers():
    """Test the parser modules with sample data."""
    print("\nTesting parsers...")
    
    try:
        from parsers.txw_parser import TXWParser
        from parsers.report_parser import ReportParser
        
        # Test TXW parser
        txw_parser = TXWParser()
        print("✓ TXW parser initialized")
        
        # Test report parser
        report_parser = ReportParser()
        print("✓ Report parser initialized")
        
        return True
        
    except Exception as e:
        print(f"✗ Parser test error: {e}")
        return False

def test_generators():
    """Test the generator modules."""
    print("\nTesting generators...")
    
    try:
        from generators.tpf_generator import TPFGenerator
        from generators.bat_generator import BATGenerator
        
        # Test TPF generator
        tpf_generator = TPFGenerator()
        print("✓ TPF generator initialized")
        
        # Test BAT generator
        bat_generator = BATGenerator()
        print("✓ BAT generator initialized")
        
        return True
        
    except Exception as e:
        print(f"✗ Generator test error: {e}")
        return False

def test_zip_utility():
    """Test the ZIP utility module."""
    print("\nTesting ZIP utility...")
    
    try:
        from utils.zip_util import ZipUtil
        
        zip_util = ZipUtil()
        print("✓ ZIP utility initialized")
        
        return True
        
    except Exception as e:
        print(f"✗ ZIP utility test error: {e}")
        return False

def test_file_structure():
    """Test that required directories and files exist."""
    print("\nTesting file structure...")
    
    required_dirs = ['parsers', 'generators', 'utils', 'templates', 'uploads', 'temp']
    required_files = [
        'app.py',
        'routes.py',
        'requirements.txt',
        'README.md',
        'parsers/__init__.py',
        'parsers/txw_parser.py',
        'parsers/report_parser.py',
        'generators/__init__.py',
        'generators/tpf_generator.py',
        'generators/bat_generator.py',
        'utils/__init__.py',
        'utils/zip_util.py',
        'templates/base.html',
        'templates/index.html',
        'templates/configure.html',
        'templates/download.html'
    ]
    
    all_good = True
    
    # Check directories
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ Directory '{dir_name}' exists")
        else:
            print(f"✗ Directory '{dir_name}' missing")
            all_good = False
    
    # Check files
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✓ File '{file_name}' exists")
        else:
            print(f"✗ File '{file_name}' missing")
            all_good = False
    
    return all_good

def test_sample_data():
    """Test that sample data exists and can be accessed."""
    print("\nTesting sample data...")
    
    if os.path.exists('test_data'):
        print("✓ test_data directory exists")
        
        # Check for sample project
        sample_project = 'test_data/BIXSC45_1AP'
        if os.path.exists(sample_project):
            print("✓ Sample project directory exists")
            
            # Check for TOXSWA subfolder
            toxswa_path = os.path.join(sample_project, 'TOXSWA')
            if os.path.exists(toxswa_path):
                print("✓ TOXSWA subfolder exists")
                
                # Check for .txw files
                txw_files = [f for f in os.listdir(toxswa_path) if f.endswith('.txw')]
                if txw_files:
                    print(f"✓ Found {len(txw_files)} .txw files")
                else:
                    print("✗ No .txw files found")
                    return False
            else:
                print("✗ TOXSWA subfolder missing")
                return False
        else:
            print("✗ Sample project directory missing")
            return False
    else:
        print("✗ test_data directory missing")
        return False
    
    return True

def main():
    """Run all tests."""
    print("SWAN Parameter Generator - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_parsers,
        test_generators,
        test_zip_utility,
        test_file_structure,
        test_sample_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The application should work correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 