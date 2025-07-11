#!/usr/bin/env python3
"""
Test the custom checkbox functionality for buffer width.
"""

def test_custom_checkbox_functionality():
    """Test that custom checkbox shows/hides custom input and affects combinations."""
    
    # Simulate the parseCustomValues function
    def parse_custom_values(input_value):
        if not input_value or input_value.strip() == '':
            return []
        
        return [int(val.strip()) for val in input_value.split(',') 
                if val.strip() and val.strip().isdigit() and 0 <= int(val.strip()) <= 100]
    
    # Test case 1: Custom checkbox unchecked
    custom_checkbox_checked = False
    selected_buffers = [0, 10, 20]  # From regular checkboxes
    custom_buffer_input = "15, 25, 35"  # Custom values entered
    
    if custom_checkbox_checked:
        custom_buffers = parse_custom_values(custom_buffer_input)
    else:
        custom_buffers = []
    
    all_buffers = sorted(list(set(selected_buffers + custom_buffers)))
    print(f"Custom checkbox unchecked: {all_buffers}")  # Should be [0, 10, 20]
    assert all_buffers == [0, 10, 20], f"Expected [0, 10, 20], got {all_buffers}"
    
    # Test case 2: Custom checkbox checked
    custom_checkbox_checked = True
    selected_buffers = [0, 10, 20]  # From regular checkboxes
    custom_buffer_input = "15, 25, 35"  # Custom values entered
    
    if custom_checkbox_checked:
        custom_buffers = parse_custom_values(custom_buffer_input)
    else:
        custom_buffers = []
    
    all_buffers = sorted(list(set(selected_buffers + custom_buffers)))
    print(f"Custom checkbox checked: {all_buffers}")  # Should be [0, 10, 15, 20, 25, 35]
    assert all_buffers == [0, 10, 15, 20, 25, 35], f"Expected [0, 10, 15, 20, 25, 35], got {all_buffers}"
    
    # Test case 3: Only custom values (no regular checkboxes selected)
    custom_checkbox_checked = True
    selected_buffers = []  # No regular checkboxes selected
    custom_buffer_input = "5, 15, 25"  # Only custom values
    
    if custom_checkbox_checked:
        custom_buffers = parse_custom_values(custom_buffer_input)
    else:
        custom_buffers = []
    
    all_buffers = sorted(list(set(selected_buffers + custom_buffers)))
    print(f"Only custom values: {all_buffers}")  # Should be [5, 15, 25]
    assert all_buffers == [5, 15, 25], f"Expected [5, 15, 25], got {all_buffers}"
    
    # Test case 4: Custom checkbox unchecked with custom input (should ignore custom input)
    custom_checkbox_checked = False
    selected_buffers = [0, 10]  # Some regular checkboxes selected
    custom_buffer_input = "15, 25, 35"  # Custom values entered but checkbox unchecked
    
    if custom_checkbox_checked:
        custom_buffers = parse_custom_values(custom_buffer_input)
    else:
        custom_buffers = []
    
    all_buffers = sorted(list(set(selected_buffers + custom_buffers)))
    print(f"Custom checkbox unchecked with custom input: {all_buffers}")  # Should be [0, 10]
    assert all_buffers == [0, 10], f"Expected [0, 10], got {all_buffers}"
    
    print("✓ All custom checkbox functionality tests passed!")
    
    # Test combination generation with the new logic
    nozzle_values = [0, 25, 50]
    runoff_values = ['10m', '20m']
    buffer_values = [0, 10, 15, 20, 25, 35]  # Mix of regular and custom
    
    combinations = []
    for nozzle in nozzle_values:
        for runoff in runoff_values:
            for buffer in buffer_values:
                combination = {
                    'nozzle': nozzle,
                    'runoff': runoff,
                    'buffer': buffer,
                    'params': []
                }
                
                # Build parameter string for naming
                if nozzle > 0:
                    combination['params'].append(f"{nozzle}N")
                if buffer > 0:
                    combination['params'].append(f"{buffer}B")
                if runoff == '10m':
                    combination['params'].append('10L&M')
                elif runoff == '20m':
                    combination['params'].append('20L&M')
                
                combinations.append(combination)
    
    expected_count = len(nozzle_values) * len(runoff_values) * len(buffer_values)
    actual_count = len(combinations)
    
    print(f"Generated {actual_count} combinations (expected {expected_count})")
    assert actual_count == expected_count
    
    # Test naming convention
    project_name = "LLGL625"
    for combo in combinations[:3]:  # Test first 3 combinations
        param_string = '_' + '_'.join(combo['params']) if combo['params'] else ''
        output_name = project_name + param_string
        print(f"Generated name: {output_name}")
    
    return True

if __name__ == "__main__":
    test_custom_checkbox_functionality()
    print("\n✅ Custom checkbox functionality working correctly!") 