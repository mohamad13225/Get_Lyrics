from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import requests
import json
import os
import googleapi

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Directory for saving lyrics files
LYRICS_DIR = 'lrc'

def get_synced_lyrics(artist_name, track_name):
    url = f"https://lrclib.net/api/get?artist_name={artist_name}&track_name={track_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        song_name = data.get('name')
        artist = data.get('artistName')
        synced_lyrics = data.get('syncedLyrics')
        album_name = data.get('albumName')
        
        # Save synced lyrics to a .lrc file
        filename = f"{artist_name}_{track_name}.lrc"  # Changed to .lrc
        file_path = os.path.join(LYRICS_DIR, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"[ar:{artist}]\n")
            file.write(f"[ti:{song_name}]\n")
            file.write(f"[al: {album_name}]\n\n")

            file.write(synced_lyrics)

        return {
            'song_name': song_name,
            'artist': artist,
            'synced_lyrics': synced_lyrics,
            'file_path': file_path
        }
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except json.JSONDecodeError:
        print("Failed to parse the JSON response.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist = request.form.get('artist').strip()
        title = request.form.get('title').strip()
        
        if not artist or not title:
            flash('Please enter both artist and music title.', 'error')
            return redirect(url_for('index'))
        
        # Process input for API request
        process_artist = artist.replace(" ", "+")
        process_title = title.replace(" ", "+")

        lyrics_info = get_synced_lyrics(process_artist, process_title)
        
        if lyrics_info:
            flash('Synced lyrics retrieved successfully!', 'success')
            return render_template('index.html', lyrics=lyrics_info)

        flash('Could not retrieve lyrics. Please check the artist and title.', 'error')
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(LYRICS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    # Create lrc directory if it doesn't exist
    os.makedirs(LYRICS_DIR, exist_ok=True)
    app.run(debug=True)
