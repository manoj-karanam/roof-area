from fastapi import FastAPI
from services.geocode import get_coordinates
from services.solar import get_roof_data
import logging, os  
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Handling CORS issue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def analyze(lat: float, lng: float, address: str = None):
    
    if address is None or lat is None or lng is None:
        logger.error("Missing required parameters")
        return {"error": "address, lat, lng are required"}

    logger.info( f"Address: {address}")
    logger.info(f"Received Successfully: Latitude={lat}, Longitude={lng}")

    logger.info("Sending coordinates to Solar API")
    logger.info(f"Requesting roof data for coordinates: {lat}, {lng}")

    roof = get_roof_data(lat, lng)

    if not roof:
        logger.error("Solar API failed or returned empty response")
        return {"error": "Solar API failed"}

    logger.info("Solar API response received successfully")
    logger.info("Returning roof + coordinate data to frontend")

    return {
        "address": address,
        "latitude": lat,
        "longitude": lng,
        "roof_data": roof
    }