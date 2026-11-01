import js from "@eslint/js";
import prettier from "eslint-config-prettier";
import tailwindcss from "eslint-plugin-better-tailwindcss";
import { defineConfig, globalIgnores } from "eslint/config";
import vue from "eslint-plugin-vue";
import globals from "globals";
import tseslint from "typescript-eslint";

/** LintはESLint、整形とTailwindのクラス順はPrettierに任せる。 */
export default defineConfig([
	globalIgnores(["dist/**", "coverage/**", "storybook-static/**"]),
	js.configs.recommended,
	tseslint.configs.recommended,
	vue.configs["flat/recommended"],
	{
		files: ["**/*.{js,ts,vue}"],
		extends: [tailwindcss.configs["recommended-error"]],
		settings: {
			"better-tailwindcss": {
				cwd: import.meta.dirname,
				entryPoint: "src/style.css",
			},
		},
		languageOptions: { globals: { ...globals.browser, ...globals.node } },
		rules: {
			"better-tailwindcss/enforce-consistent-class-order": "off",
			"better-tailwindcss/enforce-consistent-line-wrapping": "off",
		},
	},
	{
		files: ["**/*.vue"],
		languageOptions: { parserOptions: { parser: tseslint.parser } },
	},
	prettier,
]);
