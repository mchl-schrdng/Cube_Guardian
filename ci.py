from loguru import logger
import requests
import os
import time
import json

logger.remove()
logger.add(lambda msg: print(msg), format="{message}")

session = requests.Session()

def get_cube_metadata(api_url, api_token):
    session.headers.update({'Authorization': f'Bearer {api_token}'})
    response = session.get(f"{api_url}/meta")
    response.raise_for_status()
    return response.json()

def test_cube(api_url, cube_details):
    query = {
        "measures": cube_details.get("measures", []),
        "dimensions": cube_details.get("dimensions", []),
        "limit": 1
    }
    response = session.post(f"{api_url}/load", json={'query': query})
    if response.status_code != 200:
        error_json = response.json()
        error_message = error_json.get('error', 'Unknown error')
        raise requests.HTTPError(f"Error in cube {cube_details['name']}: {error_message}")

def test_dimension(api_url, cube_name, dimension, measure):
    query = {
        "measures": [measure],
        "dimensions": [dimension],
        "limit": 1
    }
    response = session.post(f"{api_url}/load", json={'query': query})
    if response.status_code != 200:
        error_json = response.json()
        return f"cube {cube_name}: Error in cube {cube_name}: {error_json.get('error', 'Unknown error')}"
    return None

def run_tests(api_url, api_token):
    start_time = time.time()
    metadata = get_cube_metadata(api_url, api_token)
    all_cubes_status = {}

    for cube in metadata['cubes']:
        cube_name = cube['name']
        measures = [m['name'] for m in cube.get('measures', [])]
        dimensions = [d['name'] for d in cube.get('dimensions', [])]
        try:
            test_cube(api_url, {'name': cube_name, 'measures': measures, 'dimensions': dimensions})
            all_cubes_status[cube_name] = 'passed'
        except requests.HTTPError:
            all_cubes_status[cube_name] = 'failed'
            # Test each dimension individually
            for dimension in dimensions:
                error_message = test_dimension(api_url, cube_name, dimension, measures[0] if measures else "")
                if error_message:
                    logger.error(error_message)

    logger.info("=" * 100)
    logger.info("Cube Status Summary")
    logger.info("=" * 100)
    for cube_name, status in all_cubes_status.items():
        logger.info(f"Cube {cube_name}: {status}")

    duration = time.time() - start_time
    logger.info("=" * 100)
    logger.info(f"Completed cube validation in {duration:.2f} seconds.")

if __name__ == "__main__":
    API_URL = os.getenv("API_URL")
    API_TOKEN = os.getenv("API_TOKEN")
    if not API_URL or not API_TOKEN:
        raise EnvironmentError("API_URL and API_TOKEN must be set as environment variables.")
    run_tests(API_URL, API_TOKEN)
