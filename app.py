import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

# Root route to prevent "Not Found" error
@app.route('/', methods=['GET'])
def health_check():
    return "<h1>T7 Engine Online</h1><p>Status: Active</p>", 200

# Main API route for trendyever7.com
@app.route('/api/index', methods=['GET', 'POST'])
def get_video_data():
    if request.method == 'GET':
        return jsonify({"status": "API is listening"}), 200

    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL parameter"}), 400

    video_url = data['url']
    cookie_path = 'cookies.txt'
    
    # 2026 Stealth Configuration for Render
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # Use cookies if they exist in your GitHub repo
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'extractor_args': {
            'youtube': {
                # 'tvhtml5' and 'android' are best for avoiding Error 152
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
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration')
            })
    except Exception as e:
        # Returns the specific error to your website console
        return jsonify({"error": str(e)}), 403

if __name__ == "__main__":
    # Render requires the port to be dynamic
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
