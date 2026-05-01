import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health():
    return "<h1>T7 Engine Online</h1>", 200

import shutil # Add this at the very top of your app.py

@app.route('/api/index', methods=['GET', 'POST'])
def get_video_data():
    if request.method == 'GET':
        return jsonify({"status": "API is listening"}), 200

    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL parameter"}), 400

    video_url = data['url']
    
    # --- RENDER READ-ONLY FIX START ---
    original_cookie_path = 'cookies.txt'
    temp_cookie_path = '/tmp/cookies.txt'

    # Move the cookie file to the writable /tmp folder
    if os.path.exists(original_cookie_path):
        shutil.copy2(original_cookie_path, temp_cookie_path)
    # --- RENDER READ-ONLY FIX END ---

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': temp_cookie_path if os.path.exists(temp_cookie_path) else None,
        'extractor_args': {
            'youtube': {
                'player_client': ['tvhtml5', 'android', 'web_embedded'],
                'player_skip': ['configs', 'webpage']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "url": info.get('url'),
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
