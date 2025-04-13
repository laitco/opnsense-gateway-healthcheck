import os
import requests
from flask import Flask, jsonify
import logging
from requests.auth import HTTPBasicAuth
from flask import request
import urllib3

# Disable SSL warnings for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.url_map.strict_slashes = False  # Allow trailing slashes to be ignored

# Load configuration from environment variables
API_KEY = os.getenv("API_KEY", "your-api-key")
API_SECRET = os.getenv("API_SECRET", "your-api-secret")
OPNSENSE_BASE_URL = os.getenv("OPNSENSE_BASE_URL", "https://opnsense.example.com")
OPNSENSE_PORT = int(os.getenv("OPNSENSE_PORT", 443))  # Default to port 443
PORT = int(os.getenv("PORT", 5000))  # Default to port 5000

# Remove unnecessary routes and focus only on the gateway API route
API_ROUTE_MAPPING = {
    "gateway": f"{OPNSENSE_BASE_URL}/api/routes/gateway/status" if OPNSENSE_PORT == 443 else f"{OPNSENSE_BASE_URL}:{OPNSENSE_PORT}/api/routes/gateway/status"
}

def verify_auth_on_init():
    """
    Verify that authentication is working when the application initializes.
    """
    logging.info("Verifying authentication on application initialization...")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        logging.error("Authentication failed: API_KEY or API_SECRET is missing.")
        raise RuntimeError("Authentication failed: Missing API_KEY or API_SECRET.")

    # Test authentication by making a request to the gateway API
    try:
        api_url = API_ROUTE_MAPPING["gateway"]
        auth = (api_key, api_secret)
        response = requests.get(api_url, auth=auth, verify=False)
        response.raise_for_status()
        logging.info("Authentication verified successfully on initialization.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Authentication verification failed: {e}")
        raise RuntimeError("Authentication verification failed.")

# Call the authentication verification function during app initialization
verify_auth_on_init()

@app.route('/health', methods=['GET'])
def health_check():
    try:
        api_url = API_ROUTE_MAPPING["gateway"]
        auth = (API_KEY, API_SECRET)
        response = requests.get(api_url, auth=auth, verify=False)
        response.raise_for_status()
        data = response.json()

        # Add 'healthy' field based on 'status_translated'
        for item in data.get('items', []):
            item['healthy'] = item['status_translated'] == 'Online'

        return jsonify(data)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for gateway: {e}")
        return jsonify({"error": "Failed to fetch data for gateway"}), 500

@app.route('/health/<name>', methods=['GET'])
def health_check_by_name(name):
    try:
        api_url = API_ROUTE_MAPPING["gateway"]
        auth = (API_KEY, API_SECRET)
        response = requests.get(api_url, auth=auth, verify=False)
        response.raise_for_status()
        data = response.json()

        # Filter by name (case-insensitive)
        filtered = [item for item in data.get('items', []) if item['name'].lower() == name.lower()]
        if not filtered:
            return jsonify({"error": "No entry found for the given name"}), 404

        # Add 'healthy' field based on 'status_translated'
        filtered[0]['healthy'] = filtered[0]['status_translated'] == 'Online'

        return jsonify(filtered[0])

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for gateway: {e}")
        return jsonify({"error": "Failed to fetch data for gateway"}), 500

@app.route('/health/<address>', methods=['GET'])
def health_check_by_address(address):
    try:
        api_url = API_ROUTE_MAPPING["gateway"]
        auth = (API_KEY, API_SECRET)
        response = requests.get(api_url, auth=auth, verify=False)
        response.raise_for_status()
        data = response.json()

        # Filter by address
        filtered = [item for item in data.get('items', []) if item['address'] == address]
        if not filtered:
            return jsonify({"error": "No entry found for the given address"}), 404

        # Add 'healthy' field based on 'status_translated'
        filtered[0]['healthy'] = filtered[0]['status_translated'] == 'Online'

        return jsonify(filtered[0])

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for gateway: {e}")
        return jsonify({"error": "Failed to fetch data for gateway"}), 500

@app.route('/health/unhealthy', methods=['GET'])
def health_check_unhealthy():
    try:
        api_url = API_ROUTE_MAPPING["gateway"]
        auth = (API_KEY, API_SECRET)
        response = requests.get(api_url, auth=auth, verify=False)
        response.raise_for_status()
        data = response.json()

        # Filter items where healthy is False
        for item in data.get('items', []):
            item['healthy'] = item['status_translated'] == 'Online'
        unhealthy_items = [item for item in data.get('items', []) if not item['healthy']]

        return jsonify(unhealthy_items)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for gateway: {e}")
        return jsonify({"error": "Failed to fetch data for gateway"}), 500

@app.route('/health/healthy', methods=['GET'])
def health_check_healthy():
    try:
        api_url = API_ROUTE_MAPPING["gateway"]
        auth = (API_KEY, API_SECRET)
        response = requests.get(api_url, auth=auth, verify=False)
        response.raise_for_status()
        data = response.json()

        # Filter items where healthy is True
        for item in data.get('items', []):
            item['healthy'] = item['status_translated'] == 'Online'
        healthy_items = [item for item in data.get('items', []) if item['healthy']]

        return jsonify(healthy_items)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for gateway: {e}")
        return jsonify({"error": "Failed to fetch data for gateway"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)