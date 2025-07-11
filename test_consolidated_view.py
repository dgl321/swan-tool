#!/usr/bin/env python3
"""
Test script to verify the consolidated project view works correctly.
"""

import requests
import os

def test_consolidated_view():
    """Test that the consolidated project view works correctly."""
    base_url = "http://localhost:8080"
    
    print("Testing Consolidated Project View...")
    
    # Test 1: Process a project path
    print("\n1. Processing test project...")
    test_project_path = "test_data/BIXSC45_1AP"
    
    if os.path.exists(test_project_path):
        process_data = {
            'project_paths': test_project_path
        }
        
        try:
            response = requests.post(f"{base_url}/process-paths", data=process_data)
            if response.status_code == 302:  # Redirect expected
                print("✓ Project processed successfully")
            else:
                print(f"✗ Project processing failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Error processing project: {e}")
    else:
        print(f"✗ Test project not found: {test_project_path}")
        return
    
    # Test 2: Check if the configuration page shows consolidated view
    print("\n2. Testing consolidated project view...")
    try:
        response = requests.get(f"{base_url}/configure")
        if response.status_code == 200:
            print("✓ Configuration page loads successfully")
            
            # Check if it shows consolidated project info
            if "files processed" in response.text:
                print("✓ Shows consolidated TXW file count")
            else:
                print("✗ Does not show consolidated TXW file count")
                
            # Check if it shows project name
            if "BIXSC45_1AP" in response.text:
                print("✓ Shows project name correctly")
            else:
                print("✗ Does not show project name")
                
            # Check if it shows substance and crop info
            if "Substance:" in response.text and "Crop:" in response.text:
                print("✓ Shows substance and crop information")
            else:
                print("✗ Does not show substance and crop information")
        else:
            print(f"✗ Configuration page failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing configuration page: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_consolidated_view() 