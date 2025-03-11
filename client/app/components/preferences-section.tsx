import type { ReactNode } from "react";

interface PreferencesSectionProps {
  title: ReactNode;
  description: ReactNode;
  children: ReactNode;
}

export function PreferencesSection({
  title,
  description,
  children,
}: PreferencesSectionProps) {
  return (
    <>
      <div>
        <h2 className="text-base/7 font-semibold">{title}</h2>
        <p className="mt-1 text-sm/6 text-muted-foreground">{description}</p>
      </div>
      <div className="grid grid-cols-1 gap-x-6 gap-y-8">{children}</div>
    </>
  );
}
