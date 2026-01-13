# Vinyl-Record-Collection-Database
A web-based vinyl record collection management system with barcode scanning, Discogs integration, and local network access.
___________________________________________________________________________________________________________________

Use at your own risk.

I cannot provide support. All information obtained/inferred with this script is without any implied warranty of fitness for any purpose or use whatsoever.
________________________________________________________________________________________________________________________

## Features

- **Barcode Scanning**: Use your phone's camera to scan vinyl barcodes and automatically retrieve information
- **Discogs Integration**: Automatic metadata lookup including artist, album, format, year, label, genres, and cover art
- **Manual Search**: Search by title/artist when no barcode is available
- **Custom Fields**: Add storage location and personal comments
- **Responsive Design**: Works seamlessly on mobile devices and desktop computers
- **Local Network**: Access from any device on your home network
- **Platform Independent**: Pure web-based solution, no app installation required
- **Offline Ready**: All data stored locally on your computer

## Requirements

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Discogs account and API token
- Network connection for initial metadata lookup

## Installation

### 1. Install Miniconda (if not already installed)

If you don't have conda installed:

```bash
# Download Miniconda installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Make executable
chmod +x Miniconda3-latest-Linux-x86_64.sh

# Run installer
./Miniconda3-latest-Linux-x86_64.sh

# Follow prompts, accept license, and allow conda init
# Close and reopen terminal after installation
```

### 2. Create Conda Environment

Create a dedicated environment for the vinyl database:

```bash
# Create environment with Python 3.10
conda create -n vinyl python=3.10 -y

# Activate the environment
conda activate vinyl

# Install required packages
pip install flask flask-cors requests pillow
```

### 3. Generate SSL Certificates

HTTPS is required for camera access on mobile devices:

```bash
# Navigate to your vinyl database directory
cd ~/vinyl-collection

# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Press Enter through all prompts (or fill them out if you prefer)
```

### 4. Update vinyl_server.py for HTTPS

Edit the last line of `vinyl_server.py`:

**Change from:**
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

**Change to:**
```python
app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
```

### 5. Get Your Discogs API Token

