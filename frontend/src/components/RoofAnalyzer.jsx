import React, { useState } from "react";
import {
  LoadScript,
  Autocomplete,
  GoogleMap,
  Marker,
} from "@react-google-maps/api";

import "../styles/RoofAnalyzer.css";

export default function RoofAnalyzer() {
  const [result, setResult] = useState(null);
  const [autocomplete, setAutocomplete] = useState(null);
  const [map, setMap] = useState(null);

  const [position, setPosition] = useState({
    lat: 41.8781,
    lng: -87.6298,
  });

  const [address, setAddress] = useState("");

  const APP_BASE_URL = process.env.REACT_APP_API_URL;

  const onPlaceChanged = () => {
    if (!autocomplete) return;

    const place = autocomplete.getPlace();
    if (!place.geometry) return;

    const lat = place.geometry.location.lat();
    const lng = place.geometry.location.lng();
    const formattedAddress = place.formatted_address;

    setPosition({ lat, lng });
    setAddress(formattedAddress);

    // move map
    if (map) {
      map.panTo({ lat, lng });
      map.setZoom(20);
    }
  };

  return (
    <LoadScript
      googleMapsApiKey={process.env.REACT_APP_GOOGLE_MAPS_KEY}
      libraries={["places"]}
    >
      <div className="roof-container">
        <h1>Roof Analyzer</h1>

        <Autocomplete
          onLoad={setAutocomplete}
          onPlaceChanged={onPlaceChanged}
        >
          <input
            type="text"
            placeholder="Search address"
            className="search-box"
          />
        </Autocomplete>

        {/* show selected address */}
        {address && <p>{address}</p>}

        <GoogleMap
          mapContainerStyle={{
            width: "100%",
            height: "500px",
            marginTop: "10px",
          }}
          center={position}
          zoom={18}
          onLoad={setMap}
          onClick={(e) =>
            setPosition({
              lat: e.latLng.lat(),
              lng: e.latLng.lng(),
            })
          }
        >
          <Marker position={position} />
        </GoogleMap>

        <button
          onClick={() => {
            fetch(
              `${APP_BASE_URL}/analyze?lat=${position.lat}&lng=${position.lng}&address=${encodeURIComponent(address)}`
            )
              .then((res) => res.json())
              .then(setResult);
          }}
          className="button"
        >
          Analyze Roof
        </button>

        {result && (
          <pre className="result-box">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </LoadScript>
  );
}