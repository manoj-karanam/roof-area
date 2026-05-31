import React, { useState } from "react";
import { GoogleMap, LoadScript, DrawingManager, StandaloneSearchBox } from "@react-google-maps/api";
import * as turf from "@turf/turf";


const libraries = ["drawing", "places"];
const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;

function RoofMap() {
  const [area, setArea] = useState(null);
  const [searchBox, setSearchBox] = useState(null);
  const [mapCenter, setMapCenter] = useState({
    // address
    lat:41.122792, lng:-85.107040
  });

  const onLoadSearchBox = (ref) => {
    setSearchBox(ref);
  };

  const onPlacesChanged = () => {
    if (!searchBox) return;

    const places = searchBox.getPlaces();

    if (places.length === 0) return;

    const location = places[0].geometry.location;

    setMapCenter({
      lat: location.lat(),
      lng: location.lng(),
    });
  };

  const onPolygonComplete = (polygon) => {
    console.log("Polygon completed");

    const path = polygon.getPath().getArray();

    console.log("Path:", path);

    const coords = path.map((point) => [
      point.lng(),
      point.lat(),
    ]);

    console.log("Coords before closing:", coords);

    // Close polygon
    coords.push(coords[0]);

    console.log("Closed coords:", coords);

    try {
      const turfPolygon = turf.polygon([coords]);
      const roofArea = turf.area(turfPolygon);

      console.log("Calculated area:", roofArea);

      setArea(roofArea);
    } catch (error) {
      console.error("Area calculation error:", error);
    }
  };

  return (
    <LoadScript
      googleMapsApiKey={apiKey}
      libraries={libraries}
    >
      <StandaloneSearchBox
        onLoad={onLoadSearchBox}
        onPlacesChanged={onPlacesChanged}
      >
        <input
          type="text"
          placeholder="Search address..."
          style={{
            boxSizing: "border-box",
            border: "1px solid transparent",
            width: "300px",
            height: "40px",
            padding: "0 12px",
            borderRadius: "4px",
            margin: "10px",
            fontSize: "16px",
          }}
        />
      </StandaloneSearchBox>
      <GoogleMap
        mapContainerStyle={{ width: "100%", height: "600px" }}
        zoom={20}
        center={ mapCenter}
        options={{ mapTypeId: "hybrid" }}
      >
        <DrawingManager
          onPolygonComplete={onPolygonComplete}
          options={{
            drawingControl: true,
            drawingModes: ["polygon"],
          }}
        />
      </GoogleMap>

      {area && (
        <h2>Roof Area: {area.toFixed(2)} m²</h2>
      )}
    </LoadScript>
  );
}

export default RoofMap;