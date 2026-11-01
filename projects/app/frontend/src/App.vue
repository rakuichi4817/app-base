<script setup lang="ts">
import { Label } from "reka-ui";
import { computed, ref } from "vue";
import GreetingResult from "./components/GreetingResult.vue";
import { useGreeting } from "./composables/useGreeting";

const name = ref("ルーク");
const submittedName = ref("ルーク");
const canSubmit = computed(() => name.value.trim().length > 0);

const { data, errorReason, isFetching } = useGreeting(submittedName);

function submitName(): void {
	if (canSubmit.value) {
		submittedName.value = name.value.trim();
	}
}
</script>

<template>
	<main class="mx-auto flex max-w-xl flex-col gap-8 px-6 py-20">
		<header class="flex flex-col gap-4">
			<div class="flex flex-col gap-3">
				<p class="text-sm font-semibold tracking-widest text-indigo-700">
					APP BASE
				</p>
				<h1 class="text-3xl font-bold">新しいプロジェクトの出発点</h1>
			</div>
			<p class="text-slate-600">
				Vue・Reka UI・TanStack Query・Tailwind
				CSSからFastAPIを呼び出す最小例です。
			</p>
		</header>

		<div class="flex flex-col gap-6">
			<form class="flex flex-col gap-3" @submit.prevent="submitName">
				<Label for="name" class="block font-medium">名前</Label>
				<div class="flex gap-3">
					<input
						id="name"
						v-model="name"
						maxlength="80"
						required
						class="min-w-0 flex-1 rounded-lg border border-slate-300 bg-white px-3 py-2 focus-visible:outline-2 focus-visible:outline-indigo-600"
					/>
					<button
						type="submit"
						:disabled="!canSubmit || isFetching"
						class="rounded-lg bg-indigo-700 px-4 py-2 font-medium text-white hover:bg-indigo-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:cursor-not-allowed disabled:opacity-50"
					>
						送信
					</button>
				</div>
			</form>

			<GreetingResult
				:message="data?.message"
				:error-reason="errorReason"
				:pending="isFetching"
			/>
		</div>
	</main>
</template>
