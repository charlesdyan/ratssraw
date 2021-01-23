from flask import Flask
from flask import request
from flask_caching import Cache
import requests
import json

SWAPI_URL = 'https://swapi.dev/api/'
SWAPI_FILMS_EP = 'films/'

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 3600
}

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(config)
    cache = Cache(app)


    @app.route('/films')
    @cache.cached()
    def films():
        swapi_resp = requests.get(f'{SWAPI_URL}{SWAPI_FILMS_EP}')
        films = [parse_film(film) for film in swapi_resp.json()['results']]
        return json.dumps(films)


    @app.route('/characters', methods=['POST'])
    @cache.cached()
    def characters():
        film_id = request.get_json()['filmID']
        swapi_resp = requests.get(f'{SWAPI_URL}{SWAPI_FILMS_EP}{film_id}')
        character_urls = swapi_resp.json()['characters']
        char_resps = [requests.get(url) for url in character_urls]
        characters = [parse_char(resp.json()) for resp in char_resps]
        return json.dumps(characters)
    
    return app


def parse_film(film):
    return {
        'id': film['episode_id'],
        'title': film['title'],
        'release_date': film['release_date']}


def parse_char_id(url):
    url_parts = url.split('/')
    return url_parts[len(url_parts) - 2]


def parse_char(character):
    return {
        'id': parse_char_id(character['url']),
        'name': character['name']
    }