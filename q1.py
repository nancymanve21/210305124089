from flask import Flask, jsonify, request
import requests
from functools import lru_cache
from time import time

application = Flask(__name__)

THIRD_PARTY_URL = 'http://20.244.56.144/test/numbers'

CACHE_SIZE = 100
CACHE_EXPIRATION = 60  
@lru_cache(maxsize=CACHE_SIZE)
def fetch_numbers(number_id):
    try:
        start_time = time()
        response = requests.get(f'{THIRD_PARTY_URL}/{number_id}')
        end_time = time()

        if response.status_code == 200:
            data = response.json()
            numbers = data.get('numbers', [])
            unique_number = list(set(numbers))
            return unique_number, end_time - start_time 
            return [], 0
    except requests.exceptions.RequestException as e:
        print(f"Error fetching numbers: {e}")
        return [], 0

@application.route('/number/<string:numberid>', methods=['GET'])
def get_average(numberid):
    try:
        numbers, fetch_time = fetch_numbers(numberid)

        if numbers:
            average = sum(numbers) / len(numbers)
        else:
            average = 0

        return jsonify({
            'numbers': numbers,
            'average': average,
            'fetch_time': fetch_time
        })
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'An error occurred.'}), 500

if __name__ == '__main__':
    application.run(debug=True)
