import { useEffect, type ReactNode } from "react";
import { create } from "zustand";
import { useHotkeys } from "react-hotkeys-hook";
import { Search } from "lucide-react";

export type Action = {
  name: string;
  icon: ReactNode;
  description: string;
  keys: string[];
  path: string;
};

const defaultActions = {
  search: {
    name: "search",
    description: "Search",
    keys: ["mod+k"],
    icon: <Search />,
    path: "general/navigation",
  },
} satisfies Record<string, Action>;

export type ActionType = keyof typeof defaultActions;

type ActionsStore = {
  actions: Record<ActionType, Action>;
  getAction: (name: ActionType) => Action | null;
  changeActionKeys: (name: ActionType, keys: string[]) => string | null;
  resetActionKeys: (name: ActionType) => void;
  listActions: () => Action[];
};

export const useActions = create<ActionsStore>((set, get) => ({
  actions: { ...defaultActions },

  getAction: (name) => get().actions[name] || null,

  changeActionKeys: (name, keys) => {
    const actions = get().actions;

    for (const action of Object.values(actions)) {
      if (
        action.name !== name &&
        action.keys.some((key) => keys.includes(key))
      ) {
        // TODO: Better error message
        return `Keybinding conflict with action "${action.name}"`;
      }
    }

    set((state) => ({
      actions: {
        ...state.actions,
        [name]: { ...state.actions[name], keys },
      },
    }));

    return null;
  },

  resetActionKeys: (name: ActionType) => {
    if (defaultActions[name]) {
      set((state) => ({
        actions: { ...state.actions, [name]: defaultActions[name] },
      }));
    }
  },

  listActions: () => Object.values(get().actions),
}));

export function useAction(name: ActionType, callback: () => void) {
  const action = useActions((state) => state.getAction(name));

  useEffect(() => {
    if (!action) return;
    const keys = action.keys.join(",");

    // Bind hotkeys
    const unbind = useHotkeys(keys, callback, [keys]);

    return () => {
      unbind(null);
    };
  }, [action, callback]);
}
