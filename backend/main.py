from fastapi import FastAPI
from services.geocode import get_coordinates
from services.solar import get_roof_data
import logging, os  
app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@app.get("/")
def root():
    logger.info("Health check hit - root endpoint accessed")
    return {"status": "working"}


@app.get("/analyze")
def analyze(address: str):

    logger.info(f"Received address: {address}")

    # STEP 1: Geocoding
    logger.info("Step 1: Converting address to coordinates using Geocoding API")
    coords = get_coordinates(address)

    if not coords:
        logger.error("Geocoding failed - no coordinates returned")
        return {"error": "Invalid address or geocoding failed"}

    logger.info(
        f"Geocoding successful: lat={coords['lat']}, lng={coords['lng']}"
    )

    # STEP 2: Solar API
    logger.info("Step 2: Sending coordinates to Solar API")
    logger.info(f"Requesting roof data for: {coords}")

    roof = get_roof_data(coords["lat"], coords["lng"])

    if not roof:
        logger.error("Solar API failed or returned empty response")
        return {"error": "Solar API failed"}

    logger.info("Solar API response received successfully")

    # STEP 3: Response
    logger.info("Returning roof + coordinate data to frontend")

    return {
        "coordinates": coords,
        "roof_data": roof
    }