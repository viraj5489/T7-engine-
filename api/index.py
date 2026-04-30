from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

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
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        # Force the engine to use a different extraction client
        'youtube_include_dash_manifest': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
        },
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We use 'download=False' to just get the link
            info = ydl.extract_info(video_url, download=False)
            
            # Check for direct URL or manifest URL
            download_url = info.get('url') or info.get('formats', [{}])[-1].get('url')
            
            if not download_url:
                return jsonify({"error": "Link not found for this specific video."}), 404
                
            return jsonify({"url": download_url})
    except Exception as e:
        # If it still fails, give a clear instruction to the user
        return jsonify({"error": "YouTube bot-check triggered. Try again in a few minutes with a different video link."}), 500
