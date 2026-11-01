import { describe, expect, it, vi } from "vitest";
import { fetchGreeting } from "./greeting";

describe("挨拶のAPI取得（fetchGreeting）", () => {
	it("名前をURLエンコードしてAPIを呼ぶ", async () => {
		const fetchMock = vi
			.fn()
			.mockResolvedValue(
				new Response(JSON.stringify({ message: "こんにちは、レイアさん！" })),
			);
		vi.stubGlobal("fetch", fetchMock);

		await expect(fetchGreeting("レイア")).resolves.toEqual({
			message: "こんにちは、レイアさん！",
		});
		expect(fetchMock).toHaveBeenCalledWith(
			`/api/greeting?${new URLSearchParams({ name: "レイア" })}`,
			{ signal: undefined },
		);
	});

	it("HTTP失敗をエラーにする", async () => {
		vi.stubGlobal(
			"fetch",
			vi.fn().mockResolvedValue(new Response(null, { status: 500 })),
		);

		await expect(fetchGreeting("レイア")).rejects.toMatchObject({
			status: 500,
			code: "UNKNOWN",
		});
	});

	it("不正な応答形式をエラーにする", async () => {
		vi.stubGlobal(
			"fetch",
			vi.fn().mockResolvedValue(new Response(JSON.stringify({ message: 42 }))),
		);

		await expect(fetchGreeting("レイア")).rejects.toThrow("応答形式");
	});
});
