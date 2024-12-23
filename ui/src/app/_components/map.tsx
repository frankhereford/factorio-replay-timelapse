'use client';

import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default function Map() {
  useEffect(() => {
    const map = L.map("map", {
      center: L.latLng(0, 0),
      zoom: 6,
    });

    L.tileLayer(
      `http://fjord:8123/stills/0/{z}/{x}/{y}.png`,
      {
        tileSize: 256,
        // zoomOffset: -1,
        minZoom: 1,
        maxZoom: 10,
        crossOrigin: true,
      }
    ).addTo(map);
  }, []);

  return <div id="map" className="h-full h-screen border-indigo-700 bg-indigo-100"></div>;
};
