import { z } from "zod";

// Define Zod schema
const FileSchema = z.object({
  name: z.string(),
  contentType: z.string(),
  size: z.number(),
  lastModified: z.string(),
});

const urls = {
  getFiles: (workspaceId: string, path?: string) =>
    path
      ? `${
          import.meta.env.VITE_API_BASE_URL
        }/workspaces/${workspaceId}/stat/${path}`
      : `${import.meta.env.VITE_API_BASE_URL}/workspaces/${workspaceId}/stat`,
  removeFile: (workspaceId: string, path: string) =>
    `${
      import.meta.env.VITE_API_BASE_URL
    }/workspaces/${workspaceId}/remove/${path}`,
  downloadFile: (workspaceId: string, path: string) =>
    `${
      import.meta.env.VITE_API_BASE_URL
    }/workspaces/${workspaceId}/download/${path}`,
  uploadFile: (workspaceId: string) =>
    `${import.meta.env.VITE_API_BASE_URL}/workspaces/${workspaceId}/upload`,
};

export async function getFiles(workspaceId: string, path?: string) {
  const response = await fetch(urls.getFiles(workspaceId, path));

  if (!response.ok) {
    throw new Error(`Failed to fetch files: ${response.statusText}`);
  }

  const data = await response.json();

  return z.array(FileSchema).parse(data); // Validate and return parsed data
}

export async function removeFile(workspaceId: string, path: string) {
  const response = await fetch(urls.removeFile(workspaceId, path), {
    method: "delete",
  });

  if (!response.ok) {
    throw new Error(`Failed to delete ${path}: ${response.statusText}`);
  }
}

export function downloadFile(workspaceId: string, path: string) {
  return fetch(urls.downloadFile(workspaceId, path))
    .then((response) => response.blob())
    .then((blob) => {
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      // TODO: When we implement multiple folders, we will need a way to
      // know the basename of the file, and its path
      link.download = path;
      link.click();
    })
    .catch(console.error);
}

export async function uploadFileToWorkspace(file: File, workspaceId: string) {
  const formData = new FormData();
  formData.append("files", file); // FastAPI expects a list, but can handle single uploads

  try {
    const response = await fetch(urls.uploadFile(workspaceId), {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    console.log("File uploaded successfully!");
  } catch (error) {
    console.error("Error uploading file:", error);
  }
}
