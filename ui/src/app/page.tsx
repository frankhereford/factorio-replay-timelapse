import Link from "next/link";

import { LatestPost } from "~/app/_components/post";
import { api, HydrateClient } from "~/trpc/server";
import Map from "~/app/_components/map";

export default async function Home() {
  const hello = await api.post.hello({ text: "from tRPC" });

  void api.post.getLatest.prefetch();

  return (
    <HydrateClient>
      <main className="">
        <div className="h-full h-screen border-indigo-700 bg-indigo-100">
          <Map></Map>
          {/* <div className="flex flex-col items-center gap-2">
            <p className="text-2xl text-white">
              {hello ? hello.greeting : "Loading tRPC query..."}
            </p>
          </div> */}
          {/* <LatestPost /> */}
        </div>
      </main>
    </HydrateClient>
  );
}


//   return (
//     <HydrateClient>
//       <main>
//         <div id="map" className="h-full h-screen border-indigo-700 bg-indigo-100">
//         </div>
//       </main>
//     </HydrateClient>
//   );
// }
