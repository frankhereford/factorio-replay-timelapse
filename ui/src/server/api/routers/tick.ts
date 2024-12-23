import { z } from "zod";

import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";

export const tickRouter = createTRPCRouter({
  available: publicProcedure.query(() => {
    return [1, 2, 3];
  }),
});