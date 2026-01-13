# QUICK START GUIDE

## First Time Setup (10 minutes)

1. **Install Miniconda** (if not already installed)
   - Download: https://docs.conda.io/en/latest/miniconda.html
   - Install and restart terminal

2. **Create Conda Environment**
   ```bash
   conda create -n vinyl python=3.10 -y
   conda activate vinyl
   pip install flask flask-cors requests pillow
   ```

3. **Generate SSL Certificates**
   ```bash
   cd ~/vinyl-collection  # Your vinyl database directory
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   # Press Enter through all prompts
   ```

4. **Update vinyl_server.py**
   - Edit the last line to add SSL:
   ```python
   app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
   ```

5. **Get Discogs Token**
   - Go to: https://www.discogs.com/settings/developers
   - Click "Generate new token"
   - Copy the token

6. **Start Server**
   ```bash
   conda activate vinyl
   ./start_vinyl_server.sh
   ```

7. **Open Browser**
   - On computer: https://localhost:5000
   - On phone: https://YOUR_IP:5000 (shown when server starts)
   - Accept security warning (self-signed certificate is safe for local use)

8. **Enter Token**
   - Paste your Discogs token in the header field
   - Token is saved automatically

## Daily Use

### Starting the Server
```bash
cd /path/to/vinyl/database
conda activate vinyl
./start_vinyl_server.sh
```

Or manually:
```bash
conda activate vinyl
python3 vinyl_server.py
```

### Adding a Record

**With Barcode:**
1. Click "Scan Barcode" tab
2. Click "Start Camera"
3. Point at barcode
4. Review info → Save

**Without Barcode:**
1. Click "Search Title" tab
2. Type artist/album name
3. Select from results
4. Review info → Save

**Manual Entry:**
1. Click "Manual Entry" tab
2. Click "Open Manual Entry Form"
3. Fill in fields
4. Save

### Viewing Your Collection
- Browse: Scroll through grid view
- Search: Type in search box
- Sort: Use dropdown menus
- Edit: Click any record card

## Keyboard Shortcuts

- **Ctrl+F**: Focus search box (in most browsers)
- **Esc**: Close modal window
- **Tab**: Navigate form fields

## Mobile Tips

- **Scanning**: Hold steady, good lighting helps
- **Horizontal scrolling**: Swipe to see more records
- **Zoom**: Pinch to zoom images
- **Add to Home Screen**: Create app-like experience

## Common Tasks

### Backup Your Database
```bash
cp vinyl_collection.db backup_$(date +%Y%m%d).db
```

### Find Your IP Address
```bash
hostname -I | awk '{print $1}'
```

### Stop the Server
Press **Ctrl+C** in the terminal

### Check if Server is Running
```bash
ps aux | grep vinyl_server.py
```

### View Server Logs
Watch the terminal where you started the server

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Camera won't start | Verify using HTTPS, accept security warning, check browser permissions |
| Can't find server on phone | Check same WiFi network, verify IP address, use HTTPS not HTTP |
| No results from Discogs | Check token is correct, check internet connection |
| Slow performance | Restart server, clear browser cache |
| Database locked | Close other instances, restart server |
| Conda environment not found | Run: `conda create -n vinyl python=3.10 -y` |
| Package import errors | Run: `conda activate vinyl` then `pip install flask flask-cors requests pillow` |
| SSL certificate error | Regenerate: `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365` |

## File Locations

- **Database**: `vinyl_collection.db` (in server directory)
- **Server**: `vinyl_server.py`
- **Web Interface**: `vinyl_collection.html`
- **Documentation**: `README.md`

## URLs to Bookmark

- Local access: https://localhost:5000
- Discogs developers: https://www.discogs.com/settings/developers
- Discogs database: https://www.discogs.com/search

**Note:** Use HTTPS (not HTTP) for proper camera access on mobile devices.

## Best Practices

✅ **DO:**
- Backup database regularly
- Fill in storage location for easy finding
- Add comments for condition notes
- Use good lighting when scanning
- Keep Discogs token private

❌ **DON'T:**
- Expose server to internet without security
- Delete database file without backup
- Share your Discogs token
- Run multiple instances on same port
- Edit database file directly

## Field Guide

- **Artist**: Main performing artist(s)
- **Album Title**: Name of the release
- **Format**: Vinyl, 12", 10", 7", etc.
- **Format Description**: LP, EP, Single, 33⅓ RPM, 45 RPM, etc.
- **Year**: Release year
- **Country**: Country of release/pressing
- **Label**: Record label
- **Catalog Number**: Label's catalog number
- **Genres**: Broad categories (Rock, Jazz, Electronic)
- **Styles**: Specific sub-genres
- **Storage Location**: Where you keep it (Shelf A, Box 3, etc.)
- **Comments**: Condition, notes, memories, etc.

## Statistics You Can Track

- Total number of records
- Number of unique artists
- Records by format (LP, 7", etc.)
- Records by year
- Most collected artists
- Formats distribution

## Advanced Features

### Sorting Options
- By Artist (A-Z or Z-A)
- By Album Title
- By Year (oldest/newest first)
- By Date Added (latest/earliest first)

### Filtering
- Search across artist, title, and label
- Case-insensitive search
- Real-time filtering

### Storage Location Examples
- "Shelf A, Position 12"
- "Box 3 - Jazz Collection"
- "Living Room Crate"
- "Storage Unit B, Row 2"
- "Bedroom Shelf, Top Row"

## Support Resources

1. **README.md** - Complete documentation
2. **Terminal output** - Error messages and logs
3. **Browser Console** (F12) - Debug information
4. **Discogs API Docs** - https://www.discogs.com/developers

## Version Info

**Current Version**: 1.0  
**Release Date**: December 2025  
**Python Required**: 3.7+  
**Browser Required**: Modern (Chrome, Firefox, Safari, Edge)

---

**Happy Collecting! 🎵**
