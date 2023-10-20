# Yandex Music Search Micro-API

## Packeges

- [Flask](https://flask.palletsprojects.com/): Used to create and run a web server and process HTTP requests.
- [python-dotenv](https://pypi.org/project/python-dotenv/): Used to load environment variables from a `.env` file.
- [yandex-music](https://yandex-music.readthedocs.io/en/latest/): Used to interact with the Yandex Music API.

## Setup

```bash
pip install Flask python-dotenv yandex-music
```

## How to get token

https://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-5272680

## Usage

```http
GET http://127.0.0.1:5050/get_song_link?artist=[Artist Name]&title=[Song Title]
```
