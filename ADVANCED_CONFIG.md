# Configuration Options for Advanced Users

# This file documents various configuration options you can modify
# in vinyl_server.py to customize the application behavior

## Conda Environment Management

### Using Different Python Versions
```bash
# Create environment with specific Python version
conda create -n vinyl python=3.11 -y
conda activate vinyl
pip install flask flask-cors requests pillow
```

### Exporting Environment
```bash
# Export for replication on another machine
conda activate vinyl
conda env export > vinyl-environment.yml

# Import on another machine
conda env create -f vinyl-environment.yml
```

### Managing Dependencies
```bash
# List all installed packages
conda activate vinyl
pip list

# Update all packages
pip install --upgrade flask flask-cors requests pillow

# Pin specific versions (if needed for stability)
pip install flask==3.0.0 werkzeug==3.0.0
```

## SSL Certificate Configuration

## SSL Certificate Configuration

### Regenerating Certificates
Certificates expire after 365 days:
```bash
cd ~/vinyl-collection
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

### Using Custom Domain (Advanced)
If you have a custom domain pointing to your server:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 \
  -subj "/CN=vinyl.mydomai.local"
```

### Using Let's Encrypt (For Public Access)
**Warning:** Only if you're exposing this to the internet (not recommended without authentication)

```bash
# Install certbot
sudo apt install certbot

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com

# Use in vinyl_server.py
ssl_context=('/etc/letsencrypt/live/yourdomain.com/fullchain.pem', 
             '/etc/letsencrypt/live/yourdomain.com/privkey.pem')
```

### Disabling HTTPS (Desktop Only Use)
If you only access from desktop (no mobile camera scanning):

**In vinyl_server.py:**
```python
# Change from:
app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))

# To:
app.run(host='0.0.0.0', port=5000, debug=True)
```

Access at: `http://localhost:5000`

**Limitation:** Barcode scanning won't work on mobile devices.

## Server Configuration

### Port Number
# Default: 5000
# To change: Edit vinyl_server.py, line ~430
# app.run(host='0.0.0.0', port=5000, debug=True)
# Change 5000 to your desired port

### Debug Mode
# Default: True (shows detailed errors, auto-reloads on code changes)
# Production: Set to False for better performance and security
# Location: vinyl_server.py, line ~430
# app.run(host='0.0.0.0', port=5000, debug=False)

### Host Binding
# Default: 0.0.0.0 (accessible from network)
# Localhost only: Change to 127.0.0.1
# Location: vinyl_server.py, line ~430
# app.run(host='127.0.0.1', port=5000, debug=True)

## Database Configuration

### Database Location
# Default: vinyl_collection.db (in same directory as server)
# To change: Edit vinyl_server.py, line ~15
# DATABASE = '/path/to/custom/location/vinyl_collection.db'

### Database Indexes
# The application creates indexes on:
# - barcode
# - artist  
# - album_title
# These improve search performance but use disk space

## API Configuration

### User Agent
# Default: 'VinylCollectionApp/1.0'
# Location: vinyl_server.py, line ~16
# USER_AGENT = 'YourCustomName/Version'

### Request Timeout
# Default: 10 seconds
# Location: Multiple places in vinyl_server.py
# Search for: timeout=10
# Increase if you have slow internet connection

### Cover Image Size
# Default: 800x800 pixels (automatically resized)
# Location: vinyl_server.py, line ~106
# img.thumbnail((800, 800), Image.Resampling.LANCZOS)
# Larger = better quality but more storage

### Cover Image Quality
# Default: 85% JPEG quality
# Location: vinyl_server.py, line ~109
# img.save(buffer, format='JPEG', quality=85)
# Range: 1-100 (higher = better quality, larger file)

### Search Result Limit
# Default: 10 results
# Location: vinyl_server.py, line ~183
# for result in results['results'][:10]:
# Change 10 to show more/fewer results

## Security Options

### CORS (Cross-Origin Resource Sharing)
# Default: Enabled (CORS(app))
# To restrict to specific origins:
# CORS(app, origins=['http://192.168.1.100:5000'])

### API Rate Limiting
# Not currently implemented
# Discogs API limits: 60 requests/minute
# Consider adding flask-limiter if needed

## Performance Tuning

### SQLite Optimizations
# Add these to init_db() function in vinyl_server.py:
# 
# conn.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging
# conn.execute('PRAGMA synchronous=NORMAL')  # Faster commits
# conn.execute('PRAGMA cache_size=-64000')  # 64MB cache
# conn.execute('PRAGMA temp_store=MEMORY')  # Use RAM for temp tables

### Response Compression
# Add gzip compression for better performance:
# 
# from flask_compress import Compress
# compress = Compress()
# compress.init_app(app)
# 
# Requires: pip install flask-compress

## UI Customization

