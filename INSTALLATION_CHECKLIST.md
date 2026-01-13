# INSTALLATION CHECKLIST

Complete these steps to get your Vinyl Collection Database up and running!

## Prerequisites ✓

- [ ] Ubuntu Linux system (or compatible OS)
- [ ] Miniconda or Anaconda installed
- [ ] Internet connection (for Discogs API)
- [ ] Modern web browser
- [ ] Discogs account (free)
- [ ] OpenSSL (usually pre-installed on Ubuntu)

## Installation Steps

### 1. Download Files ✓
- [ ] vinyl_server.py
- [ ] vinyl_collection.html
- [ ] start_vinyl_server.sh
- [ ] README.md (optional, but recommended)
- [ ] QUICKSTART.md (optional)

### 2. Create Project Directory ✓
```bash
mkdir ~/vinyl-collection
cd ~/vinyl-collection
# Move downloaded files here
```

### 2. Create Project Directory ✓
```bash
mkdir ~/vinyl-collection
cd ~/vinyl-collection
# Move downloaded files here
```

### 3. Install/Verify Miniconda ✓
Check if conda is installed:
```bash
conda --version
```

If not installed, install Miniconda:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
# Restart terminal after installation
```

### 4. Create Conda Environment ✓
```bash
conda create -n vinyl python=3.10 -y
```

Verify creation:
```bash
conda env list
# Should show 'vinyl' in the list
```

### 5. Install Python Dependencies ✓
```bash
conda activate vinyl
pip install flask flask-cors requests pillow
```

Verify installation:
```bash
python3 -c "import flask, flask_cors, requests, PIL; print('All packages installed!')"
```

### 6. Generate SSL Certificates ✓
```bash
cd ~/vinyl-collection  # Your project directory
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
Press Enter through all prompts (or fill them out)

Verify created:
```bash
ls -l cert.pem key.pem
```

### 7. Update vinyl_server.py ✓
Edit the last line of `vinyl_server.py`:

Change:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

To:
```python
app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
```

### 8. Get Discogs API Token ✓
### 8. Get Discogs API Token ✓
- [ ] Go to https://www.discogs.com/settings/developers
- [ ] Click "Generate new token"
- [ ] Copy token to safe place
- [ ] Keep token private!

### 9. Find Your IP Address ✓
```bash
hostname -I | awk '{print $1}'
```
Write it down: __________________

### 10. Make Scripts Executable ✓
```bash
chmod +x start_vinyl_server.sh vinyl_server.py
```

### 6. Find Your IP Address ✓
```bash
hostname -I | awk '{print $1}'
```
Write it down: __________________

## First Run Test

### 11. Start the Server ✓
```bash
conda activate vinyl
./start_vinyl_server.sh
```

Expected output:
```
========================================================================
  🎵 VINYL COLLECTION DATABASE
========================================================================
...
Server starting on https://0.0.0.0:5000
```

### 12. Test Local Access ✓
- [ ] Open browser
- [ ] Go to https://localhost:5000
- [ ] Accept security warning (click "Advanced" then "Proceed")
- [ ] Page loads successfully
- [ ] Enter Discogs token in header
- [ ] Token saves (refresh page to verify)

### 13. Test Mobile Access ✓
- [ ] Connect phone to same WiFi network
- [ ] Open browser on phone
- [ ] Go to https://YOUR_IP:5000
- [ ] Accept security warning
- [ ] Page loads successfully
- [ ] Can see the same collection

### 14. Test Barcode Scanning ✓
### 14. Test Barcode Scanning ✓
- [ ] Click "Scan Barcode" tab
- [ ] Click "Start Camera"
- [ ] Camera activates
- [ ] Grant camera permissions if asked
- [ ] Scan a barcode (any UPC/EAN will work)
- [ ] Record info loads from Discogs

### 15. Test Search Function ✓
- [ ] Click "Search Title" tab
- [ ] Enter an artist name (try "Beatles")
- [ ] Results appear
- [ ] Click a result
- [ ] Info loads correctly

### 16. Add Test Record ✓
- [ ] Use barcode scan OR search
- [ ] Review loaded information
- [ ] Fill in storage location
- [ ] Add a comment
- [ ] Click "Save Record"
- [ ] Record appears in collection

### 17. Test Edit Function ✓
- [ ] Click on saved record
- [ ] Edit form opens
- [ ] Modify a field
- [ ] Click "Save Record"
- [ ] Changes are saved

### 18. Test Delete Function ✓
- [ ] Click on record
- [ ] Click "Delete" button
- [ ] Confirm deletion
- [ ] Record is removed

### 19. Test Statistics ✓
- [ ] Click "Statistics" tab
- [ ] Stats display correctly
- [ ] Numbers match collection

### 20. Verify Files Created ✓
```bash
ls -lh vinyl_collection.db cert.pem key.pem
```
All files should exist in project directory

## Troubleshooting Common Issues

