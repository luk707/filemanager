export async function uploadFileToWorkspace(file: File, workspaceId: string) {
  const formData = new FormData();
  formData.append("files", file); // FastAPI expects a list, but can handle single uploads

  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_BASE_URL}/workspaces/${workspaceId}/upload`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    console.log("File uploaded successfully!");
  } catch (error) {
    console.error("Error uploading file:", error);
  }
}
