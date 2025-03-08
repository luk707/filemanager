import { useSearchParams } from "react-router";

export function useInspector() {
  const [searchParams, setSearchParams] = useSearchParams();
  return {
    isOpen: searchParams.get("i") !== null,
    // TODO: Support for different types of things to inspect
    open() {
      searchParams.set("i", "");
      setSearchParams(searchParams, { replace: true });
    },
    close() {
      searchParams.delete("i");
      setSearchParams(searchParams, { replace: true });
    },
  };
}