### Server Won't Start
- [ ] Check conda is installed: `conda --version`
- [ ] Check environment exists: `conda env list | grep vinyl`
- [ ] Activate environment: `conda activate vinyl`
- [ ] Check packages installed: `pip list | grep flask`
- [ ] Check port 5000 not in use: `lsof -i :5000`
- [ ] Check file permissions: `ls -l vinyl_server.py`

### Camera Not Working
- [ ] Verify using HTTPS (not HTTP)
- [ ] Check SSL certificates exist: `ls -l cert.pem key.pem`
- [ ] Accept security warning on device
- [ ] Use Chrome or Firefox (best support)
- [ ] Check browser camera permissions
- [ ] Try incognito/private mode

### Can't Connect from Phone
- [ ] Verify same WiFi network
- [ ] Check IP address is correct
- [ ] Use HTTPS (not HTTP)
- [ ] Accept security warning for your IP address
- [ ] Try disabling firewall temporarily
- [ ] Check server is running (terminal shows activity)

### Discogs Errors
- [ ] Verify token is correct (no spaces)
- [ ] Check internet connection
- [ ] Try different search term
- [ ] Wait a minute (rate limit)

### Conda Environment Issues
- [ ] Conda not found: Run `conda init bash` and restart terminal
- [ ] Environment doesn't exist: `conda create -n vinyl python=3.10 -y`
- [ ] Packages not found: `conda activate vinyl` then `pip install flask flask-cors requests pillow`
- [ ] Wrong Python version: Check with `python3 --version` (should be 3.10)

### SSL Certificate Issues
- [ ] Missing cert files: Run generation command again
- [ ] Expired certificate: Regenerate (valid for 365 days)
- [ ] Permission errors: `chmod 644 cert.pem key.pem`

### Flask/Werkzeug Version Conflicts
If you see `ImportError: cannot import name 'url_quote'`:
```bash
conda activate vinyl
pip uninstall flask werkzeug -y
pip install flask flask-cors requests pillow
```

## Post-Installation

### Create First Backup ✓
```bash
cp vinyl_collection.db vinyl_collection_backup.db
```

### Bookmark URLs ✓
- [ ] http://localhost:5000 (on computer)
- [ ] http://YOUR_IP:5000 (on phone)

### Test Backup/Restore ✓
```bash
# Create backup
cp vinyl_collection.db backup_test.db

# Stop server (Ctrl+C)

# Remove original
rm vinyl_collection.db

# Restore
cp backup_test.db vinyl_collection.db

# Restart server
./start_vinyl_server.sh

# Verify data is intact
```

### Schedule Regular Backups ✓
```bash
# Add to crontab for daily backups at 2 AM
crontab -e

# Add this line:
0 2 * * * cp ~/vinyl-collection/vinyl_collection.db ~/vinyl-collection/backups/vinyl_$(date +\%Y\%m\%d).db
```

## Optional Enhancements

### Add to Startup (systemd) ✓
- [ ] Create service file
- [ ] Enable service
- [ ] Test auto-start
(See README.md for instructions)

### Set Up Apache Proxy ✓
- [ ] Configure Apache
- [ ] Create virtual host
- [ ] Test access
(See ADVANCED_CONFIG.md for instructions)

### Create Desktop Shortcut ✓
Create: `~/Desktop/vinyl-collection.desktop`
```
[Desktop Entry]
Version=1.0
Type=Application
Name=Vinyl Collection
Exec=gnome-terminal -- bash -c 'cd ~/vinyl-collection && ./start_vinyl_server.sh; bash'
Icon=multimedia-audio-player
Terminal=true
```

### Add to Phone Home Screen ✓
On phone browser:
- [ ] Visit http://YOUR_IP:5000
- [ ] Open browser menu
- [ ] Select "Add to Home Screen"
- [ ] Name it "Vinyl Collection"
- [ ] Use like an app!

## Final Checks

- [ ] Server starts without errors
- [ ] Can access from computer
- [ ] Can access from phone
- [ ] Barcode scanning works
- [ ] Search works
- [ ] Records save and load
- [ ] Database file exists
- [ ] Backup created
- [ ] Token saved in browser
- [ ] Documentation reviewed

## Success! 🎉

Your Vinyl Collection Database is ready to use!

### Next Steps:
1. Start adding your vinyl collection
2. Organize with storage locations
3. Add personal notes and comments
4. Explore the statistics page
5. Set up regular backups
6. Share with friends (if desired)

### Tips for Best Experience:
- Use good lighting when scanning barcodes
- Fill in storage locations as you go
- Add comments about condition or memories
- Back up weekly or after big additions
- Keep your Discogs token private

### Need Help?
- Read QUICKSTART.md for daily usage
- Check README.md for detailed info
- Review ADVANCED_CONFIG.md for customization
- Check server terminal for error messages
- Look at browser console (F12) for issues

---

**Installation Date**: _______________  
**Initial Record Count**: _______________  
**Your IP Address**: _______________  
**Backup Schedule**: _______________

**Congratulations on setting up your Vinyl Collection Database!**
