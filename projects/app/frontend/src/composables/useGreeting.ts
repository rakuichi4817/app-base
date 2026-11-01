import { useQuery } from "@tanstack/vue-query";
import { computed, type Ref } from "vue";
import { fetchGreeting } from "../api/greeting";
import { getErrorReason } from "../api/errors";

/** 取得状態と安全な理由を提供し、画面固有の操作説明は持たない。 */
export function useGreeting(name: Ref<string>) {
	const query = useQuery({
		queryKey: computed(() => ["greeting", name.value]),
		queryFn: ({ signal }) => fetchGreeting(name.value, signal),
		retry: false,
	});
	return {
		...query,
		errorReason: computed(() => getErrorReason(query.error.value)),
	};
}
