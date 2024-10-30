from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import ffmpeg
import os

app = Flask(__name__)

def download_video(url, format_code):
    options = {
        'format': format_code,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt'
    }
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
    return file_path

def convert_to_mp3(file_path, bitrate="320k"):
    mp3_path = os.path.splitext(file_path)[0] + ".mp3"
    ffmpeg.input(file_path).output(mp3_path, audio_bitrate=bitrate).run(overwrite_output=True)
    os.remove(file_path)  # Clean up the original file after conversion
    return mp3_path

@app.route('/')
def index():
    return render_template('vd.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form['quality']
    content_type = request.form['content_type']

    if content_type == 'audio':
        format_code = 'bestaudio/best'
        file_path = download_video(url, format_code)
        mp3_file_path = convert_to_mp3(file_path, bitrate=f"{quality}k")
        return send_file(mp3_file_path, as_attachment=True)

    elif content_type == 'video':
        format_map = {
            "720p": "bestvideo[height<=720]+bestaudio/best",
            "480p": "bestvideo[height<=480]+bestaudio/best",
            "360p": "bestvideo[height<=360]+bestaudio/best"
        }
        format_code = format_map.get(quality, "best")
        file_path = download_video(url, format_code)
        return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    app.run(debug=True)
