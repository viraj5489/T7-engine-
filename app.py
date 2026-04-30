import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/index', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return jsonify({"status": "Online", "message": "T7 Engine Running"}), 200
    
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"error": "No URL"}), 400

        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            'extractor_args': {'youtube': {'player_client': ['ios']}}
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"url": info.get('url')})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

app = app
