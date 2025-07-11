#!/usr/bin/env python3
"""
Test script for multi-parameter selection functionality.
"""

import os
import sys
import tempfile
import shutil

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from routes import generate_parameter_string_from_combination, prepare_tpf_parameters_for_combination

def test_parameter_combinations():
    """Test various parameter combinations."""
    
    # Test combinations
    test_combinations = [
        {'nozzle': 0, 'runoff': '', 'buffer': 0},  # No parameters
        {'nozzle': 70, 'runoff': '10m', 'buffer': 0},  # 70% nozzle, 10m runoff
        {'nozzle': 90, 'runoff': '20m', 'buffer': 10},  # 90% nozzle, 20m runoff, 10m buffer
        {'nozzle': 50, 'runoff': '', 'buffer': 5},  # 50% nozzle, 5m buffer
        {'nozzle': 0, 'runoff': '10m', 'buffer': 20},  # 10m runoff, 20m buffer
    ]
    
    print("Testing parameter string generation:")
    print("=" * 50)
    
    for i, combo in enumerate(test_combinations, 1):
        param_string = generate_parameter_string_from_combination(combo)
        print(f"Combination {i}: {combo}")
        print(f"  Parameter string: '{param_string}'")
        print()
    
    # Test TPF parameter preparation
    print("Testing TPF parameter preparation:")
    print("=" * 50)
    
    # Mock project data
    mock_project = {
        'project_name': 'TEST_PROJECT',
        'crop': 'Wheat',
        'substance_name': 'TestSubstance',
        'scenarios': ['scenario1', 'scenario2'],
        'vapour_pressure': 2.0e-07
    }
    
    # Mock form data
    mock_form_data = {
        'num_applications': '1',
        'output_project_path': 'C:\\Test\\Output',
        'use_step3_mass_loadings': 'on',
        'select_buffer_width': 'off'
    }
    
    for i, combo in enumerate(test_combinations, 1):
        print(f"Testing combination {i}: {combo}")
        try:
            params = prepare_tpf_parameters_for_combination(mock_project, mock_form_data, combo)
            print(f"  Success: {params['filename']}")
            print(f"  Nozzle reduction: {params['nozzle_reduction']}%")
            print(f"  Buffer width: {params['buffer_width']}m")
            print(f"  Runoff volume reduction: {params['runoff_volume_reduction']}")
            print(f"  Erosion mass reduction: {params['erosion_mass_reduction']}")
        except Exception as e:
            print(f"  Error: {e}")
        print()

def test_combination_generation():
    """Test the logic for generating all combinations."""
    
    print("Testing combination generation logic:")
    print("=" * 50)
    
    # Simulate selected parameters
    selected_nozzles = [0, 70, 90]
    selected_runoffs = ['10m', '20m']
    selected_buffers = [0, 10]
    
    print(f"Selected nozzles: {selected_nozzles}")
    print(f"Selected runoffs: {selected_runoffs}")
    print(f"Selected buffers: {selected_buffers}")
    print()
    
    # Generate all combinations
    combinations = []
    for nozzle in selected_nozzles:
        for runoff in selected_runoffs:
            for buffer in selected_buffers:
                combination = {
                    'nozzle': nozzle,
                    'runoff': runoff,
                    'buffer': buffer
                }
                combinations.append(combination)
    
    print(f"Total combinations generated: {len(combinations)}")
    print()
    
    # Show each combination
    for i, combo in enumerate(combinations, 1):
        param_string = generate_parameter_string_from_combination(combo)
        output_name = f"TEST_PROJECT{param_string}"
        print(f"{i:2d}. {output_name}")
        print(f"     Nozzle: {combo['nozzle']}% | Runoff: {combo['runoff']} | Buffer: {combo['buffer']}m")
    
    print()
    print(f"Expected output: {len(combinations)} separate project folders")

if __name__ == "__main__":
    print("Multi-Parameter Selection Test")
    print("=" * 50)
    print()
    
    test_parameter_combinations()
    test_combination_generation()
    
    print("Test completed!") 