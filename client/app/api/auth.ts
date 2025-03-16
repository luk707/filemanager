import { z } from "zod";

export const TokenSchema = z.string();

const urls = {
  getToken: () => `${import.meta.env.VITE_API_BASE_URL}/auth/token`,
};

export async function getToken(username: string, password: string) {
  const response = await fetch(urls.getToken(), {
    headers: {
      Authorization: `Basic ${btoa(`${username}:${password}`)}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get token: ${response.statusText}`);
  }

  const data = await response.json();

  return TokenSchema.parse(data);
}
