'use client';

import { useState, useEffect } from "react";
import LeafletMap from "~/app/_components/leaflet_map";

interface MapClientProps {
  ticks: number[];
}

export default function MapClient({ ticks }: MapClientProps) {
  const [tick, setTick] = useState(60000);

useEffect(() => {
    console.log("Ticks prop changed:", ticks);
  }, [ticks]);

  return (
    <>
      <LeafletMap tick={tick}></LeafletMap>
    </>
  );
}