import re
import os
from typing import Dict, List, Optional

class ReportParser:
    """Parser for TOXSWA report files to extract PEC values and other metadata."""
    
    def __init__(self):
        self.pec_values = {}
        self.vdf_corrections = {}
        self.application_details = []
        
    def parse_report_file(self, file_path: str) -> Dict:
        """
        Parse a _report.txt file and extract relevant metadata.
        
        Args:
            file_path: Path to the report file
            
        Returns:
            Dictionary containing extracted metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Report file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        return self._extract_metadata(content)
    
    def _extract_metadata(self, content: str) -> Dict:
        """Extract metadata from report file content."""
        metadata = {
            'substance_name': None,
            'crop': None,
            'description': None,
            'runs': [],
            'pec_values': {},
            'application_details': []
        }
        
        # Extract substance name
        substance_match = re.search(r'\* Substance\s+:\s+(\w+)', content)
        if substance_match:
            metadata['substance_name'] = substance_match.group(1)
            
        # Extract description
        desc_match = re.search(r'\* Description\s+:\s+(.+)', content)
        if desc_match:
            metadata['description'] = desc_match.group(1).strip()
            
        # Extract run information from the table
        # Look for lines that start with * followed by a number and contain crop information
        # This pattern is more robust and avoids picking up numerical data
        
        # Pattern to match: "* 4630  Cereals, spring(1st)     D1_Ditch"
        # or similar variations
        run_pattern = r'\*\s+(\d+)\s+([A-Za-z,\s]+)\([^)]+\)\s+(\w+[_\w]*)'
        run_matches = re.findall(run_pattern, content)
        
        crops_found = set()
        for match in run_matches:
            run_id, crop, scenario = match
            crop_clean = crop.strip()
            
            # Only add if it looks like a real crop name (contains letters, not just numbers)
            if any(c.isalpha() for c in crop_clean):
                crops_found.add(crop_clean)
                
                # Parse scenario code (e.g., D1_Ditch -> D1, Ditch)
                scenario_parts = scenario.split('_')
                scenario_code = scenario_parts[0] if scenario_parts else scenario
                water_body = scenario_parts[1] if len(scenario_parts) > 1 else None
                
                run_info = {
                    'run_id': run_id.strip(),
                    'crop': crop_clean,
                    'scenario': scenario_code,
                    'water_body': water_body
                }
                metadata['runs'].append(run_info)
        
        # Set the crop to the first one found (or join if multiple)
        if crops_found:
            metadata['crop'] = list(crops_found)[0]  # Take the first crop found
            
        # Extract PEC values (these might be in a different section)
        # Look for PEC-related information
        pec_pattern = r'PEC\s*=\s*([\d.]+)'
        pec_matches = re.findall(pec_pattern, content, re.IGNORECASE)
        if pec_matches:
            metadata['pec_values'] = {
                'values': [float(x) for x in pec_matches]
            }
            
        return metadata
    
    def parse_multiple_report_files(self, folder_path: str) -> List[Dict]:
        """
        Parse all _report.txt files in a folder and return metadata for each.
        
        Args:
            folder_path: Path to folder containing report files
            
        Returns:
            List of dictionaries containing metadata for each report file
        """
        results = []
        
        if not os.path.exists(folder_path):
            return results
            
        for filename in os.listdir(folder_path):
            if filename.endswith('_report.txt'):
                file_path = os.path.join(folder_path, filename)
                try:
                    metadata = self.parse_report_file(file_path)
                    metadata['filename'] = filename
                    metadata['file_path'] = file_path
                    results.append(metadata)
                except Exception as e:
                    print(f"Error parsing {filename}: {e}")
                    
        return results
    
    def extract_application_details(self, content: str) -> List[Dict]:
        """Extract detailed application information from report content."""
        details = []
        
        # Look for application timing information
        app_pattern = r'(\d+-\w+)/(\d+-\w+)/(\d+)'
        app_matches = re.findall(app_pattern, content)
        
        for match in app_matches:
            start_date, end_date, interval = match
            details.append({
                'start_date': start_date,
                'end_date': end_date,
                'interval': int(interval)
            })
            
        return details 