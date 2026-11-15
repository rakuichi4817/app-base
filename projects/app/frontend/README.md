# frontend

Vue + TypeScript + Viteの最小アプリです。

Storybookはルートで `mise run storybook`、静的ビルドは `mise run storybook:build`、OSS一覧は `mise run license` です。使い方は [TypeScript・VueのStorybook](../../../docs/TypeScript・Vue.md#storybook) を参照してください。

- ReKa UI（パッケージ名 `reka-ui`）：ラベルなどアクセシブルなUIプリミティブ
- TanStack Query：APIの取得・キャッシュ・ローディング・エラー管理
- Tailwind CSS v4：ViteプラグインとCSSエントリーポイントによるスタイル管理
- ESLint / Prettier / vue-tsc：Lint・整形・型チェック
- Vitest / Vue Test Utils / jsdom：APIクライアントと画面のテスト

ルートで `mise run dev` を実行し、http://127.0.0.1:5173 を開きます。
個別操作は `mise run //projects/app/frontend:lint` などで実行できます。

Viteの `/api` プロキシは開発時のみ有効です。`dist/` をFastAPIへ渡す [Docker構成](../../../docs/Docker.md) では、画面とAPIを同一オリジンで配信します。
