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
        # This forces the use of the "Web" client which is harder to block
        'youtube_include_dash_manifest': False,
        'extractor_args': {
            'youtube': {
                'player_client': ['web'],
                'skip': ['dash', 'hls']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.youtube.com',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            
            # Fallback if first URL is missing
            if not download_url and 'formats' in info:
                for f in reversed(info['formats']):
                    if f.get('url') and (f.get('vcodec') != 'none' and f.get('acodec') != 'none'):
                        download_url = f['url']
                        break
            
            if not download_url:
                return jsonify({"error": "YouTube blocked this specific video. Try a different one."}), 403
                
            return jsonify({"url": download_url})
    except Exception as e:
        return jsonify({"error": "Bot-check triggered. Please wait 10 mins or try a different video."}), 500
