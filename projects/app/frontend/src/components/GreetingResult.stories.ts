import type { Meta, StoryObj } from "@storybook/vue3-vite";
import GreetingResult from "./GreetingResult.vue";

const meta = {
	title: "表示/挨拶の取得結果",
	component: GreetingResult,
	args: { pending: false },
} satisfies Meta<typeof GreetingResult>;
export default meta;
type Story = StoryObj<typeof meta>;
export const Success: Story = {
	name: "正常取得",
	args: { message: "こんにちは、ルークさん！" },
};
export const Loading: Story = { name: "読み込み中", args: { pending: true } };
export const Empty: Story = { name: "未取得" };
export const Failure: Story = {
	name: "通信失敗",
	args: { errorReason: "ネットワーク接続を確認してください。" },
};
