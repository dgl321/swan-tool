import os
import zipfile
import tempfile
from typing import List, Dict
from datetime import datetime

class ZipUtil:
    """Utility for creating zip archives of generated files."""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def create_zip_archive(self, files: List[str], output_path: str, archive_name: str = None) -> str:
        """
        Create a zip archive containing the specified files.
        
        Args:
            files: List of file paths to include in the archive
            output_path: Directory where the zip file should be saved
            archive_name: Name for the zip file (optional)
            
        Returns:
            Path to the created zip file
        """
        if not files:
            raise ValueError("No files provided for zip archive")
            
        # Generate archive name if not provided
        if not archive_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"SWAN_Output_{timestamp}.zip"
            
        zip_path = os.path.join(output_path, archive_name)
        
        # Create the zip file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files:
                if os.path.exists(file_path):
                    # Add file to zip with just the filename (no path)
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)
                    
        return zip_path
    
    def create_project_zip(self, project_data: List[Dict], output_dir: str) -> str:
        """
        Create a zip archive for a complete project with all generated files.
        
        Args:
            project_data: List of dictionaries containing project data
            output_dir: Directory where the zip file should be saved
            
        Returns:
            Path to the created zip file
        """
        files_to_zip = []
        
        # Collect all generated files
        for project in project_data:
            # Add .tpf file
            tpf_path = project.get('tpf_file_path')
            if tpf_path and os.path.exists(tpf_path):
                files_to_zip.append(tpf_path)
                
            # Add individual .bat file if it exists
            bat_path = project.get('bat_file_path')
            if bat_path and os.path.exists(bat_path):
                files_to_zip.append(bat_path)
                
        # Add main TOXSWABAT.bat file if it exists
        main_bat_path = os.path.join(output_dir, "TOXSWABAT.bat")
        if os.path.exists(main_bat_path):
            files_to_zip.append(main_bat_path)
            
        # Create zip archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"SWAN_Project_{timestamp}.zip"
        
        return self.create_zip_archive(files_to_zip, output_dir, archive_name)
    
    def create_organized_zip(self, project_data: List[Dict], output_dir: str) -> str:
        """
        Create a zip archive with organized folder structure.
        
        Args:
            project_data: List of dictionaries containing project data
            output_dir: Directory where the zip file should be saved
            
        Returns:
            Path to the created zip file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = os.path.join(output_dir, f"SWAN_Organized_{timestamp}.zip")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add .tpf files to a TPF folder
            for project in project_data:
                tpf_path = project.get('tpf_file_path')
                if tpf_path and os.path.exists(tpf_path):
                    arcname = f"TPF/{os.path.basename(tpf_path)}"
                    zipf.write(tpf_path, arcname)
                    
            # Add .bat files to a BAT folder
            for project in project_data:
                bat_path = project.get('bat_file_path')
                if bat_path and os.path.exists(bat_path):
                    arcname = f"BAT/{os.path.basename(bat_path)}"
                    zipf.write(bat_path, arcname)
                    
            # Add main TOXSWABAT.bat to root
            main_bat_path = os.path.join(output_dir, "TOXSWABAT.bat")
            if os.path.exists(main_bat_path):
                zipf.write(main_bat_path, "TOXSWABAT.bat")
                
        return zip_path
    
    def cleanup_temp_files(self, files: List[str]):
        """
        Clean up temporary files.
        
        Args:
            files: List of file paths to delete
        """
        for file_path in files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")
                
    def create_combined_project_zip(self, project_outputs: List[Dict]) -> str:
        """
        Create a combined zip archive with all project outputs organized by project.
        
        Args:
            project_outputs: List of dictionaries containing project output information
            
        Returns:
            Path to the created zip file
        """
        # Create a temporary directory for the zip
        temp_dir = tempfile.mkdtemp()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = os.path.join(temp_dir, f"SWAN_Combined_Projects_{timestamp}.zip")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for project_output in project_outputs:
                project_name = project_output['project_name']
                output_dir = project_output['output_dir']
                
                # Add all files from the project output directory
                if os.path.exists(output_dir):
                    for root, dirs, files in os.walk(output_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Create archive path with project name as folder
                            rel_path = os.path.relpath(file_path, output_dir)
                            arcname = f"{project_name}/{rel_path}"
                            zipf.write(file_path, arcname)
                            
        return zip_path
    
    def get_file_info(self, file_path: str) -> Dict:
        """
        Get information about a file for display purposes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file information
        """
        if not os.path.exists(file_path):
            return {}
            
        stat = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'path': file_path
        } 