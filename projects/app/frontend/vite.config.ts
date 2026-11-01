import tailwindcss from "@tailwindcss/vite";
import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

/** 開発時のみAPIをFastAPIへ転送する。本番では同一オリジンで配信する。 */
export default defineConfig({
	plugins: [vue(), tailwindcss()],
	server: {
		host: "127.0.0.1",
		port: 5173,
		strictPort: true,
		proxy: { "/api": "http://127.0.0.1:8000" },
	},
});
