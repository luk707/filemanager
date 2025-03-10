import type { ReactNode } from "react";

export interface PreferencesFieldProps {
  title: string;
  description: string;
  children: ReactNode;
}

export function PreferencesField({
  title,
  description,
  children,
}: PreferencesFieldProps) {
  return (
    <fieldset>
      <legend className="text-sm/6 font-semibold">{title}</legend>
      <p className="mt-1 text-sm/6 text-muted-foreground">{description}</p>
      {children}
    </fieldset>
  );
}
