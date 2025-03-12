import type { Meta, StoryObj } from "@storybook/react";
import { fn } from "@storybook/test";
import { X } from "lucide-react";

import { Button } from "./button";

const meta = {
  title: "UI/Button",
  component: Button,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: [
        "default",
        "destructive",
        "outline",
        "secondary",
        "ghost",
        "link",
      ],
    },
    size: {
      control: "select",
      options: ["default", "sm", "lg", "icon", "icon-sm", "icon-xs"],
    },
    asChild: {
      table: {
        disable: true,
      },
    },
  },
  args: { onClick: fn() },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const DefaultButton: Story = {
  parameters: {},
  args: {
    children: "Button",
  },
};

export const CloseButton: Story = {
  args: {
    variant: "ghost",
    size: "icon-xs",
    children: <X />,
  },
  tags: ["autodocs"],
};

export const SubmitButton: Story = {
  args: {
    type: "submit",
    children: "Update preferences",
  },
};
