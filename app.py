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

@app.route('/api/index', methods=['GET', 'POST'])
def get_video():
    if request.method == 'GET':
        return jsonify({"status": "ready"}), 200

    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "No URL"}), 400

    url = data['url']
    cookies = 'cookies.txt'
    
    # 2026 'TV-Bypass' Logic - Specifically to fix Error 152
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookies if os.path.exists(cookies) else None,
        'extractor_args': {
            'youtube': {
                # 'tv' and 'tv_downgraded' are the only ones skipping JS challenges
                'player_client': ['tv', 'tv_downgraded', 'web_embedded'],
                'player_skip': ['webpage', 'configs']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Mimic a human 'thinking' before clicking
            time.sleep(1.5)
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "url": info.get('url'),
                "title": info.get('title'),
                "thumb": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"error": f"YouTube security active: {str(e)}"}), 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
