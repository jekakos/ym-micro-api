import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from yandex_music.utils.request import Request
from yandex_music import Client
import yandex_music.exceptions
import pprint

app = Flask(__name__)
load_dotenv()
yandex_music_token = os.getenv('YANDEX_MUSIC_TOKEN')
proxy_user = os.getenv('PROXY_USER')
proxy_password = os.getenv('PROXY_PASSWORD')
proxy_ip = os.getenv('PROXY_IP')
proxy_port = os.getenv('PROXY_PORT')
proxy_url = 'socks5://' + proxy_user + ':' + \
    proxy_password + '@' + proxy_ip + ':' + proxy_port

yandex_request = Request(proxy_url=proxy_url)
client = Client(token=yandex_music_token, request=yandex_request).init()


@app.route('/get_track_info', methods=['GET'])
def get_track_info():
    trackId = request.args.get('trackId')

    if not trackId:
        return jsonify({'error': 'Bad Request', 'message': 'trackId are required'}), 400

    try:
        search_result = client.tracks(f'{trackId}')
    except yandex_music.exceptions.YandexMusicError as e:
        return jsonify({'error': 'Yandex Music Error', 'message': str(e)}), 500

    # pprint.pprint(search_result)
    if not search_result:
        return jsonify({'error': 'Not Found', 'message': 'No tracks found'}), 404

    track = search_result[0]
    track_url = f"https://music.yandex.ru/track/{track['id']}"

    track_info = {
        'id': track['id'],
        'title': track['title'],
        'artist': track['artists'][0]['name'] if track['artists'] else None,
        'album': track['albums'][0]['title'] if track['albums'] else None,
        'track_url': track_url
    }

    return jsonify(track_info)


@app.route('/get_track_link', methods=['GET'])
def get_track_link():
    artist = request.args.get('artist')
    title = request.args.get('title')

    if not artist or not title:
        return jsonify({'error': 'Bad Request', 'message': 'Both artist and title are required'}), 400

    try:
        search_result = client.search(f'{artist} {title}')
    except yandex_music.exceptions.YandexMusicError as e:
        return jsonify({'error': 'Yandex Music Error', 'message': str(e)}), 500

    if not search_result or not search_result.tracks.results:
        return jsonify({'error': 'Not Found', 'message': 'No tracks found'}), 404

    first_track = search_result.tracks.results[0]

    # pprint.pprint(first_track)
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
    app.run(host='0.0.0.0', port=5050, debug=True)