### Theme Colors
# Primary color: #667eea (purple)
# Secondary: #764ba2 (darker purple)
# Location: vinyl_collection.html, <style> section
# Search for these hex codes and replace

### Grid Layout
# Default: Auto-fill, minimum 250px per card
# Location: vinyl_collection.html, line ~316
# grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
# Change 250px to adjust card size

### Items Per Row (Desktop)
# Controlled by minmax() - smaller min = more items
# For more items: minmax(200px, 1fr)
# For fewer items: minmax(300px, 1fr)

### Cover Image Height
# Default: 250px
# Location: vinyl_collection.html, line ~328
# height: 250px;
# Adjust for taller/shorter cards

## Data Fields

### Add Custom Fields
# To add new fields to database:
# 
# 1. Add column to CREATE TABLE in init_db() function
# 2. Add to INSERT and UPDATE queries
# 3. Add to HTML form in vinyl_collection.html
# 4. Add to JavaScript save/load functions

### Example: Adding a "Condition" Field
# 
# Database (vinyl_server.py, init_db):
# condition TEXT,
# 
# API routes (add to INSERT/UPDATE):
# data.get('condition'),
# 
# HTML form (vinyl_collection.html):
# <div>
#     <label>Condition</label>
#     <select id="condition">
#         <option>Mint</option>
#         <option>Near Mint</option>
#         <option>Very Good</option>
#         <option>Good</option>
#         <option>Fair</option>
#         <option>Poor</option>
#     </select>
# </div>
# 
# JavaScript (openAddModal):
# document.getElementById('condition').value = data.condition || '';
# 
# JavaScript (saveRecord):
# condition: document.getElementById('condition').value,

## Backup Automation

### Automatic Daily Backups (Cron)
# Create a script: backup_vinyl.sh
# 
# #!/bin/bash
# DATE=$(date +%Y%m%d)
# cp /path/to/vinyl_collection.db /path/to/backups/vinyl_$DATE.db
# find /path/to/backups -name "vinyl_*.db" -mtime +30 -delete
# 
# Add to crontab: crontab -e
# 0 2 * * * /path/to/backup_vinyl.sh

## Logging

### Enable File Logging
# Add to vinyl_server.py after imports:
# 
# import logging
# logging.basicConfig(
#     filename='vinyl_server.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

### Log API Requests
# Add to each API route:
# app.logger.info(f'API call: {request.method} {request.path}')

## Apache/Nginx Integration

### Apache Virtual Host
# <VirtualHost *:80>
#     ServerName vinyl.local
#     ProxyPreserveHost On
#     ProxyPass / http://localhost:5000/
#     ProxyPassReverse / http://localhost:5000/
# </VirtualHost>

### Nginx Configuration
# server {
#     listen 80;
#     server_name vinyl.local;
#     location / {
#         proxy_pass http://localhost:5000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#     }
# }

## Environment Variables

### Using .env File
# Create .env file:
# FLASK_ENV=development
# FLASK_DEBUG=True
# DATABASE_PATH=/custom/path/vinyl.db
# 
# Load in vinyl_server.py:
# from dotenv import load_dotenv
# load_dotenv()
# DATABASE = os.getenv('DATABASE_PATH', 'vinyl_collection.db')

## Multi-User Support (Advanced)

### Basic Authentication
# Add to vinyl_server.py:
# 
# from flask_httpauth import HTTPBasicAuth
# auth = HTTPBasicAuth()
# 
# users = {
#     "admin": "password"  # Use hashed passwords in production!
# }
# 
# @auth.verify_password
# def verify_password(username, password):
#     if username in users and users[username] == password:
#         return username
# 
# @app.route('/api/records', methods=['GET'])
# @auth.login_required
# def get_records():
#     # ... existing code

## Testing Configuration

### Test Mode
# Set environment variable:
# TESTING=True
# 
# Use separate test database:
# if os.getenv('TESTING'):
#     DATABASE = 'test_vinyl.db'

## Monitoring

### Health Check Endpoint
# Add to vinyl_server.py:
# 
# @app.route('/health')
# def health():
#     return jsonify({
#         'status': 'healthy',
#         'database': os.path.exists(DATABASE),
#         'records': get_record_count()
#     })

---

## Important Notes

- **Always backup** before making configuration changes
- **Test changes** in development environment first
- **Restart server** after any Python code changes
- **Clear browser cache** after HTML/CSS changes
- **Check logs** if something doesn't work

## Getting Help

If you need help with advanced configurations:
1. Check Flask documentation: https://flask.palletsprojects.com/
2. Check SQLite documentation: https://www.sqlite.org/docs.html
3. Check Discogs API docs: https://www.discogs.com/developers

---

**Remember**: The default configuration works well for most users!
Only customize if you have specific needs.
