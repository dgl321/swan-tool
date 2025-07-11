#!/usr/bin/env python3
"""
Test script to verify the new parameter-based naming convention.
"""

import sys
sys.path.append('.')

from routes import generate_parameter_string

def test_naming_convention():
    """Test the parameter string generation for different scenarios."""
    
    print("Testing Parameter-Based Naming Convention...")
    
    # Test cases
    test_cases = [
        {
            'name': 'No parameters',
            'form_data': {},
            'expected': ''
        },
        {
            'name': '10m L&M scenario only',
            'form_data': {'mitigation_scenario': '10m'},
            'expected': '_10L&M'
        },
        {
            'name': '20m L&M scenario only',
            'form_data': {'mitigation_scenario': '20m'},
            'expected': '_20L&M'
        },
        {
            'name': 'Nozzle reduction only',
            'form_data': {'nozzle_reduction': '90'},
            'expected': '_90N'
        },
        {
            'name': 'Buffer width only',
            'form_data': {'buffer_width': '20'},
            'expected': '_20B'
        },
        {
            'name': 'Complete scenario: 90N_20B_10L&M',
            'form_data': {
                'nozzle_reduction': '90',
                'buffer_width': '20',
                'mitigation_scenario': '10m'
            },
            'expected': '_90N_20B_10L&M'
        },
        {
            'name': 'Complete scenario: 50N_10B_20L&M',
            'form_data': {
                'nozzle_reduction': '50',
                'buffer_width': '10',
                'mitigation_scenario': '20m'
            },
            'expected': '_50N_10B_20L&M'
        },
        {
            'name': 'Nozzle and buffer only',
            'form_data': {
                'nozzle_reduction': '75',
                'buffer_width': '15'
            },
            'expected': '_75N_15B'
        }
    ]
    
    print("\nTest Results:")
    print("=" * 50)
    
    for test_case in test_cases:
        result = generate_parameter_string(test_case['form_data'])
        expected = test_case['expected']
        
        if result == expected:
            print(f"✅ {test_case['name']}")
            print(f"   Input: {test_case['form_data']}")
            print(f"   Output: '{result}'")
        else:
            print(f"❌ {test_case['name']}")
            print(f"   Input: {test_case['form_data']}")
            print(f"   Expected: '{expected}'")
            print(f"   Got: '{result}'")
        print()
    
    # Test example project names
    print("Example Project Names:")
    print("=" * 50)
    
    example_projects = [
        ('LLGL625', {'nozzle_reduction': '90', 'buffer_width': '20', 'mitigation_scenario': '10m'}),
        ('EXAMPLE', {'nozzle_reduction': '50', 'buffer_width': '10', 'mitigation_scenario': '20m'}),
        ('PROJECT', {'mitigation_scenario': '10m'}),
        ('SIMPLE', {'nozzle_reduction': '75'})
    ]
    
    for project_name, form_data in example_projects:
        param_string = generate_parameter_string(form_data)
        output_name = f"{project_name}{param_string}"
        print(f"{project_name} → {output_name}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_naming_convention() 