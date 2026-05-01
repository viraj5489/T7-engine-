import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# Enable CORS so your website trendyever7.com can talk to this server
CORS(app)

# FIX: This handles the main URL (https://t7-engine.onrender.com)
@app.route('/', methods=['GET'])
def health_check():
    return "<h1>T7 Engine is Online</h1><p>API Endpoint: <code>/api/index</code></p>", 200

# This handles the actual video link generation
@app.route('/api/index', methods=['GET', 'POST'])
def get_video_link():
    if request.method == 'GET':
        return jsonify({"status": "Online", "message": "API is ready"}), 200

    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400

    video_url = data['url']
    cookie_path = 'cookies.txt'
    
    # EXACT ALIGNMENT START
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'tvhtml5'],
                'skip': ['webpage', 'hls', 'dash'],
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }
    # EXACT ALIGNMENT END

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "url": info.get('url'),
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"error": f"Bot Check Active: {str(e)}"}), 403

# Required for Render to find the correct Port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
