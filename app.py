from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/index', methods=['POST', 'GET'])
def get_link():
    if request.method == 'GET':
        return jsonify({"status": "Online", "message": "T7 Engine Running"}), 200

    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400

    video_url = data['url']
    cookie_path = 'cookies.txt'
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android'],
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
            return jsonify({"url": info.get('url')})
    except Exception as e:
        return jsonify({"error": "YouTube Bot-Check active. Refresh cookies."}), 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
                        break

            if not download_url:
                raise Exception("No URL extracted")

            return jsonify({"url": download_url})
    except Exception as e:
        # If it fails, we try ONE more time without the cookie to see if that's the issue
        return jsonify({"error": "YouTube Bot-Check active. Try a different video or refresh cookies."}), 403

app = app
