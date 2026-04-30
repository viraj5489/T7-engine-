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
    # Simple check to see if the API is awake
    if request.method == 'GET':
        return jsonify({
            "status": "Online",
            "message": "T7 Engine API is ready for requests"
        }), 200

    # Get the URL from your website's POST request
    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400

    video_url = data['url']
    cookie_path = 'cookies.txt'
    
    # 2026 Professional Extraction Settings
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # Use cookies if the file exists on GitHub
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'tvhtml5'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # Send the direct download link back to your website
            return jsonify({
                "url": info.get('url'),
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail')
            })
    except Exception as e:
        # If YouTube blocks the request, this error helps you know why
        return jsonify({"error": f"YouTube Wall Active: {str(e)}"}), 403

# Required for Render to find the correct Port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
