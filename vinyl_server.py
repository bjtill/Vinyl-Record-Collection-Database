#!/usr/bin/env python3
"""
Vinyl Collection Database Server
A Flask-based web application for managing vinyl record collections
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import requests
import os
import json
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)

# Configuration
DATABASE = 'vinyl_collection.db'
DISCOGS_API_URL = 'https://api.discogs.com'
USER_AGENT = 'VinylCollectionApp/1.0'

# Initialize database
def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT,
            discogs_id TEXT,
            artist TEXT NOT NULL,
            album_title TEXT NOT NULL,
            format TEXT,
            format_description TEXT,
            release_date TEXT,
            year INTEGER,
            country TEXT,
            label TEXT,
            catalog_number TEXT,
            genres TEXT,
            styles TEXT,
            cover_image_url TEXT,
            cover_image_data TEXT,
            storage_location TEXT,
            comments TEXT,
            date_added TEXT,
            last_modified TEXT,
            discogs_url TEXT
        )
    ''')
    
    c.execute('''
        CREATE INDEX IF NOT EXISTS idx_barcode ON records(barcode)
    ''')
    
    c.execute('''
        CREATE INDEX IF NOT EXISTS idx_artist ON records(artist)
    ''')
    
    c.execute('''
        CREATE INDEX IF NOT EXISTS idx_album_title ON records(album_title)
    ''')
    
    conn.commit()
    conn.close()

# Discogs API functions
def search_discogs_by_barcode(barcode, token):
    """Search Discogs by barcode"""
    headers = {
        'User-Agent': USER_AGENT,
        'Authorization': f'Discogs token={token}'
    }
    
    url = f'{DISCOGS_API_URL}/database/search'
    params = {
        'barcode': barcode,
        'type': 'release'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error searching Discogs by barcode: {e}")
        return None

def search_discogs_by_title(query, token):
    """Search Discogs by title/artist"""
    headers = {
        'User-Agent': USER_AGENT,
        'Authorization': f'Discogs token={token}'
    }
    
    url = f'{DISCOGS_API_URL}/database/search'
    params = {
        'q': query,
        'type': 'release'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error searching Discogs by title: {e}")
        return None

def get_discogs_release(release_id, token):
    """Get detailed release information from Discogs"""
    headers = {
        'User-Agent': USER_AGENT,
        'Authorization': f'Discogs token={token}'
    }
    
    url = f'{DISCOGS_API_URL}/releases/{release_id}'
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error getting Discogs release: {e}")
        return None

def download_cover_image(url):
    """Download and encode cover image as base64"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Convert to base64
        img = Image.open(BytesIO(response.content))
        # Resize if too large
        img.thumbnail((800, 800), Image.Resampling.LANCZOS)
        
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{img_str}"
    except Exception as e:
        print(f"Error downloading cover image: {e}")
        return None

def parse_discogs_data(data):
    """Parse Discogs release data into our database format"""
    parsed = {
        'discogs_id': str(data.get('id', '')),
        'artist': ', '.join([a.get('name', '') for a in data.get('artists', [])]),
        'album_title': data.get('title', ''),
        'year': data.get('year'),
        'country': data.get('country', ''),
        'label': ', '.join([l.get('name', '') for l in data.get('labels', [])]),
        'catalog_number': ', '.join([l.get('catno', '') for l in data.get('labels', [])]),
        'genres': ', '.join(data.get('genres', [])),
        'styles': ', '.join(data.get('styles', [])),
        'discogs_url': data.get('uri', ''),
    }
    
    # Parse format information
    formats = data.get('formats', [])
    if formats:
        format_info = formats[0]
        parsed['format'] = format_info.get('name', '')
        
        descriptions = format_info.get('descriptions', [])
        parsed['format_description'] = ', '.join(descriptions) if descriptions else ''
    
    # Get cover image
    images = data.get('images', [])
    if images:
        parsed['cover_image_url'] = images[0].get('uri', '')
    
    # Release date
    if data.get('released'):
        parsed['release_date'] = data.get('released')
    elif parsed['year']:
        parsed['release_date'] = str(parsed['year'])
    
    return parsed

# API Routes
@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'vinyl_collection.html')

@app.route('/api/search/barcode', methods=['POST'])
def search_barcode():
    """Search for a record by barcode using Discogs API"""
    data = request.json
    barcode = data.get('barcode')
    token = data.get('token')
    
    if not barcode or not token:
        return jsonify({'error': 'Barcode and token required'}), 400
    
    # Search Discogs
    results = search_discogs_by_barcode(barcode, token)
    
    if not results or not results.get('results'):
        return jsonify({'error': 'No results found'}), 404
    
    # Get the first result and fetch detailed info
    release_id = results['results'][0]['id']
    release_data = get_discogs_release(release_id, token)
    
    if not release_data:
        return jsonify({'error': 'Could not fetch release details'}), 500
    
    parsed_data = parse_discogs_data(release_data)
    parsed_data['barcode'] = barcode
    
    # Download cover image if available
    if parsed_data.get('cover_image_url'):
        cover_data = download_cover_image(parsed_data['cover_image_url'])
        if cover_data:
            parsed_data['cover_image_data'] = cover_data
    
    return jsonify(parsed_data)

