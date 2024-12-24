'use client';

import { api } from "~/trpc/react";
import { useState, useEffect } from "react";
import LeafletMap from "~/app/_components/leaflet_map";
import TickPicker from "~/app/_components/tick_picker";

interface MapClientProps {
  ticks: number[];
}

export default function MapClient({ ticks: initialTicks }: MapClientProps) {
  const [available, refetchAvailable] = api.tick.available.useSuspenseQuery();
  const [ticks, setTicks] = useState(initialTicks);
  const [tick, setTick] = useState(0);

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
    <>
      <LeafletMap tick={tick}></LeafletMap>
      <TickPicker ticks={ticks} selectedTick={tick} onTickChange={setTick} />
    </>
  );
}