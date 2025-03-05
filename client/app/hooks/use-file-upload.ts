import { useCallback } from "react";
import { uploadFileToWorkspace } from "~/api/upload";

export function useFileUpload(workspaceId: string) {
  const handleFileUpload = useCallback(async () => {
    try {
      // Open file picker
      const [fileHandle] = await (window as any).showOpenFilePicker();
      const file = await fileHandle.getFile();

      // Upload file
      await uploadFileToWorkspace(file, workspaceId);
    } catch (error) {
      console.error("File selection failed:", error);
    }
  }, [workspaceId]);

  return { handleFileUpload };
}
