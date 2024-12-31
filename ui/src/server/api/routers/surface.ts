// import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";
import fs from "fs";

export const surfaceRouter = createTRPCRouter({
  surfaces: publicProcedure.query(() => {
    const rawScreenshotsDir = process.env.RAW_SCREENSHOTS;

    if (!rawScreenshotsDir) {
      throw new Error("RAW_SCREENSHOTS environment variable is not set");
    }

    const surfaces = fs.readdirSync(rawScreenshotsDir, { withFileTypes: true })
          .filter(dirent => dirent.isDirectory() && /^\d+$/.test(dirent.name))
          .map(dirent => dirent.name)
          .sort((a, b) => parseInt(a, 10) - parseInt(b, 10));
    
        return surfaces;
  }),
});
