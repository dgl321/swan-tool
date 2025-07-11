#!/usr/bin/env python3
"""
Test script for the new FOCUS mitigation scenario functionality.
"""

import requests
import json
import os

def test_mitigation_scenarios():
    """Test the new mitigation scenario functionality."""
    base_url = "http://localhost:8080"
    
    print("Testing FOCUS Mitigation Scenarios...")
    
    # Test 1: Process a project path first
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
    
    # Test 2: Check if the configuration page loads with processed projects
    print("\n2. Testing configuration page with processed projects...")
    try:
        response = requests.get(f"{base_url}/configure")
        if response.status_code == 200:
            print("✓ Configuration page loads successfully")
            
            # Check if the new dropdown is present
            if "mitigation_scenario" in response.text:
                print("✓ Mitigation scenario dropdown is present")
            else:
                print("✗ Mitigation scenario dropdown not found")
                
            # Check if FOCUS scenarios are mentioned
            if "FOCUS" in response.text:
                print("✓ FOCUS scenarios are mentioned")
            else:
                print("✗ FOCUS scenarios not found")
                
            # Check if the specific scenario options are present
            if "10m VFS Buffer" in response.text:
                print("✓ 10m VFS Buffer option is present")
            else:
                print("✗ 10m VFS Buffer option not found")
                
            if "20m VFS Buffer" in response.text:
                print("✓ 20m VFS Buffer option is present")
            else:
                print("✗ 20m VFS Buffer option not found")
        else:
            print(f"✗ Configuration page failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing configuration page: {e}")
    
    # Test 3: Simulate form submission with 10m scenario
    print("\n3. Testing 10m VFS Buffer scenario...")
    test_data = {
        'mitigation_scenario': '10m',
        'num_applications': '1',
        'output_project_path': 'C:\\SwashProjects\\Output',
        'vapour_pressure': '4.60e-08',
        'nozzle_reduction': '0',
        'buffer_width': '0',
        'use_step3_mass_loadings': 'off',
        'select_buffer_width': 'off'
    }
    
    try:
        response = requests.post(f"{base_url}/generate", data=test_data)
        print(f"✓ Form submission completed with status: {response.status_code}")
    except Exception as e:
        print(f"✗ Error in form submission: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_mitigation_scenarios() 