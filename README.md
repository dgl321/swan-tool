# SWAN Parameter Generator

A Flask web application that replaces the Excel macro-based SWAN parameter generator tool used for TOXSWA Step 3 surface water assessments. This tool automates the conversion from TOXSWA Step 3 projects to SWAN Step 4 parameter files.

## Features

- **Multi-Project Processing**: Upload multiple TOXSWA Step 3 project folders at once
- **Automatic Metadata Extraction**: Parses `.txw` and `_report.txt` files to extract substance, crop, and application information
- **Dynamic TPF Generation**: Creates SWAN `.tpf` parameter files using real templates with placeholder replacement
- **Batch Processing**: Generates `TOXSWABAT.bat` files for automated TOXSWA execution
- **ZIP Packaging**: Packages all generated files into downloadable archives
- **Modern Web Interface**: Clean, responsive UI built with Bootstrap

## Project Structure

```
swan-tool/
├── app.py                 # Main Flask application
├── routes.py              # Flask routes and request handling
├── parsers/               # File parsing modules
│   ├── txw_parser.py      # TOXSWA .txw file parser
│   └── report_parser.py   # Report file parser
├── generators/            # File generation modules
│   ├── tpf_generator.py   # SWAN .tpf file generator
│   └── bat_generator.py   # Batch file generator
├── utils/                 # Utility modules
│   └── zip_util.py        # ZIP archive creation
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Upload page
│   ├── configure.html     # Configuration page
│   └── download.html      # Download page
├── static/                # Static assets (CSS, JS)
├── uploads/               # Upload directory
├── temp/                  # Temporary files
└── test_data/            # Sample data for testing
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd swan-tool
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the web interface**:
   Open your browser and navigate to `http://localhost:8080`

## Usage

### 1. Process TOXSWA Projects

- Navigate to the home page
- Enter the full file system paths to your TOXSWA Step 3 project folders
- Each folder should contain:
  - A `TOXSWA/` subfolder with `.txw` files
  - `_report.txt` files in the project root
- Enter one path per line in the text area

### 2. Configure SWAN Parameters

After uploading, you'll be taken to the configuration page where you can set:

- **Project Information**: Number of applications, output paths
- **Substance Properties**: Vapour pressure, mitigation count
- **Run-off Mitigation**: Volume/flux reduction parameters
- **Spray Drift Mitigation**: Nozzle reduction, buffer widths
- **Advanced Options**: Step 3 mass loadings, buffer selection

### 3. Generate Files

Click "Generate SWAN Files" to create:

- Complete copies of each original project folder with all files
- Individual `.tpf` parameter files for each project (added to the copied folders)
- A `TOXSWABAT.bat` file for each project for batch processing
- A combined ZIP archive containing all projects organized by folder

### 4. Download Results

Download the combined ZIP package containing all projects from the download page. Each project is organized in its own folder within the ZIP archive.

## File Formats

### Input Files

- **`.txw` files**: TOXSWA input files containing substance and scenario information
- **`_report.txt` files**: SWASH report files with PEC values and application details
- **Project folders**: Complete TOXSWA Step 3 project structures accessed via file system paths

### Output Files

- **`.tpf` files**: SWAN parameter files with placeholders replaced (one per project)
- **`.bat` files**: Batch files for TOXSWA execution (one per project)
- **`.zip` files**: Combined archive containing all projects organized by folder

## Template Placeholders

The TPF generator supports the following placeholders:

- `<rCrop>` - Crop name
- `<rCompund>` - Substance name
- `<nApps>` - Number of applications
- `<srcProjName>` - Source project name
- `<srcProjPath>` - Source project path
- `<outputProjPath>` - Output project path
- `<SWANtpf>` - Parameter filename
- `<fName>` - Filename
- `<VP>` - Vapour pressure
- `<MitCount>` - Mitigation count
- `<ROVolRed>` - Runoff volume reduction
- `<ROFluxRed>` - Runoff flux reduction
- `<ErosMassRed>` - Erosion mass reduction
- `<ErosFluxRed>` - Erosion flux reduction
- `<NozRed>` - Nozzle reduction
- `<Step3>` - Use Step 3 mass loadings
- `<SelBuf>` - Select buffer width
- `<BuffWid>` - Buffer width
- `<MitMatrix>` - Mitigation scenario matrix

## API Endpoints

- `GET /` - Main project processing page
- `POST /process-paths` - Project path processing
- `GET /configure` - Configuration page
- `POST /generate` - File generation
- `GET /download` - Download page
- `GET /download/<filename>` - Download specific file
- `GET /api/project-info` - Project information API

## Development

### Adding New Parsers

1. Create a new parser class in the `parsers/` directory
2. Implement the required parsing methods
3. Update the routes to use the new parser

### Adding New Generators

1. Create a new generator class in the `generators/` directory
2. Implement the required generation methods
3. Update the routes to use the new generator

### Customizing Templates

1. Modify the template files in the `templates/` directory
2. Update the placeholder replacement logic in `tpf_generator.py`
3. Test with sample data

## Testing

The application includes sample data in the `test_data/` directory:

- `BIXSC45_1AP/` - Complete TOXSWA Step 3 project
- `BIXSC45_1AP_10mS_10m_VFS/` - SWAN Step 4 project
- `BIXSC45_1AP_10mS_10mL&M/` - SWAN Step 4 project

Use these folders to test the application functionality.

## Troubleshooting

### Common Issues

1. **Path Access Errors**: Ensure the application has read access to the project folders
2. **Parsing Errors**: Check that `.txw` and `_report.txt` files are valid
3. **Template Errors**: Verify that the template file exists and has correct placeholders
4. **Generation Errors**: Check that all required parameters are provided

### Debug Mode

Run the application in debug mode for detailed error messages:

```python
app.run(debug=True)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository. 