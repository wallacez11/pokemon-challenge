from flask import Blueprint, jsonify, current_app
from flask_login import login_required
from .weather import get_current_weather, get_lat_lng, get_pokemon_type_by_temperature
from http import HTTPStatus

import requests
import random


pokemon_bp = Blueprint('pokemon', __name__)

def make_http_request(resource, method):
    pokemon_api_base_url = current_app.config.get('POKEMON_API_BASE_URL')
    pokemon_url = f"{pokemon_api_base_url}{resource}"

    try:
        # Verifica o método HTTP e faz a chamada correspondente
        if method == 'GET':
            response = requests.get(pokemon_url)
        elif method == 'POST':
            response = requests.post(pokemon_url)
        elif method == 'PUT':
            response = requests.put(pokemon_url)
        elif method == 'DELETE':
            response = requests.delete(pokemon_url)
        else:
            return {
                'data': None,
                'status_code': None,
                'error_message': 'Invalid HTTP method'
            }

        # Monta o objeto de retorno com a resposta, o código de status e a mensagem de erro
        return {
            'data': response.json() if response.status_code == 200 else None,
            'status_code': response.status_code,
            'error_message': '' 
        }

    except Exception as e:
        # Monta o objeto de erro com a mensagem de exceção
        return {
            'data': [],
            'status_code':  [],
            'error_message': str(e)
        }  

@pokemon_bp.route('/app/pokemon/<name>', methods=['GET'])
@login_required
def get_pokemon_type_by_name(name):
    if not name:
        return jsonify({'error': 'Pokemon name cannot be empty'}), 400

    resource = f"pokemon/{name}"
    method = "GET"
    
    response = make_http_request(resource, method)

    if response['error_message']:
        return jsonify({'error': response['error_message']}), 500 

    if response['data'] and 'types' in response['data']:
        pokemon_types = [type_obj['type']['name'] for type_obj in response['data']['types']]
        return jsonify({'types': pokemon_types}), response['status_code']
    else:
        return jsonify({'message': HTTPStatus(int(response['status_code'])).phrase}), response['status_code']

@pokemon_bp.route('/app/pokemon/type/<type>', methods=['GET'])
@login_required
def get_random_pokemon_by_type(type):
    if not type:
        return jsonify({'error': 'Pokemon type cannot be empty'}), 400

    resource = f"type/{type}"
    method = "GET"
    
    response = make_http_request(resource, method)

    if response['error_message']:
        return jsonify({'error': response['error_message']}), 500 

    if  response['data'] and 'pokemon' in response['data']:
        pokemon_list = response['data']['pokemon']
        if pokemon_list:
            random_pokemon = random.choice(pokemon_list)
            pokemon_name = random_pokemon['pokemon']['name']
            return jsonify({'pokemon': pokemon_name}), response['status_code']
    else:
        return jsonify({'message': HTTPStatus(int(response['status_code'])).phrase}), response['status_code']


@pokemon_bp.route('/app/pokemon/long/<type>', methods=['GET'])
@login_required
def get_longest_name_pokemon_by_type(type):
    if not type:
        return jsonify({'error': 'Pokemon type cannot be empty'}), 400

    resource = f"type/{type}"
    method = "GET"
    
    response = make_http_request(resource, method)

    if response['error_message']:
        return jsonify({'error': response['error_message']}), 500 
    
    if response['data'] and 'pokemon' in response['data']:
        pokemon_list = response['data']['pokemon']
        if pokemon_list:
            longest_pokemon = find_longest_pokemon(pokemon_list)
            if longest_pokemon:
                return jsonify({'longest_pokemon': longest_pokemon}), response['status_code']
    
    return jsonify({'message': HTTPStatus(response['status_code']).phrase}), response['status_code']

@pokemon_bp.route('/app/pokemon/iam', methods=['GET'])
@login_required
def get_random_pokemon_by_weather():
    type = get_pokemon_type_by_temperature()
    if not type:
        return jsonify({'error': 'Pokemon type cannot be empty'}), 400

    resource = f"type/{type}"
    method = "GET"
    
    response = make_http_request(resource, method)

    if response['error_message']:
        return jsonify({'error': response['error_message']}), 500 
    
    if response['data'] and 'pokemon' in response['data']:
        pokemon_list = response['data']['pokemon']
        filtered_pokemon = [pokemon['pokemon'] for pokemon in pokemon_list if any(letter in pokemon['pokemon']['name'].lower() for letter in ['i', 'a', 'm'])]
        if filtered_pokemon:
            random_pokemon = random.choice(filtered_pokemon)
            return jsonify({'pokemon': random_pokemon}), response.get('status_code', 200)
    
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

