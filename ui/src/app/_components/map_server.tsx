import { api } from "~/trpc/server";
import MapClient from "~/app/_components/map_client";

export default async function MapServer() {
  const ticks = await api.tick.available();
  return <MapClient ticks={ticks} />;
}