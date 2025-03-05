import { z } from "zod";

// Define Zod schema
const FileSchema = z.object({
  name: z.string(),
  contentType: z.string().nullable(),
  size: z.number(),
  lastModified: z.string(),
});

// Define TypeScript type from Zod schema
export type File = z.infer<typeof FileSchema>;

// Define an array schema for validation
const FileArraySchema = z.array(FileSchema);

export async function getFiles(): Promise<File[]> {
  const response = await fetch("http://127.0.0.1:8000/workspace/files");

  if (!response.ok) {
    throw new Error(`Failed to fetch files: ${response.statusText}`);
  }

  const data = await response.json();

  return FileArraySchema.parse(data); // Validate and return parsed data
}
