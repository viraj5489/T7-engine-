import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health():
    return "<h1>T7 Engine Online</h1>", 200

@app.route('/api/index', methods=['GET', 'POST'])
def get_video():
    if request.method == 'GET':
        return jsonify({"status": "ready"}), 200

    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "No URL"}), 400

    url = data['url']
    cookies = 'cookies.txt'
    
    # Updated 2026 Stealth Settings
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookies if os.path.exists(cookies) else None,
        'extractor_args': {
            'youtube': {
                # 'web_embedded' is the 2026 secret for bypassing bot checks
                'player_client': ['web_embedded', 'tvhtml5'],
                'player_skip': ['configs', 'webpage']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "url": info.get('url'),
                "title": info.get('title'),
                "thumb": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
