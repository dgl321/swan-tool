import re
import os
from typing import Dict, List, Optional

class TXWParser:
    """Parser for TOXSWA .txw files to extract metadata."""
    
    def __init__(self):
        self.substance_name = None
        self.crop = None
        self.application_dates = []
        self.application_rate = None
        self.scenario = None
        self.water_body = None
        
    def parse_txw_file(self, file_path: str) -> Dict:
        """
        Parse a .txw file and extract relevant metadata.
        
        Args:
            file_path: Path to the .txw file
            
        Returns:
            Dictionary containing extracted metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"TXW file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        return self._extract_metadata(content)
    
    def _extract_metadata(self, content: str) -> Dict:
        """Extract metadata from TXW file content."""
        metadata = {
            'substance_name': None,
            'crop': None,
            'application_dates': [],
            'application_rate': None,
            'scenario': None,
            'water_body': None,
            'scenario_code': None,
            'vapour_pressure': None
        }
        
        # Extract substance name
        substance_match = re.search(r'(\w+)\s+SubstanceName', content)
        if substance_match:
            metadata['substance_name'] = substance_match.group(1)
            
        # Extract vapour pressure from the volatilization section
        # Look for the pattern: "4.6E-8      PreVapRef_BIXAFEN_SW (Pa)"
        vapour_pressure_match = re.search(r'([0-9.]+E?[+-]?\d*)\s+PreVapRef_\w+\s+\(Pa\)', content)
        if vapour_pressure_match:
            try:
                vapour_pressure = float(vapour_pressure_match.group(1))
                metadata['vapour_pressure'] = vapour_pressure
            except ValueError:
                print(f"Could not parse vapour pressure value: {vapour_pressure_match.group(1)}")
            
        # Extract crop information (this might be in the report file instead)
        # Look for crop-related information in comments or headers
        
        # Extract scenario information
        scenario_match = re.search(r'(\w+)\s+Location', content)
        if scenario_match:
            scenario = scenario_match.group(1)
            metadata['scenario'] = scenario
            
            # Parse scenario code (e.g., D1_Ditch -> D1, Ditch)
            if '_' in scenario:
                parts = scenario.split('_')
                metadata['scenario_code'] = parts[0]
                metadata['water_body'] = parts[1] if len(parts) > 1 else None
                
        # Extract application scheme
        app_scheme_match = re.search(r'(\w+)\s+ApplicationScheme', content)
        if app_scheme_match:
            metadata['application_scheme'] = app_scheme_match.group(1)
            
        return metadata
    
    def parse_multiple_txw_files(self, folder_path: str) -> List[Dict]:
        """
        Parse all .txw files in a folder and return metadata for each.
        
        Args:
            folder_path: Path to folder containing .txw files
            
        Returns:
            List of dictionaries containing metadata for each .txw file
        """
        results = []
        
        if not os.path.exists(folder_path):
            return results
            
        for filename in os.listdir(folder_path):
            if filename.endswith('.txw'):
                file_path = os.path.join(folder_path, filename)
                try:
                    metadata = self.parse_txw_file(file_path)
                    metadata['filename'] = filename
                    metadata['file_path'] = file_path
                    results.append(metadata)
                except Exception as e:
                    print(f"Error parsing {filename}: {e}")
                    
        return results 