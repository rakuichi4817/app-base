/** APIの安全な公開理由。内部例外や任意の本文は表示しない。 */
const reasons: Record<string, string> = {
	INVALID_NAME: "名前を確認してください。",
	VALIDATION_ERROR: "入力内容を確認してください。",
	INTERNAL_ERROR: "サーバーで問題が発生しました。",
};

export class ApiError extends Error {
	constructor(
		public readonly status: number,
		public readonly code: string,
	) {
		super(`API request failed: ${status}`);
	}
}

/** 画面共通の失敗理由へ変換する。操作説明は画面側で付ける。 */
export function getErrorReason(error: unknown): string | undefined {
	if (!error) return undefined;
	if (error instanceof ApiError)
		return reasons[error.code] ?? "処理に失敗しました。";
	if (error instanceof TypeError) return "ネットワーク接続を確認してください。";
	return "応答を確認できませんでした。";
}
