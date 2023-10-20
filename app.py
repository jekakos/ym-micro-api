import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from yandex_music import Client
import yandex_music.exceptions
import pprint

app = Flask(__name__)
load_dotenv()
yandex_music_token = os.getenv('YANDEX_MUSIC_TOKEN')

@app.route('/get_song_link', methods=['GET'])
def get_song_link():
    artist = request.args.get('artist')
    title = request.args.get('title')

    if not artist or not title:
        return jsonify({'error': 'Bad Request', 'message': 'Both artist and title are required'}), 400
    
    try:
      client = Client(yandex_music_token).init()
      search_result = client.search(f'{artist} {title}')
    except yandex_music.exceptions.YandexMusicError as e:
      return jsonify({'error': 'Yandex Music Error', 'message': str(e)}), 500
    
    if not search_result.tracks.results:
        return jsonify({'error': 'Not Found', 'message': 'No tracks found'}), 404
    
    first_track = search_result.tracks.results[0]

    #pprint.pprint(first_track)
    track_url = f"https://music.yandex.ru/track/{first_track['id']}"
    
    track_info = {
        'id': first_track['id'],
        'title': first_track['title'],
        'artist': first_track['artists'][0]['name'] if first_track['artists'] else None,
        'album': first_track['albums'][0]['title'] if first_track['albums'] else None,
        'track_url': track_url
    }

    return jsonify(track_info)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)