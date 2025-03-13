import { z } from "zod";

export const UserSchema = z.object({
  id: z.string(),
  createdAt: z.string().nullable(),
  name: z.string().nullable(),
  avatarUrl: z.string().nullable(),
});

const urls = {
  getUsers: () => `${import.meta.env.VITE_API_BASE_URL}/users`,
};

export async function getUsers() {
  const response = await fetch(urls.getUsers());

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  const data = await response.json();

  return z.array(UserSchema).parse(data);
}
