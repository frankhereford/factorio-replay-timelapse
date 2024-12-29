'use client';

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface LeafletMapProps {
  tick: number;
}

export default function LeafletMap({ tick }: LeafletMapProps) {
  const mapRef = useRef<L.Map | null>(null);

  let surface = 'nauvis'

  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = L.map("map", {
        center: L.latLng(0, 0),
        zoom: 6,
      });

      L.tileLayer(
        `http://fjord:8123/stills/${surface}/${tick}/{z}/{x}/{y}.png`,
        {
          tileSize: 256,
          minZoom: 1,
          maxZoom: 10,
          crossOrigin: true,
        }
      ).addTo(mapRef.current);
    } else {
      mapRef.current.eachLayer((layer) => {
        if (layer instanceof L.TileLayer) {
          layer.setUrl(`http://fjord:8123/stills/${surface}/${tick}/{z}/{x}/{y}.png`);
        }
      });
    }
  }, [tick]);

  return <div id="map" className="h-full h-screen border-indigo-700 bg-indigo-100 z-0"></div>;
}