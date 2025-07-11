import os
import tempfile
import zipfile
import shutil
from flask import render_template, request, redirect, url_for, flash, send_file, jsonify, session
from werkzeug.utils import secure_filename
from datetime import datetime

from app import app, allowed_file
from parsers.txw_parser import TXWParser
from parsers.report_parser import ReportParser
from generators.tpf_generator import TPFGenerator
from generators.bat_generator import BATGenerator
from utils.zip_util import ZipUtil

# Initialize parsers and generators
txw_parser = TXWParser()
report_parser = ReportParser()
tpf_generator = TPFGenerator()
bat_generator = BATGenerator()
zip_util = ZipUtil()

@app.route('/')
def index():
    """Main page with file upload form."""
    return render_template('index.html')

@app.route('/process-paths', methods=['POST'])
def process_paths():
    """Handle project path processing."""
    project_paths_text = request.form.get('project_paths', '').strip()
    
    if not project_paths_text:
        flash('No project paths provided', 'error')
        return redirect(url_for('index'))
    
    # Split paths by lines and clean them, handling spaces and special characters
    project_paths = []
    for line in project_paths_text.split('\n'):
        path = line.strip()
        if path:
            # Handle quoted paths and spaces
            if (path.startswith('"') and path.endswith('"')) or (path.startswith("'") and path.endswith("'")):
                path = path[1:-1]  # Remove quotes
            project_paths.append(path)
    
    # Debug: Print the paths we're processing
    print(f"Processing {len(project_paths)} paths:")
    for i, path in enumerate(project_paths):
        print(f"  {i+1}: '{path}' (exists: {os.path.exists(path)})")
    
    if not project_paths:
        flash('No valid project paths found', 'error')
        return redirect(url_for('index'))
    
    # Create temporary directory for processing
    temp_dir = tempfile.mkdtemp()
    processed_projects = []
    
    try:
        for project_path in project_paths:
            # Validate and normalize the path
            if os.path.exists(project_path):
                # Process the project folder directly
                project_data = process_single_project(project_path, temp_dir)
                if project_data:
                    processed_projects.extend(project_data)
                else:
                    flash(f'No valid TOXSWA data found in: {project_path}', 'warning')
            else:
                flash(f'Project path not found: {project_path}', 'warning')
                # Try to provide helpful debugging info
                parent_dir = os.path.dirname(project_path)
                if os.path.exists(parent_dir):
                    flash(f'Parent directory exists: {parent_dir}', 'info')
                    try:
                        contents = os.listdir(parent_dir)
                        flash(f'Contents of parent directory: {contents[:5]}', 'info')
                    except Exception as e:
                        flash(f'Cannot read parent directory: {e}', 'warning')
                
        if not processed_projects:
            flash('No valid TOXSWA projects found in the provided paths', 'error')
            return redirect(url_for('index'))
            
        # Store processed projects in session
        session['processed_projects'] = processed_projects
        session['temp_dir'] = temp_dir
        
        flash(f'Successfully processed {len(processed_projects)} projects from {len(project_paths)} paths', 'success')
        return redirect(url_for('configure'))
        
    except Exception as e:
        flash(f'Error processing project paths: {str(e)}', 'error')
        return redirect(url_for('index'))

def validate_project_path(project_path: str) -> bool:
    """Validate that a project path contains the required TOXSWA structure."""
    if not os.path.exists(project_path):
        print(f"Path does not exist: {project_path}")
        return False
        
    # Check for TOXSWA subfolder
    toxswa_path = os.path.join(project_path, 'TOXSWA')
    if not os.path.exists(toxswa_path):
        print(f"TOXSWA subfolder not found: {toxswa_path}")
        return False
        
    # Check for at least one .txw file
    try:
        txw_files = [f for f in os.listdir(toxswa_path) if f.endswith('.txw')]
        if not txw_files:
            print(f"No .txw files found in: {toxswa_path}")
            return False
        print(f"Found {len(txw_files)} .txw files in: {toxswa_path}")
    except Exception as e:
        print(f"Error reading TOXSWA directory: {e}")
        return False
        
    return True

def process_single_project(project_path: str, temp_dir: str) -> list:
    """Process a single TOXSWA project folder."""
    projects = []
    
    # Validate the project path
    if not validate_project_path(project_path):
        return projects
    
    # Look for TOXSWA subfolder
    toxswa_path = os.path.join(project_path, 'TOXSWA')
    
    # Parse .txw files
    txw_data = txw_parser.parse_multiple_txw_files(toxswa_path)
    
    # Parse report files
    report_data = report_parser.parse_multiple_report_files(project_path)
    
    # Group TXW files by project name
    project_name = os.path.basename(project_path)
    
    # Find matching report data (use the first one since they should be the same for the project)
    report_info = report_data[0] if report_data else None
    
    # Create consolidated project data
    project_data = {
        'project_name': project_name,
        'project_path': project_path,
        'txw_files': txw_data,  # All TXW files for this project
        'report_data': report_info,
        'substance_name': txw_data[0].get('substance_name') if txw_data else 'Unknown',
        'crop': report_info.get('crop') if report_info else 'Unknown',
        'num_applications': 1,  # Default value
        'scenarios': extract_scenarios(txw_data),
        'vapour_pressure': txw_data[0].get('vapour_pressure') if txw_data else None,  # Use first TXW file's vapour pressure
        'total_txw_files': len(txw_data)
    }
    
    projects.append(project_data)
        
    return projects

