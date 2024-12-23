import Link from "next/link";

import 'leaflet/dist/leaflet.css';

// import { LatestPost } from "~/app/_components/post";
import { api, HydrateClient } from "~/trpc/server";

export default async function Home() {
  // const hello = await api.post.hello({ text: "from tRPC" });
  // void api.post.getLatest.prefetch();

  return (
    <HydrateClient>
      <main>
        <div id="map" className="h-full h-screen border-indigo-700 bg-indigo-100">
        </div>
      </main>
    </HydrateClient>
  );
}
