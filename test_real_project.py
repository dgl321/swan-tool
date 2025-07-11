#!/usr/bin/env python3
"""
Test script to test with real LLGL625 project data.
"""

import requests
import os

def test_real_project():
    """Test with real LLGL625 project data."""
    base_url = "http://localhost:8080"
    
    print("Testing with Real LLGL625 Project...")
    
    # Test 1: Process the real LLGL625 project
    print("\n1. Processing LLGL625 project...")
    real_project_path = "/Users/dylangrimeslarkin/Library/CloudStorage/OneDrive-LifeScientific/A/LLGL625"
    
    if os.path.exists(real_project_path):
        process_data = {
            'project_paths': real_project_path
        }
        
        try:
            response = requests.post(f"{base_url}/process-paths", data=process_data)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 302:  # Redirect expected
                print("✓ Project processed successfully")
            else:
                print(f"✗ Project processing failed: {response.status_code}")
                print(f"Response content: {response.text[:500]}")
        except Exception as e:
            print(f"✗ Error processing project: {e}")
    else:
        print(f"✗ Real project not found: {real_project_path}")
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
            if "LLGL625" in response.text:
                print("✓ Shows project name correctly")
            else:
                print("✗ Does not show project name")
                
            # Check if it shows substance and crop info
            if "Substance:" in response.text and "Crop:" in response.text:
                print("✓ Shows substance and crop information")
            else:
                print("✗ Does not show substance and crop information")
                
            # Check if it shows the correct number of TXW files
            if "11 files processed" in response.text:
                print("✓ Shows correct number of TXW files")
            else:
                print("✗ Does not show correct number of TXW files")
        else:
            print(f"✗ Configuration page failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing configuration page: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_real_project() 