@app.route('/api/search/title', methods=['POST'])
def search_title():
    """Search for records by title/artist using Discogs API"""
    data = request.json
    query = data.get('query')
    token = data.get('token')
    
    if not query or not token:
        return jsonify({'error': 'Query and token required'}), 400
    
    # Search Discogs
    results = search_discogs_by_title(query, token)
    
    if not results or not results.get('results'):
        return jsonify({'error': 'No results found'}), 404
    
    # Return simplified list of results
    simplified_results = []
    for result in results['results'][:10]:  # Limit to 10 results
        simplified_results.append({
            'id': result.get('id'),
            'artist': ', '.join([a for a in result.get('artist', '').split(' - ')]),
            'title': result.get('title', ''),
            'year': result.get('year', ''),
            'format': ', '.join(result.get('format', [])),
            'label': ', '.join(result.get('label', [])),
            'country': result.get('country', ''),
            'thumb': result.get('thumb', ''),
            'cover_image': result.get('cover_image', '')
        })
    
    return jsonify(simplified_results)

@app.route('/api/release/<release_id>', methods=['POST'])
def get_release(release_id):
    """Get detailed information about a specific release"""
    data = request.json
    token = data.get('token')
    barcode = data.get('barcode', '')
    
    if not token:
        return jsonify({'error': 'Token required'}), 400
    
    release_data = get_discogs_release(release_id, token)
    
    if not release_data:
        return jsonify({'error': 'Could not fetch release details'}), 500
    
    parsed_data = parse_discogs_data(release_data)
    parsed_data['barcode'] = barcode
    
    # Download cover image if available
    if parsed_data.get('cover_image_url'):
        cover_data = download_cover_image(parsed_data['cover_image_url'])
        if cover_data:
            parsed_data['cover_image_data'] = cover_data
    
    return jsonify(parsed_data)

@app.route('/api/records', methods=['GET'])
def get_records():
    """Get all records from the database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Get query parameters for filtering/sorting
    search = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'artist')
    sort_order = request.args.get('sort_order', 'ASC')
    
    query = 'SELECT * FROM records'
    params = []
    
    if search:
        query += ' WHERE artist LIKE ? OR album_title LIKE ? OR label LIKE ?'
        search_term = f'%{search}%'
        params = [search_term, search_term, search_term]
    
    # Validate sort parameters
    valid_sorts = ['artist', 'album_title', 'year', 'date_added', 'storage_location']
    if sort_by not in valid_sorts:
        sort_by = 'artist'
    if sort_order not in ['ASC', 'DESC']:
        sort_order = 'ASC'
    
    query += f' ORDER BY {sort_by} {sort_order}'
    
    c.execute(query, params)
    records = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return jsonify(records)

@app.route('/api/records', methods=['POST'])
def add_record():
    """Add a new record to the database"""
    data = request.json
    
    required_fields = ['artist', 'album_title']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    
    c.execute('''
        INSERT INTO records (
            barcode, discogs_id, artist, album_title, format, format_description,
            release_date, year, country, label, catalog_number, genres, styles,
            cover_image_url, cover_image_data, storage_location, comments,
            date_added, last_modified, discogs_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('barcode'),
        data.get('discogs_id'),
        data.get('artist'),
        data.get('album_title'),
        data.get('format'),
        data.get('format_description'),
        data.get('release_date'),
        data.get('year'),
        data.get('country'),
        data.get('label'),
        data.get('catalog_number'),
        data.get('genres'),
        data.get('styles'),
        data.get('cover_image_url'),
        data.get('cover_image_data'),
        data.get('storage_location'),
        data.get('comments'),
        now,
        now,
        data.get('discogs_url')
    ))
    
    record_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': record_id, 'message': 'Record added successfully'}), 201

@app.route('/api/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    """Update an existing record"""
    data = request.json
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    
    c.execute('''
        UPDATE records SET
            barcode = ?,
            discogs_id = ?,
            artist = ?,
            album_title = ?,
            format = ?,
            format_description = ?,
            release_date = ?,
            year = ?,
            country = ?,
            label = ?,
            catalog_number = ?,
            genres = ?,
            styles = ?,
            cover_image_url = ?,
            cover_image_data = ?,
            storage_location = ?,
            comments = ?,
            last_modified = ?,
            discogs_url = ?
        WHERE id = ?
    ''', (
        data.get('barcode'),
        data.get('discogs_id'),
        data.get('artist'),
        data.get('album_title'),
        data.get('format'),
        data.get('format_description'),
        data.get('release_date'),
        data.get('year'),
        data.get('country'),
        data.get('label'),
        data.get('catalog_number'),
        data.get('genres'),
        data.get('styles'),
        data.get('cover_image_url'),
        data.get('cover_image_data'),
        data.get('storage_location'),
        data.get('comments'),
        now,
        data.get('discogs_url'),
        record_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Record updated successfully'})

@app.route('/api/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete a record from the database"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('DELETE FROM records WHERE id = ?', (record_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Record deleted successfully'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get collection statistics"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM records')
    total_records = c.fetchone()[0]
    
    c.execute('SELECT COUNT(DISTINCT artist) FROM records')
    total_artists = c.fetchone()[0]
    
    c.execute('SELECT format, COUNT(*) as count FROM records GROUP BY format ORDER BY count DESC')
    formats = [{'format': row[0] or 'Unknown', 'count': row[1]} for row in c.fetchall()]
    
    c.execute('SELECT year, COUNT(*) as count FROM records WHERE year IS NOT NULL GROUP BY year ORDER BY year')
    years = [{'year': row[0], 'count': row[1]} for row in c.fetchall()]
    
    conn.close()
    
    return jsonify({
        'total_records': total_records,
        'total_artists': total_artists,
        'formats': formats,
        'years': years
    })

if __name__ == '__main__':
    # Initialize database on first run
    if not os.path.exists(DATABASE):
        print("Initializing database...")
        init_db()
        print("Database initialized successfully!")
    
    print("\n" + "="*60)
    print("Vinyl Collection Database Server")
    print("="*60)
    print("\nServer starting on http://0.0.0.0:5000")
    print("Access from this computer: http://localhost:5000")
    print("Access from other devices: http://YOUR_IP_ADDRESS:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
