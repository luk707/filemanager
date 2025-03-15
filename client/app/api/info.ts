import { z } from "zod";

export const InfoSchema = z.object({
  organizationName: z.string(),
});

const urls = {
  getInfo: () => `${import.meta.env.VITE_API_BASE_URL}/info`,
};

export async function getInfo() {
  const response = await fetch(urls.getInfo());

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  const data = await response.json();

  return InfoSchema.parse(data);
}
