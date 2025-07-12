import os
import re
from typing import Dict, List, Optional
from datetime import datetime

class TPFGenerator:
    """Generator for SWAN .tpf parameter files based on templates."""
    
    def __init__(self, template_path: str = None):
        """
        Initialize the TPF generator.
        
        Args:
            template_path: Path to the template .tpf file
        """
        self.template_path = template_path
        self.template_content = None
        
    def load_template(self, template_path: str = None) -> str:
        """
        Load a .tpf template file.
        
        Args:
            template_path: Path to the template file (optional if set in __init__)
            
        Returns:
            Template content as string
        """
        if template_path:
            self.template_path = template_path
        elif not self.template_path:
            raise ValueError("No template path provided")
            
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
            
        with open(self.template_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.template_content = f.read()
            
        return self.template_content
    
    def generate_tpf(self, parameters: Dict, output_path: str) -> str:
        """
        Generate a .tpf file by replacing placeholders in the template.
        
        Args:
            parameters: Dictionary containing parameter values
            output_path: Path where the generated .tpf file should be saved
            
        Returns:
            Path to the generated .tpf file
        """
        if not self.template_content:
            raise ValueError("No template loaded. Call load_template() first.")
            
        # Create the content by replacing placeholders
        content = self.template_content
        
        # Check if this is a VFSMOD template
        use_vfsmod = parameters.get('use_vfsmod', False)
        
        # Replace standard placeholders
        replacements = {
            '<rCrop>': parameters.get('crop', 'Unknown'),
            '<rCompund>': parameters.get('substance_name', 'Unknown'),
            '<nApps>': str(parameters.get('num_applications', 1)),
            '<srcProjName>': parameters.get('source_project_name', 'Unknown'),
            '<srcProjPath>': parameters.get('source_project_path', 'Unknown'),
            '<outputProjPath>': parameters.get('output_project_path', 'Unknown'),
            '<SWANtpf>': parameters.get('parameter_filename', 'Unknown'),
            '<fName>': parameters.get('filename', 'Unknown'),
            '<VP>': str(parameters.get('vapour_pressure', '0.000000046')),
            '<MitCount>': str(parameters.get('mitigation_count', 8)),
            '<ROVolRed>': str(parameters.get('runoff_volume_reduction', 0.0)),
            '<ROFluxRed>': str(parameters.get('runoff_flux_reduction', 0.0)),
            '<ErosMassRed>': str(parameters.get('erosion_mass_reduction', 0.0)),
            '<ErosFluxRed>': str(parameters.get('erosion_flux_reduction', 0.0)),
            '<NozRed>': str(parameters.get('nozzle_reduction', 0)),
            '<Step3>': 'Yes' if parameters.get('use_step3_mass_loadings', False) else 'No',
            '<SelBuf>': 'Yes' if parameters.get('select_buffer_width', False) else 'No',
            '<BuffWid>': str(parameters.get('buffer_width', 0))
        }
        
        # Apply replacements
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
            
        # Handle mitigation matrix
        mit_matrix = self._generate_mitigation_matrix(parameters)
        content = content.replace('<MitMatrix>', mit_matrix)
        
        # Handle VFSMOD vs standard runoff section
        if use_vfsmod:
            # Replace the entire runoff section with VFSMOD format
            vfsmod_width = parameters.get('vfsmod_width', 0)
            vfsmod_section = f"""*-----------------------------------------------------------------
* Run-off mitigation parameters
*-----------------------------------------------------------------
*
Reduction run-off mode:                 VfsMod
Filter strip buffer width:             {vfsmod_width}
*
*-----------------------------------------------------------------"""
            
            # Find and replace the runoff section
            content = self._replace_runoff_section(content, vfsmod_section)
        else:
            # Use standard runoff format (already handled by placeholders)
            pass
        
        # Write the generated content to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return output_path
    
    def _generate_mitigation_matrix(self, parameters: Dict) -> str:
        """Generate the mitigation matrix section for the .tpf file."""
        scenarios = parameters.get('scenarios', [])
        
        if not scenarios:
            # Default scenarios based on the template
            scenarios = [
                {'scenario': 'D1', 'water_body': 'Ditch', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
                {'scenario': 'D1', 'water_body': 'Stream', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
                {'scenario': 'D3', 'water_body': 'Ditch', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
                {'scenario': 'D4', 'water_body': 'Pond', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
                {'scenario': 'D4', 'water_body': 'Stream', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
                {'scenario': 'D5', 'water_body': 'Pond', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
                {'scenario': 'D5', 'water_body': 'Stream', 'runoff': 'No', 'spray_drift': 'Yes', 'dry_deposition': 'No'},
                {'scenario': 'R4', 'water_body': 'Stream', 'runoff': 'Yes', 'spray_drift': 'Yes', 'dry_deposition': 'No'}
            ]
        
        matrix_lines = []
        for scenario in scenarios:
            line = f"{scenario['scenario']:<8} {scenario['water_body']:<10} {scenario['runoff']:<4}  {scenario['spray_drift']:<4}  {scenario['dry_deposition']:<4}"
            matrix_lines.append(line)
            
        return '\n'.join(matrix_lines)
    
    def _replace_runoff_section(self, content: str, new_section: str) -> str:
        """Replace the runoff mitigation section in the template."""
        # Pattern to match the runoff section
        pattern = r'\*-----------------------------------------------------------------\s*\*\s*Run-off mitigation parameters\s*\*-----------------------------------------------------------------\s*\*.*?\*-----------------------------------------------------------------'
        
        # Use re.DOTALL to match across multiple lines
        if re.search(pattern, content, re.DOTALL):
            return re.sub(pattern, new_section, content, flags=re.DOTALL)
        else:
            # If pattern not found, try a more flexible approach
            # Look for the section between the runoff header and the next section
            pattern2 = r'(\*-----------------------------------------------------------------\s*\*\s*Run-off mitigation parameters\s*\*-----------------------------------------------------------------\s*\*.*?)(\*-----------------------------------------------------------------\s*\*\s*Spray drift mitigation parameters)'
            
            if re.search(pattern2, content, re.DOTALL):
                return re.sub(pattern2, new_section + r'\2', content, flags=re.DOTALL)
            else:
                # If still not found, just return original content
                print("Warning: Could not find runoff section to replace")
                return content
    
    def generate_multiple_tpf_files(self, project_data: List[Dict], output_dir: str) -> List[str]:
        """
        Generate multiple .tpf files for a list of projects.
        
        Args:
            project_data: List of dictionaries containing project data
            output_dir: Directory where .tpf files should be saved
            
        Returns:
            List of paths to generated .tpf files
        """
        generated_files = []
        
        for project in project_data:
            try:
                # Generate filename based on project name
                project_name = project.get('project_name', 'unknown')
                filename = f"{project_name}.tpf"
                output_path = os.path.join(output_dir, filename)
                
                # Generate the .tpf file
                generated_path = self.generate_tpf(project, output_path)
                generated_files.append(generated_path)
                
            except Exception as e:
                print(f"Error generating TPF for project {project.get('project_name', 'unknown')}: {e}")
                
        return generated_files 