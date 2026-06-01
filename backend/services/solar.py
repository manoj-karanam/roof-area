import os
import requests
import logging
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
solar_api_url = os.getenv("GOOGLE_SOLAR_API_URL")


def get_roof_data(lat, lng):
    logger.info(f"Starting Solar API call for lat={lat}, lng={lng}")

    # STEP 1: Validate config
    if not API_KEY:
        logger.error("Missing GOOGLE_API_KEY")
        raise Exception("Missing GOOGLE_API_KEY")

    if not solar_api_url:
        logger.error("Missing GOOGLE_SOLAR_API_URL")
        raise Exception("Missing GOOGLE_SOLAR_API_URL")

    try:
        logger.info(f"Calling Solar API: {solar_api_url}")

        response = requests.get(
            solar_api_url,
            params={
                "location.latitude": lat,
                "location.longitude": lng,
                "key": API_KEY
            }
        )

        logger.info(f"Solar API status code: {response.status_code}")

        data = response.json()

        logger.debug(f"Full Solar API response: {data}")

        # STEP 2: Validate response
        if "error" in data:
            logger.error(f"Solar API error response: {data['error']}")
            raise Exception(f"Solar API error: {data['error']}")

        logger.info("Solar API call successful")

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed to Solar API: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Solar API processing error: {str(e)}")
        raise