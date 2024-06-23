from flask import Flask, request, jsonify
from pytube import YouTube
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_download_links', methods=['POST'])
def get_download_links():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        yt = YouTube(url)
        
        video_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        audio_streams = yt.streams.filter(only_audio=True)
        
        video_links = [{'resolution': stream.resolution, 'url': stream.url} for stream in video_streams]
        audio_links = [{'abr': stream.abr, 'url': stream.url} for stream in audio_streams]

        return jsonify({'video_links': video_links, 'audio_links': audio_links})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
