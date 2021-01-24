from flask import Flask
from flask import request
from flask import jsonify
from flask_caching import Cache
from ratssraw.errors import GenericError
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
        raise_on_swapi_error(swapi_resp)
        films = [parse_film(film) for film in swapi_resp.json()['results']]
        return json.dumps(films)


    @app.route('/characters', methods=['POST'])
    @cache.cached()
    def characters():
        post_json = request.get_json()
        if 'filmID' in post_json:
            film_id = request.get_json()['filmID']
            swapi_resp = requests.get(f'{SWAPI_URL}{SWAPI_FILMS_EP}{film_id}')
            raise_on_swapi_error(swapi_resp)
            character_urls = swapi_resp.json()['characters']
            char_resps = [requests.get(url) for url in character_urls]
            [raise_on_swapi_error(resp) for resp in char_resps]
            characters = [parse_char(resp.json()) for resp in char_resps]
            return json.dumps(characters)
        else:
            raise GenericError('json payload must follow format {"filmID": <int>}')
    

    @app.errorhandler(GenericError)
    def handleError(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


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


def raise_on_swapi_error(swapi_resp):
    if swapi_resp.status_code != 200:
        raise GenericError('Something went wrong between us and SWAPI', status_code=500)