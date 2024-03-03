from flask import Blueprint, jsonify, current_app
from flask_login import login_required
from .weather import get_pokemon_type_by_temperature
from http import HTTPStatus

import requests
import random

pokemon_bp = Blueprint('pokemon', __name__)

def make_http_request(resource, method):
    try:
        pokemon_api_base_url = current_app.config.get('POKEMON_API_BASE_URL')
        pokemon_url = f"{pokemon_api_base_url}{resource}"
        response = requests.request(method, pokemon_url)
        response_data = response.json() if response.status_code == 200 else None
        return {'data': response_data, 'status_code': response.status_code, 'error_message': ''}
    except Exception as e:
        return {'data': None, 'status_code': 500, 'error_message': str(e)}

@pokemon_bp.route('/app/pokemon/<name>', methods=['GET'])
@login_required
def get_pokemon_type_by_name(name):
    if not name:
        current_app.logger.warning('Pokemon name cannot be empty')
        return jsonify({'error': 'Pokemon name cannot be empty'}), 400

    resource = f"pokemon/{name}"
    method = "GET"
    response = make_http_request(resource, method)

    if response['error_message']:
        current_app.logger.error(f'Error retrieving pokemon type by name: {response["error_message"]}')
        return jsonify({'error': 'Internal Server Error'}), 500

    if response['data'] and 'types' in response['data']:
        pokemon_types = [type_obj['type']['name'] for type_obj in response['data']['types']]
        current_app.logger.info(f'Retrieved types for Pokemon {name}: {pokemon_types}')
        return jsonify({'types': pokemon_types}), response['status_code']
    else:
        current_app.logger.warning(f'Failed to retrieve types for Pokemon {name}')
        return jsonify({'message': HTTPStatus(int(response['status_code'])).phrase}), response['status_code']

@pokemon_bp.route('/app/pokemon/type/<type>', methods=['GET'])
@login_required
def get_random_pokemon_by_type(type):
    if not type:
        current_app.logger.warning('Pokemon type cannot be empty')
        return jsonify({'error': 'Pokemon type cannot be empty'}), 400

    resource = f"type/{type}"
    method = "GET"
    response = make_http_request(resource, method)

    if response['error_message']:
        current_app.logger.error(f'Error retrieving random pokemon by type: {response["error_message"]}')
        return jsonify({'error': 'Internal Server Error'}), 500

    pokemon_list = response['data'].get('pokemon', []) if response['data'] is not None else []
    if pokemon_list:
        random_pokemon = random.choice(pokemon_list)['pokemon']['name']
        current_app.logger.info(f'Retrieved random Pokemon {random_pokemon} by type {type}')
        return jsonify({'pokemon': random_pokemon}), response['status_code']
    else:
        current_app.logger.warning('No Pokemon found for the specified type')
        return jsonify({'message': 'No Pokemon found'}), response['status_code']

@pokemon_bp.route('/app/pokemon/long/<type>', methods=['GET'])
@login_required
def get_longest_name_pokemon_by_type(type):
    if not type:
        current_app.logger.warning('Pokemon type cannot be empty')
        return jsonify({'error': 'Pokemon type cannot be empty'}), 400

    resource = f"type/{type}"
    method = "GET"
    response = make_http_request(resource, method)

    if response['error_message']:
        current_app.logger.error(f'Error retrieving longest name pokemon by type: {response["error_message"]}')
        return jsonify({'error': 'Internal Server Error'}), 500

    pokemon_list = response['data'].get('pokemon', []) if response['data'] is not None else []
    if pokemon_list:
        longest_pokemon = max(pokemon_list, key=lambda x: len(x['pokemon']['name']))
        longest_pokemon_name = longest_pokemon['pokemon']['name']
        current_app.logger.info(f'Retrieved longest name Pokemon {longest_pokemon_name} by type {type}')
        return jsonify({'longest_pokemon': longest_pokemon_name}), response['status_code']
    else:
        return jsonify({'message': 'No Pokemon found'}), response['status_code']

@pokemon_bp.route('/app/pokemon/iam', methods=['GET'])
@login_required
def get_random_pokemon_by_weather():
    pokemon_type = get_pokemon_type_by_temperature()
    if not pokemon_type:
        current_app.logger.warning('Pokemon type cannot be empty')
        return jsonify({'error': 'Pokemon type cannot be empty'}), 400

    resource = f"type/{pokemon_type}"
    method = "GET"
    response = make_http_request(resource, method)

    if response['error_message']:
        current_app.logger.error(f'Error retrieving random pokemon by weather: {response["error_message"]}')
        return jsonify({'error': 'Internal Server Error'}), 500
    
    pokemon_list = response['data'].get('pokemon', []) if response['data'] is not None else []
    filtered_pokemon = [pokemon['pokemon'] for pokemon in pokemon_list if any(letter in pokemon['pokemon']['name'].lower() for letter in ['i', 'a', 'm'])]
    if filtered_pokemon:
        random_pokemon = random.choice(filtered_pokemon)['name']
        current_app.logger.info(f'Retrieved random Pokemon by weather: {random_pokemon}')
        return jsonify({'pokemon': random_pokemon}), response['status_code']
    else:
        current_app.logger.warning('No Pokemon found with "I", "A" or "M" in its name')
        return jsonify({'error': 'No Pokemon found with "I", "A" or "M" in its name'}), 404

def find_longest_pokemon(pokemon_list):
    longest_pokemon = None
    max_length = 0
    for pokemon in pokemon_list:
        pokemon_name = pokemon['pokemon']['name']
        if len(pokemon_name) > max_length:
            max_length = len(pokemon_name)
            longest_pokemon = pokemon_name
    return longest_pokemon