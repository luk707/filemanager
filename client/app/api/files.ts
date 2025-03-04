export interface File {
  id: string;
  name: string;
  contentType: string;
  size: number;
}

export async function getFiles(): Promise<File[]> {
  return [
    {
      id: "752fe730-560f-484d-b608-4ecd85e306c3",
      name: "Sales Figures 2025",
      contentType: "text/csv",
      size: 0,
    },
    {
      id: "f59fcedd-c326-4216-b575-b99c695f0304",
      name: "Logo",
      contentType: "image/jpeg",
      size: 0,
    },
    {
      id: "0c411cb1-bb54-48bd-a672-44f5b277dcb0",
      name: "Windows98 Post Boot Sound",
      contentType: "audio/wav",
      size: 0,
    },
  ];
}
