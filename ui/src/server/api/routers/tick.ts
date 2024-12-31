// import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";
import fs from "fs";

export const tickRouter = createTRPCRouter({
  available: publicProcedure.query(() => {
    const rawScreenshotsDir = process.env.RAW_SCREENSHOTS;

    if (!rawScreenshotsDir) {
      throw new Error("RAW_SCREENSHOTS environment variable is not set");
    }

    const nauvisDir = `${rawScreenshotsDir}/nauvis`;

    const directories = fs.readdirSync(nauvisDir, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory() && /^\d+$/.test(dirent.name))
      .map(dirent => parseInt(dirent.name, 10))
      .filter(value => value % (60 * 60) === 0)
      .sort((a, b) => a - b);

    return directories;
  }),
});
