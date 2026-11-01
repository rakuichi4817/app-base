import { describe, expect, it } from "vitest";
import { ApiError, getErrorReason } from "./errors";

describe("安全なエラー理由への変換", () => {
	it("既知の500理由を保持し、操作説明を混ぜない", () => {
		expect(getErrorReason(new ApiError(500, "INTERNAL_ERROR"))).toBe(
			"サーバーで問題が発生しました。",
		);
	});
	it("未知コードや内部例外の文字列を公開しない", () => {
		expect(getErrorReason(new ApiError(500, "secret"))).toBe(
			"処理に失敗しました。",
		);
		expect(getErrorReason(new Error("secret"))).toBe(
			"応答を確認できませんでした。",
		);
	});
	it("通信障害と未失敗を区別する", () => {
		expect(getErrorReason(new TypeError("fetch failed"))).toBe(
			"ネットワーク接続を確認してください。",
		);
		expect(getErrorReason(null)).toBeUndefined();
	});
});
