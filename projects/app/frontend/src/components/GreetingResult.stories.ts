import type { Meta, StoryObj } from "@storybook/vue3-vite";
import { expect, within } from "storybook/test";
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
	play: async ({ canvasElement }) => {
		await expect(
			within(canvasElement).getByText("こんにちは、ルークさん！"),
		).toBeVisible();
	},
};
export const Loading: Story = { name: "読み込み中", args: { pending: true } };
export const Empty: Story = { name: "未取得" };
export const Failure: Story = {
	name: "通信失敗",
	args: { errorReason: "ネットワーク接続を確認してください。" },
	play: async ({ canvasElement }) => {
		await expect(within(canvasElement).getByRole("alert")).toHaveTextContent(
			"挨拶を取得できませんでした。",
		);
	},
};
