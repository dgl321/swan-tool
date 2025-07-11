#!/usr/bin/env python3
"""
Test script to verify template replacement is working correctly.
"""

import os
import sys
sys.path.append('.')

from generators.tpf_generator import TPFGenerator

def test_template_replacement():
    """Test that the template replacement works correctly."""
    
    # Initialize the TPF generator
    tpf_generator = TPFGenerator()
    
    # Load the template
    template_path = 'BIXSC45_1AP_10mS_10m_VFS.tpf'
    tpf_generator.load_template(template_path)
    
    # Test parameters (simulating LLGL625 project data)
    test_parameters = {
        'crop': 'Legumes',
        'substance_name': 'LAMBDA',
        'num_applications': 1,
        'source_project_name': 'LLGL625',
        'source_project_path': '/path/to/LLGL625',
        'output_project_path': 'C:\\SwashProjects\\LLGL625_Output',
        'parameter_filename': 'LLGL625.tpf',
        'filename': 'LLGL625.tpf',
        'vapour_pressure': 2.00e-07,
        'mitigation_count': 11,
        'runoff_volume_reduction': 0.6,
        'runoff_flux_reduction': 0.6,
        'erosion_mass_reduction': 0.85,
        'erosion_flux_reduction': 0.85,
        'nozzle_reduction': 0,
        'use_step3_mass_loadings': False,
        'select_buffer_width': True,
        'buffer_width': 20,
        'scenarios': [
            {'scenario': 'D1', 'water_body': 'Ditch', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
            {'scenario': 'D1', 'water_body': 'Stream', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
            {'scenario': 'D3', 'water_body': 'Ditch', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
            {'scenario': 'D4', 'water_body': 'Pond', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
            {'scenario': 'D4', 'water_body': 'Stream', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
            {'scenario': 'D5', 'water_body': 'Pond', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
            {'scenario': 'D5', 'water_body': 'Stream', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
            {'scenario': 'R4', 'water_body': 'Stream', 'runoff': 'Yes', 'spray_drift': 'Yes', 'dry_deposition': 'No'}
        ]
    }
    
    # Generate the TPF file
    output_path = './test_output.tpf'
    generated_path = tpf_generator.generate_tpf(test_parameters, output_path)
    
    print(f"Generated TPF file: {generated_path}")
    
    # Read and display the generated content
    with open(generated_path, 'r') as f:
        content = f.read()
    
    print("\n=== Generated TPF Content ===")
    print(content)
    
    # Check if key replacements worked
    checks = [
        ('Crop:         Legumes', 'Crop replacement'),
        ('Substance:    LAMBDA', 'Substance replacement'),
        ('Source project name: LLGL625', 'Project name replacement'),
        ('Vapour pressure (Pa):    2e-07', 'Vapour pressure replacement'),
        ('Mitigation count:        11', 'Mitigation count replacement'),
        ('Fractional reduction in run-off volume: 0.6', 'Runoff volume replacement'),
        ('Fractional reduction in run-off flux:   0.6', 'Runoff flux replacement'),
        ('Fractional reduction in erosion mass:   0.85', 'Erosion mass replacement'),
        ('Fractional reduction in erosion flux:   0.85', 'Erosion flux replacement'),
    ]
    
    print("\n=== Replacement Checks ===")
    for check_text, description in checks:
        if check_text in content:
            print(f"✅ {description}: {check_text}")
        else:
            print(f"❌ {description}: {check_text}")
    
    # Clean up
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"\nCleaned up test file: {output_path}")

if __name__ == "__main__":
    test_template_replacement() 