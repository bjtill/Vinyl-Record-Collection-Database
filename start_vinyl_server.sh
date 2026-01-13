#!/bin/bash

# Vinyl Collection Database - Startup Script
# This script activates the conda environment and starts the Flask server with HTTPS

echo "========================================================================"
echo "  🎵 VINYL COLLECTION DATABASE"
echo "========================================================================"
echo ""

# Get local IP address
if command -v hostname &> /dev/null; then
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
    if [ -z "$LOCAL_IP" ]; then
        LOCAL_IP=$(ip addr show | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1 | head -n1)
    fi
else
    LOCAL_IP="YOUR_IP_ADDRESS"
fi

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ ERROR: conda is not installed or not in PATH"
    echo "   Please install Miniconda or Anaconda first."
    echo "   Visit: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Initialize conda for bash (if not already done)
eval "$(conda shell.bash hook)"

# Check if vinyl environment exists
if ! conda env list | grep -q "^vinyl "; then
    echo "❌ ERROR: 'vinyl' conda environment not found"
    echo ""
    echo "   Please create it first with:"
    echo "   conda create -n vinyl python=3.10 -y"
    echo "   conda activate vinyl"
    echo "   pip install flask flask-cors requests pillow"
    exit 1
fi

# Activate the vinyl environment
echo "  Activating conda environment 'vinyl'..."
conda activate vinyl

# Check if required packages are installed
echo "  Checking dependencies..."
python3 -c "import flask, flask_cors, requests, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Required Python packages are missing."
    echo "   Install them with:"
    echo "   conda activate vinyl"
    echo "   pip install flask flask-cors requests pillow"
    exit 1
fi

# Check if vinyl_server.py exists
if [ ! -f "vinyl_server.py" ]; then
    echo "❌ ERROR: vinyl_server.py not found in current directory"
    echo "   Make sure you're running this script from the correct directory."
    exit 1
fi

# Check if vinyl_collection.html exists
if [ ! -f "vinyl_collection.html" ]; then
    echo "⚠️  WARNING: vinyl_collection.html not found"
    echo "   The web interface may not work properly."
fi

# Check for SSL certificates
if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
    echo "⚠️  WARNING: SSL certificates not found (cert.pem and key.pem)"
    echo "   HTTPS is required for camera access on mobile devices."
    echo ""
    echo "   Generate them now? (y/n)"
    read -p "   " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "   Generating self-signed SSL certificate..."
        openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"
        if [ $? -eq 0 ]; then
            echo "   ✅ SSL certificates created successfully!"
        else
            echo "   ❌ Failed to create SSL certificates"
            exit 1
        fi
    else
        echo "   Continuing without SSL (camera scanning won't work on mobile)"
    fi
fi

echo ""
echo "  Starting server with HTTPS..."
echo ""
echo "  📱 Access from this computer:"
echo "     https://localhost:5000"
echo ""
echo "  📱 Access from mobile/other devices on your network:"
echo "     https://${LOCAL_IP}:5000"
echo ""
echo "  ⚠️  NOTE: You will see a security warning about the self-signed certificate."
echo "     This is normal - click 'Advanced' and 'Proceed' to continue."
echo ""
echo "  💡 Make sure your Discogs API token is ready!"
echo "     Get it at: https://www.discogs.com/settings/developers"
echo ""
echo "  ⏹️  Press Ctrl+C to stop the server"
echo ""
echo "========================================================================"
echo ""

echo "✅ All checks passed. Starting server..."
echo ""

# Start the Flask server
python3 vinyl_server.py
