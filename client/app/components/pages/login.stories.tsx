import type { Meta, StoryObj } from "@storybook/react";

import { LoginPage } from "./login";

const meta = {
  title: "Pages/Login",
  component: LoginPage,
  parameters: {
    layout: "centered",
  },
} satisfies Meta<typeof LoginPage>;

export default meta;
type Story = StoryObj<typeof meta>;

export const DefaultPage: Story = {
  args: {
    organizationName: "Acme Inc.",
  },
};
