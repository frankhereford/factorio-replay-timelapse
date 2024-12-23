'use client';

import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface LeafletMapProps {
  tick: number;
}

export default function LeafletMap({ tick }: LeafletMapProps) {
  useEffect(() => {
    const map = L.map("map", {
      center: L.latLng(0, 0),
      zoom: 6,
    });

    L.tileLayer(
      `http://fjord:8123/stills/${tick}/{z}/{x}/{y}.png`,
      {
        tileSize: 256,
        // zoomOffset: -1,
        minZoom: 1,
        maxZoom: 10,
        crossOrigin: true,
      }
    ).addTo(map);
  }, [tick]);

  return <div id="map" className="h-full h-screen border-indigo-700 bg-indigo-100"></div>;
};