<script setup lang="ts">
defineProps<{ message?: string; errorReason?: string; pending: boolean }>();
</script>

<template>
	<div
		class="rounded-xl border border-slate-200 bg-white p-5"
		aria-live="polite"
		:aria-busy="pending"
	>
		<p v-if="errorReason" role="alert" class="text-red-700">
			挨拶を取得できませんでした。{{ errorReason }}
		</p>
		<p v-else-if="pending">読み込み中…</p>
		<p v-else-if="message">{{ message }}</p>
		<p v-else>まだ挨拶はありません。</p>
	</div>
</template>
