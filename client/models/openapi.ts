import { z } from "zod";

export const OpenAPISchema = z.object({
  openapi: z.string(),
  info: z.object({
    title: z.string(),
    version: z.string(),
  }),
});
