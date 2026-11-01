import type { StorybookConfig } from "@storybook/vue3-vite";

const config: StorybookConfig = {
	stories: ["../src/**/*.stories.ts"],
	addons: ["@storybook/addon-a11y"],
	framework: "@storybook/vue3-vite",
	core: { disableTelemetry: true },
};
export default config;
