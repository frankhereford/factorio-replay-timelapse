import { api, HydrateClient } from "~/trpc/server";
import MapClient from "~/app/_components/map_client";

export default async function MapServer() {
  const ticks = await api.tick.available();
  void api.tick.available.prefetch();

  return (
    <>
      <HydrateClient>
        <MapClient ticks={ticks} />;
      </HydrateClient>
    </>
  );
}