import { ApiError } from "./errors";

export interface GreetingResponse {
	message: string;
}

/** HTTPエラーと応答形式の不正を検出して挨拶を取得する。 */
export async function fetchGreeting(
	name: string,
	signal?: AbortSignal,
): Promise<GreetingResponse> {
	const params = new URLSearchParams({ name });
	const response = await fetch(`/api/greeting?${params}`, { signal });

	if (!response.ok) {
		const body: unknown = await response.json().catch(() => null);
		const code =
			typeof body === "object" &&
			body !== null &&
			"code" in body &&
			typeof body.code === "string"
				? body.code
				: "UNKNOWN";
		throw new ApiError(response.status, code);
	}

	const data: unknown = await response.json();

	if (
		typeof data !== "object" ||
		data === null ||
		!("message" in data) ||
		typeof data.message !== "string"
	) {
		throw new Error("APIの応答形式が正しくありません。");
	}

	return { message: data.message };
}
