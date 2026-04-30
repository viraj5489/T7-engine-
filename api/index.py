from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/index', methods=['POST'])
def get_link():
    data = request.json
    url = data.get('url')
    ydl_opts = {'format': 'best', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"url": info['url']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
      
