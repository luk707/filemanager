import { useCallback } from "react";
import { useNavigate } from "react-router";
import { uploadFileToWorkspace } from "~/api/upload";

export function useFileUpload(workspaceId: string) {
  const navigate = useNavigate();
  const handleFileUpload = useCallback(async () => {
    try {
      // Open file picker
      const [fileHandle] = await (window as any).showOpenFilePicker();
      const file = await fileHandle.getFile();

      // Upload file
      await uploadFileToWorkspace(file, workspaceId);
      navigate(".", { replace: true });
    } catch (error) {
      console.error("File selection failed:", error);
    }
  }, [workspaceId]);

  return { handleFileUpload };
}
