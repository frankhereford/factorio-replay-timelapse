import { api, HydrateClient } from "~/trpc/server";
import Map from "~/app/_components/map";

export default async function Home() {
  const hello = await api.post.hello({ text: "from tRPC" });

  void api.post.getLatest.prefetch();

  return (
    <HydrateClient>
      <main>
          <Map></Map>
     </main>
    </HydrateClient>
  );
}