1. Log into your Discogs account at [discogs.com](https://www.discogs.com)
2. Go to **Settings** → **Developers** (or visit https://www.discogs.com/settings/developers)
3. Click **"Generate new token"**
4. Copy the token - you'll need to enter it in the web interface

## Usage

### Starting the Server

1. Open a terminal in the directory containing the files

2. Activate the conda environment:
```bash
conda activate vinyl
```

3. Start the server using the startup script:
```bash
./start_vinyl_server.sh
```

Or start manually:
```bash
python3 vinyl_server.py
```

You should see output like:
```
============================================================
Vinyl Collection Database Server
============================================================

Server starting on https://0.0.0.0:5000
Access from this computer: https://localhost:5000
Access from other devices: https://YOUR_IP_ADDRESS:5000

Press Ctrl+C to stop the server
============================================================
```

**Note:** The server uses HTTPS (not HTTP) for camera access on mobile devices.

### Finding Your IP Address

To access from other devices on your network, you need your computer's local IP address:

**On Ubuntu/Linux:**
```bash
hostname -I | awk '{print $1}'
```

**Or use:**
```bash
ip addr show | grep "inet " | grep -v 127.0.0.1
```

Your IP will look something like `192.168.1.100`

### Accessing the Application

- **From the same computer**: Open browser to `https://localhost:5000`
- **From phone/tablet on same network**: Open browser to `https://YOUR_IP_ADDRESS:5000`

**Important:** You will see a security warning about the self-signed certificate. This is expected and safe:
- **Chrome/Firefox**: Click "Advanced" → "Proceed to localhost" (or your IP)
- **iOS Safari**: Tap "Show Details" → "visit this website"

The warning appears because the certificate is self-signed, but it's perfectly safe for local network use.

### Using the Application

1. **Enter Your Discogs Token**
   - On first visit, enter your Discogs API token in the header
   - The token will be saved in your browser for future visits

2. **Adding Records**
   
   **Option A: Scan Barcode**
   - Click "Start Camera"
   - Point camera at vinyl barcode
   - App automatically looks up and loads information
   - Review and save
   
   **Option B: Search by Title**
   - Enter artist or album name
   - Select from search results
   - Review and save
   
   **Option C: Manual Entry**
   - Click "Open Manual Entry Form"
   - Fill in all fields manually
   - Save record

3. **Managing Your Collection**
   - View all records in grid layout
   - Search/filter by artist, title, or label
   - Sort by artist, title, year, or date added
   - Click any record to view details or edit
   - Add storage location and comments
   - Delete records if needed

4. **View Statistics**
   - Click "Statistics" tab
   - See total records and unique artists
   - View breakdown by format

## Database

The application uses SQLite to store your collection locally. The database file `vinyl_collection.db` will be created automatically in the same directory as the server script.

### Database Schema

The database stores comprehensive information:
- Basic info: Artist, Album Title, Format, Year
- Detailed info: Label, Catalog Number, Country, Genres, Styles
- Custom fields: Storage Location, Comments
- Metadata: Discogs ID, Barcode, Cover Image
- Tracking: Date Added, Last Modified

### Backup Your Data

To backup your collection, simply copy the `vinyl_collection.db` file:

```bash
cp vinyl_collection.db vinyl_collection_backup_$(date +%Y%m%d).db
```

## Troubleshooting

### Camera Not Working
- Ensure you're using HTTPS (not HTTP)
- Verify SSL certificates exist (cert.pem and key.pem)
- Accept the security warning for your IP address on mobile device
- Check browser has camera permissions
- Use Chrome or Firefox for best compatibility

### Can't Access from Other Devices
- Check firewall settings on server computer
- Ensure both devices are on same network
- Verify you're using correct IP address
- Try port 5000 is not blocked

### Discogs API Errors
- Verify your API token is correct
- Check you're not exceeding API rate limits (60 requests/minute)
- Ensure you have internet connection

### Database Issues
- Check file permissions on `vinyl_collection.db`
- Ensure sufficient disk space
- Database file should be in same directory as server

### Conda Environment Issues
- Ensure conda is properly initialized: `conda init bash` then restart terminal
- Verify environment exists: `conda env list`
- If packages are missing: `conda activate vinyl` then `pip install flask flask-cors requests pillow`
- To recreate environment: `conda remove -n vinyl --all` then follow installation steps

### Flask/Werkzeug Version Conflicts
If you get `ImportError: cannot import name 'url_quote'` errors:

```bash
conda activate vinyl
pip uninstall flask werkzeug -y
pip install flask flask-cors requests pillow
```

## Alternative Installation Methods

### Method 1: System Python (Not Recommended)
If you prefer not to use conda:

```bash
pip install flask flask-cors requests pillow --break-system-packages
```

**Note:** This can cause conflicts with system packages and other Python projects. Conda environment is strongly recommended.

### Method 2: Python venv
Alternative to conda:

```bash
python3 -m venv vinyl-env
source vinyl-env/bin/activate
pip install flask flask-cors requests pillow
```

### Method 3: Without HTTPS (Desktop Only)
If you only need desktop access (no mobile camera scanning):

Keep the original `vinyl_server.py` without SSL:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

Access at: `http://localhost:5000`

**Limitation:** Barcode scanning won't work on mobile devices.

## Running as a Service (Advanced)

To have the server start automatically on boot, create a systemd service:

1. Create service file:
```bash
sudo nano /etc/systemd/system/vinyl-collection.service
```

2. Add content:
```ini
[Unit]
Description=Vinyl Collection Database Server
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/vinyl/app
ExecStart=/usr/bin/python3 /path/to/vinyl/app/vinyl_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start:
```bash
sudo systemctl enable vinyl-collection
sudo systemctl start vinyl-collection
```

## Apache Integration (Optional)

If you already have Apache running, you can proxy the Flask app through Apache:

1. Enable required modules:
```bash
sudo a2enmod proxy proxy_http
```

2. Add to your Apache config:
```apache
<VirtualHost *:80>
    ServerName vinyl.yourdomain.local
    
    ProxyPreserveHost On
    ProxyPass / http://localhost:5000/
    ProxyPassReverse / http://localhost:5000/
</VirtualHost>
```

3. Restart Apache:
```bash
sudo systemctl restart apache2
```

## Security Considerations

- This application is designed for **local network use only**
- Do not expose to the internet without proper authentication
- Keep your Discogs API token private
- Consider using HTTPS if accessing over network
- Regular backups recommended

## Data Privacy

- All data is stored locally on your computer
- No cloud services involved
- Discogs API only used for metadata lookup
- Cover images downloaded and stored locally

## Technical Details

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Barcode Scanner**: ZXing library
- **API Integration**: Discogs REST API

## Performance

- Handles 1000+ records efficiently
- SQLite database optimized with indexes
- Cover images stored as base64 (automatic compression to 800x800px)
- Responsive design adapts to any screen size

## Future Enhancements

Potential features for future versions:
- Import/export to CSV
- Multiple collection views (list, compact, detailed)
- Advanced filtering (by decade, genre, location)
- Wishlist functionality
- Duplicate detection
- Collection value tracking
- PDF/Excel reports
- Multi-user support

## Support

For issues or questions:
1. Check this README
2. Review error messages in browser console (F12)
3. Check server terminal output for errors
4. Verify Discogs API token is valid
5. Ensure all dependencies are installed

## Credits

- Discogs API for metadata
- ZXing library for barcode scanning
- Flask framework
- SQLite database

---

**Version**: 1.0  
**Last Updated**: January 2026  
**Python Version**: 3.7+  
**Tested On**: Ubuntu 24.04
