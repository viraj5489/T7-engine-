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
        'nocheckcertificate': True,
        # The Secret Sauce: Pretending to be an Android TV
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
            
            # Try to get the direct URL
            download_url = info.get('url')
            
            # If the direct URL isn't there, check the formats list
            if not download_url and 'formats' in info:
                # We look for the last format that has both video and audio
                for f in reversed(info['formats']):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        download_url = f.get('url')
                        break

            if not download_url:
                return jsonify({"error": "YouTube blocked this specific video format."}), 403

            return jsonify({"url": download_url})
    except Exception as e:
        return jsonify({"error": "YouTube bot-check still active. Try again in 10 minutes."}), 500
      
