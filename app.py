from flask import Flask
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Add custom Jinja2 tests
@app.template_test('endswith')
def endswith_test(value, suffix):
    """Test if a string ends with a given suffix."""
    return str(value).endswith(suffix)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip', 'txt', 'txw', 'tpf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('temp', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Import routes after app is created
import routes

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True) 