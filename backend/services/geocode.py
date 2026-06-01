import os
import requests
import logging

# Logger for this module
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
geocode_url = os.getenv("GOOGLE_GEOCODE_URL")


def get_coordinates(address):
    
    logger.info(f"Starting geocoding for address: {address}")

    # STEP 1: Validate config
    if not API_KEY:
        logger.error("Google API key is missing")
        raise Exception("Missing GOOGLE_MAPS_API_KEY")

    if not geocode_url:
        logger.error("Geocode URL is missing")
        raise Exception("Missing GOOGLE_GEOCODE_URL")

    logger.info(f"Using Geocode URL: {geocode_url}")

    try:
        # STEP 2: Call Google API
        response = requests.get(geocode_url, params={
            "address": address,
            "key": API_KEY
        })

        logger.info(f"Geocode API response status: {response.status_code}")

        data = response.json()

        logger.debug(f"Full geocode response: {data}")

        # STEP 3: Validate response
        if "results" not in data or len(data["results"]) == 0:
            logger.error(f"No geocoding results found for address: {address}")
            raise Exception("Invalid address or no results from Google Geocoding API")

        location = data["results"][0]["geometry"]["location"]

        coords = {
            "lat": location["lat"],
            "lng": location["lng"]
        }

        logger.info(f"Geocoding successful: {coords}")

        return coords

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed while calling Geocoding API: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Geocoding error: {str(e)}")
        raise