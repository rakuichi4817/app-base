import { QueryClient, VueQueryPlugin } from "@tanstack/vue-query";
import { flushPromises, mount } from "@vue/test-utils";
import { describe, expect, it, vi } from "vitest";
import App from "./App.vue";

describe("挨拶画面（App）", () => {
	it("APIの挨拶を表示し、名前の変更時に再取得する", async () => {
		// GIVEN: 名前に応じた応答を返す通信境界と、ケース専用のQueryClient。
		vi.stubGlobal(
			"fetch",
			vi.fn().mockImplementation(async (url: string) => {
				const name = new URL(url, "http://localhost").searchParams.get("name");

				return new Response(
					JSON.stringify({ message: `こんにちは、${name}さん！` }),
				);
			}),
		);
		const queryClient = new QueryClient({
			defaultOptions: { queries: { retry: false } },
		});
		const wrapper = mount(App, {
			global: { plugins: [[VueQueryPlugin, { queryClient }]] },
		});

		try {
			// WHEN: 初回表示の取得が完了する。
			await vi.waitFor(() =>
				expect(wrapper.text()).toContain("こんにちは、ルークさん！"),
			);
			// WHEN: 名前を変更して送信する。
			await wrapper.get("input").setValue("レイア");
			await wrapper.get("form").trigger("submit");
			await flushPromises();
			// THEN: 変更後の名前の挨拶を表示する。
			await vi.waitFor(() =>
				expect(wrapper.text()).toContain("こんにちは、レイアさん！"),
			);

			// WHEN: 入力を空白だけにする。THEN: 送信を無効にする。
			await wrapper.get("input").setValue("   ");
			expect(wrapper.get("button").attributes("disabled")).toBeDefined();
		} finally {
			wrapper.unmount();
			queryClient.clear();
		}
	});
});
