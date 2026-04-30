from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/index', methods=['POST', 'GET'])
def get_link():
    if request.method == 'GET':
        return jsonify({"status": "Online", "message": "T7 Engine is Running"}), 200

    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400

    video_url = data['url']
    
    # Path to cookies - since we moved app.py to root, cookies.txt is in root too
    cookie_path = 'cookies.txt'
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # Use cookies if the file exists
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        # Stealth TV and Mobile signatures
        'extractor_args': {
            'youtube': {
                'player_client': ['tvhtml5', 'android', 'ios'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            
            # Fallback if the first URL is restricted
            if not download_url and 'formats' in info:
                for f in reversed(info['formats']):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        download_url = f.get('url')
                        break

            if not download_url:
                return jsonify({"error": "Link extraction failed."}), 403

            return jsonify({"url": download_url})
    except Exception as e:
        error_msg = str(e)
        if "Sign in" in error_msg:
            return jsonify({"error": "YouTube Bot-Check active. Refresh cookies or try later."}), 403
        return jsonify({"error": "Engine busy. Try a different video."}), 500

# Required for Vercel 2026
app = app
