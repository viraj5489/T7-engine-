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
    
    # Path to cookies in the root folder
    cookie_path = 'cookies.txt'
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # TRICK 1: Use the Cookies if the file exists
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        # TRICK 2: Use the "TV" client to bypass the bot-check
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
            
            if not download_url and 'formats' in info:
                for f in reversed(info['formats']):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        download_url = f.get('url')
                        break

            return jsonify({"url": download_url})
    except Exception as e:
        # This is the message you saw in your screenshot
        return jsonify({"error": "YouTube Bot-Check active. Refresh cookies or try later."}), 403

app = app
# Required for Vercel 2026
app = app