def copy_project_files(source_dir: str, dest_dir: str) -> bool:
    """
    Copy all files and folders from the source project directory to the destination directory.
    
    Args:
        source_dir: Path to the original project directory
        dest_dir: Path to the destination directory
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create destination directory if it doesn't exist
        os.makedirs(dest_dir, exist_ok=True)
        
        # Copy all files and folders from source to destination
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            dest_item = os.path.join(dest_dir, item)
            
            if os.path.isdir(source_item):
                # Copy directory recursively
                shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
            else:
                # Copy file
                shutil.copy2(source_item, dest_item)
                
        return True
    except Exception as e:
        print(f"Error copying project files: {e}")
        return False

def extract_scenarios(txw_data: list) -> list:
    """Extract scenario information from TXW data."""
    scenarios = []
    
    for txw_info in txw_data:
        scenario_code = txw_info.get('scenario_code')
        water_body = txw_info.get('water_body')
        
        if scenario_code and water_body:
            scenario = {
                'scenario': scenario_code,
                'water_body': water_body,
                'runoff': 'Yes' if scenario_code.startswith('R') else 'No',
                'spray_drift': 'Yes',
                'dry_deposition': 'No'
            }
            scenarios.append(scenario)
            
    return scenarios

@app.route('/configure')
def configure():
    """Configuration page for SWAN parameters."""
    if 'processed_projects' not in session:
        flash('No projects to configure. Please upload files first.', 'error')
        return redirect(url_for('index'))
        
    projects = session['processed_projects']
    return render_template('configure.html', projects=projects)

@app.route('/generate', methods=['POST'])
def generate_files():
    """Generate .tpf and .bat files based on configuration."""
    if 'processed_projects' not in session:
        flash('No projects to process. Please upload files first.', 'error')
        return redirect(url_for('index'))
        
    projects = session['processed_projects']
    
    # Get form data
    form_data = request.form.to_dict()
    
    # Load template
    template_path = form_data.get('template_path', 'BIXSC45_1AP_10mS_10m_VFS.tpf')
    if not os.path.exists(template_path):
        template_path = os.path.join('test_data', 'BIXSC45_1AP_10mS_10m_VFS', 'BIXSC45_1AP_10mS_10m_VFS.tpf')
        
    tpf_generator.load_template(template_path)
    
    generated_files = []
    project_outputs = []
    
    try:
        # Generate files for each project in its own directory
        for project in projects:
            project_path = project['project_path']
            project_name = project['project_name']
            
            # Create output directory in the same location as the original project
            project_output_dir = os.path.join(os.path.dirname(project_path), f"{project_name}_SWAN_Output")
            os.makedirs(project_output_dir, exist_ok=True)
            
            # Copy all files from the original project to the output directory
            print(f"Copying project files from {project_path} to {project_output_dir}")
            if not copy_project_files(project_path, project_output_dir):
                flash(f'Warning: Could not copy all files from {project_name}', 'warning')
            
            # Prepare parameters for TPF generation
            parameters = prepare_tpf_parameters(project, form_data)
            
            # Generate TPF file
            tpf_filename = f"{project_name}.tpf"
            tpf_path = os.path.join(project_output_dir, tpf_filename)
            
            generated_tpf = tpf_generator.generate_tpf(parameters, tpf_path)
            project['tpf_file_path'] = generated_tpf
            generated_files.append(generated_tpf)
            
            # Generate .bat file for this project
            bat_path = os.path.join(project_output_dir, "TOXSWABAT.bat")
            generated_bat = bat_generator.generate_bat_from_project_data([project], project_output_dir)
            generated_files.append(generated_bat)
            
            # Store project output info
            project_outputs.append({
                'project_name': project_name,
                'output_dir': project_output_dir,
                'tpf_file': generated_tpf,
                'bat_file': generated_bat
            })
        
        # Create a combined zip archive with all projects
        combined_zip_path = zip_util.create_combined_project_zip(project_outputs)
        generated_files.append(combined_zip_path)
        
        # Store generated files and project outputs in session
        session['generated_files'] = generated_files
        session['project_outputs'] = project_outputs
        session['combined_zip_path'] = combined_zip_path
        
        flash(f'Files generated successfully for {len(projects)} projects!', 'success')
        return redirect(url_for('download'))
        
    except Exception as e:
        flash(f'Error generating files: {str(e)}', 'error')
        return redirect(url_for('configure'))

def prepare_tpf_parameters(project: dict, form_data: dict) -> dict:
    """Prepare parameters for TPF generation."""
    # Get scenarios and automatically set mitigation count
    scenarios = project.get('scenarios', [])
    mitigation_count = len(scenarios) if scenarios else 1
    
    # Get vapour pressure from project data (extracted from TXW) or form data
    extracted_vp = project.get('vapour_pressure')
    if extracted_vp is not None:
        vapour_pressure = float(extracted_vp)
        print(f"Using extracted vapour pressure: {vapour_pressure} Pa")
    else:
        vapour_pressure = float(form_data.get('vapour_pressure', 0.000000046))
        print(f"Using form vapour pressure: {vapour_pressure}")
    
    # Handle mitigation scenario selection
    mitigation_scenario = form_data.get('mitigation_scenario', '')
    if mitigation_scenario == '10m':
        # 10m VFS Buffer: Volume 0.6, Erosion 0.85
        runoff_volume_reduction = 0.6
        runoff_flux_reduction = 0.6
        erosion_mass_reduction = 0.85
        erosion_flux_reduction = 0.85
    elif mitigation_scenario == '20m':
        # 20m VFS Buffer: Volume 0.8, Erosion 0.95
        runoff_volume_reduction = 0.8
        runoff_flux_reduction = 0.8
        erosion_mass_reduction = 0.95
        erosion_flux_reduction = 0.95
    else:
        # Use form values if no scenario selected (fallback)
        runoff_volume_reduction = float(form_data.get('runoff_volume_reduction', 0.0))
        runoff_flux_reduction = float(form_data.get('runoff_flux_reduction', 0.0))
        erosion_mass_reduction = float(form_data.get('erosion_mass_reduction', 0.0))
        erosion_flux_reduction = float(form_data.get('erosion_flux_reduction', 0.0))
    
    parameters = {
        'crop': project.get('crop', 'Unknown'),
        'substance_name': project.get('substance_name', 'Unknown'),
        'num_applications': int(form_data.get('num_applications', 1)),
        'source_project_name': project.get('project_name', 'Unknown'),
        'source_project_path': project.get('project_path', 'Unknown'),
        'output_project_path': form_data.get('output_project_path', 'C:\\SwashProjects\\Output'),
        'parameter_filename': f"{project['project_name']}.tpf",
        'filename': f"{project['project_name']}.tpf",
        'vapour_pressure': vapour_pressure,  # Use extracted or form value
        'mitigation_count': mitigation_count,  # Automatically set based on scenarios
        'runoff_volume_reduction': runoff_volume_reduction,
        'runoff_flux_reduction': runoff_flux_reduction,
        'erosion_mass_reduction': erosion_mass_reduction,
        'erosion_flux_reduction': erosion_flux_reduction,
        'nozzle_reduction': int(form_data.get('nozzle_reduction', 0)),
        'use_step3_mass_loadings': form_data.get('use_step3_mass_loadings') == 'on',
        'select_buffer_width': form_data.get('select_buffer_width') == 'on',
        'buffer_width': int(form_data.get('buffer_width', 0)),
        'scenarios': scenarios
    }
    
    return parameters

@app.route('/download')
def download():
    """Download page for generated files."""
    if 'project_outputs' not in session:
        flash('No files to download. Please generate files first.', 'error')
        return redirect(url_for('index'))
        
    project_outputs = session['project_outputs']
    combined_zip_path = session.get('combined_zip_path')
    
    # Get info for the combined zip file
    zip_info = None
    if combined_zip_path and os.path.exists(combined_zip_path):
        zip_info = zip_util.get_file_info(combined_zip_path)
    
    # Count projects
    project_count = len(project_outputs)
            
    return render_template('download.html', 
                         project_outputs=project_outputs, 
                         zip_info=zip_info, 
                         project_count=project_count)

@app.route('/download/<filename>')
def download_file(filename):
    """Download a specific generated file."""
    if 'combined_zip_path' not in session:
        flash('No files available for download.', 'error')
        return redirect(url_for('index'))
        
    combined_zip_path = session['combined_zip_path']
    
    if os.path.exists(combined_zip_path):
        return send_file(combined_zip_path, as_attachment=True)
    else:
        flash('File not found.', 'error')
        return redirect(url_for('download'))

@app.route('/api/project-info')
def api_project_info():
    """API endpoint to get project information."""
    if 'processed_projects' not in session:
        return jsonify({'error': 'No projects available'}), 404
        
    projects = session['processed_projects']
    return jsonify({'projects': projects})

@app.route('/test-path/<path:test_path>')
def test_path(test_path):
    """Test endpoint to check if a path exists and has TOXSWA structure."""
    import os
    result = {
        'path': test_path,
        'exists': os.path.exists(test_path),
        'is_dir': os.path.isdir(test_path) if os.path.exists(test_path) else False,
        'toxswa_exists': False,
        'txw_files': []
    }
    
    if result['exists'] and result['is_dir']:
        toxswa_path = os.path.join(test_path, 'TOXSWA')
        result['toxswa_exists'] = os.path.exists(toxswa_path)
        
        if result['toxswa_exists']:
            try:
                txw_files = [f for f in os.listdir(toxswa_path) if f.endswith('.txw')]
                result['txw_files'] = txw_files
            except Exception as e:
                result['error'] = str(e)
    
    return jsonify(result) 