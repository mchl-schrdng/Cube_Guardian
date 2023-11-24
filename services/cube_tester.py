import requests
import time
import logging
from datetime import datetime
from db.db_init_tester import init_db, add_test_result

# Set up basic configuration for logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Session for efficient networking
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
    response = session.post(f"{api_url}/load", json={"query": query})
    if response.status_code != 200:
        error_json = response.json()
        raise requests.HTTPError(f"Error in cube {cube_details['name']}: {error_json.get('error', 'Unknown error')}")

def test_dimension(api_url, cube_name, dimension, measure):
    query = {
        "measures": [measure],
        "dimensions": [dimension],
        "limit": 1
    }
    response = session.post(f"{api_url}/load", json={"query": query})
    if response.status_code != 200:
        error_json = response.json()
        return f"Dimension '{dimension}' in cube '{cube_name}' failed: {error_json.get('error', 'Unknown error')}"

def run_tests(api_url, api_token):
    # Initialize the database
    init_db()

    start_time = time.time()
    metadata = get_cube_metadata(api_url, api_token)
    overall_status = 'passed'  # Initialize to 'passed'
    check_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for cube in metadata['cubes']:
        cube_name = cube['name']
        measures = [m['name'] for m in cube.get('measures', [])]
        dimensions = [d['name'] for d in cube.get('dimensions', [])]

        cube_failed = False
        try:
            test_cube(api_url, {'name': cube_name, 'measures': measures, 'dimensions': dimensions})
            add_test_result('cube_status', (check_date, cube_name, 'passed'))  # Update cube status to passed
            logging.info(f"Cube {cube_name} passed.")
        except requests.HTTPError as e:
            cube_failed = True
            overall_status = 'failed'
            add_test_result('cube_status', (check_date, cube_name, 'failed'))  # Update cube status to failed
            logging.error(f"Cube {cube_name} failed: {e}")

        if cube_failed:
            for dimension in dimensions:
                error_message = test_dimension(api_url, cube_name, dimension, measures[0] if measures else "")
                if error_message:
                    add_test_result('dimension_status', (check_date, cube_name, dimension, 'failed', error_message))
                    logging.error(error_message)

    duration = time.time() - start_time
    add_test_result('overall_status', (check_date, overall_status))

    logging.info("=" * 100)
    logging.info(f"Completed cube validation in {duration:.2f} seconds.")

if __name__ == "__main__":
    API_URL = st.secrets["custom"]["api_url"]
    API_TOKEN = st.secrets["custom"]["api_token"]
    if not API_URL or not API_TOKEN:
        raise EnvironmentError("API_URL and API_TOKEN must be set as environment variables.")
    run_tests(API_URL, API_TOKEN)
