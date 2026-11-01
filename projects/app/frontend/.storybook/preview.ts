import type { Preview } from "@storybook/vue3-vite";
import "../src/style.css";

const preview: Preview = { parameters: { a11y: { test: "error" } } };
export default preview;
