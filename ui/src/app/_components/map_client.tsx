'use client';

import { api } from "~/trpc/react";
import { useState, useEffect } from "react";
import LeafletMap from "~/app/_components/leaflet_map";
import TickPicker from "~/app/_components/tick_picker";
import SurfaceSelector from "~/app/_components/surface_selector";

interface MapClientProps {
  ticks: number[];
}

export default function MapClient({ ticks: initialTicks }: MapClientProps) {
  const [available, refetchAvailable] = api.tick.available.useSuspenseQuery();
  const [ticks, setTicks] = useState(initialTicks);
  const [tick, setTick] = useState(0);
  const [surface, setSurface] = useState('nauvis');

  const surfaces = ['nauvis', 'platform-1'];

  useEffect(() => {
    console.log("Ticks prop changed:", initialTicks);
    setTicks(initialTicks);
  }, [initialTicks]);

  useEffect(() => {
    console.log("available changed:", available);
    setTicks(available);
  }, [available]);

  useEffect(() => {
    const interval = setInterval(() => {
      refetchAvailable.refetch();
    }, 30000);

    return () => clearInterval(interval);
  }, [refetchAvailable]);

  return (
    <div className="relative h-screen">
      <LeafletMap tick={tick} surface={surface} />
      <TickPicker ticks={ticks} selectedTick={tick} onTickChange={setTick} />
      <SurfaceSelector selectedSurface={surface} onSurfaceChange={setSurface} surfaces={surfaces} />
    </div>
  );
}