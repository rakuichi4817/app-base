# TypeScript・Vue

- [TypeScript共通](#typescript共通)
- [Vueの採用構成](#採用構成)
- [Tailwindの余白](#tailwindの余白)
- [Storybook](#storybook)

## TypeScript共通

Vueに依存しない方針です。型チェックはTypeScript、LintはESLintとtypescript-eslint、整形はPrettier、テストはVitestを使います。Vue SFCは追加でvue-tscを使います。

- strictとnoUncheckedIndexedAccessを基本にし、API応答はunknownから検証する。型アサーションだけで外部入力を保証済みにしない。
- 公開関数・型・設定と非自明な処理に、日本語JSDocで目的・制約を記載する。逐語説明や自明なコメントを増やさない。
- 入出力型はフィールドを明示し、継承・型合成・関数化は[設計・実装方針](設計・実装方針.md#継承より明示的な定義と合成)に従う。
- Promiseの失敗・キャンセルを区別し、例外を握りつぶさない。画面へは[エラー処理](設計・実装方針.md#エラー処理)の安全な理由を渡す。

Node.jsではtypesにnode、ESLint globalsにnodeを指定します。ブラウザーではDOMのlibとbrowser globalsを使い、Node.js専用APIを混ぜません。ビルド設定はNode.js、画面コードはブラウザーとして別tsconfigにします。単独利用は[転用ガイド](転用ガイド.md)を参照してください。

## 採用構成

- Vue SFC + `<script setup lang="ts">`：画面とローカル状態。
- Vite：開発サーバーと本番ビルド。
- ReKa UI（`reka-ui`）：見た目を固定しないUIプリミティブ。サンプルは `Label` の最小例。
- TanStack Query（`@tanstack/vue-query`）：サーバー状態の取得・キャッシュ・非同期状態。
- Tailwind CSS v4：`@tailwindcss/vite` と `@import "tailwindcss"`。v3の設定ファイルやディレクティブは不要。

ルーター・グローバル状態管理は未導入です。部品の確認には[Storybook](#storybook)を使います。

## 状態とAPI

ページは取得Composableと表示部品を組み合わせ、表示専用部品はpropsとイベントだけを扱います。通信はsrc/api、Query・キャッシュ・無効化はComposable、画面の操作説明はコンポーネントに置きます。[エラー処理](設計・実装方針.md#エラー処理)と責務を揃えてください。

入力途中の名前はVueの `ref`、送信した名前はQueryキーとして扱います。キーにAPI引数を含めることで名前ごとにキャッシュを分けます。
`queryFn` の `AbortSignal` をfetchへ渡し、HTTP失敗とJSONの形をAPIクライアントで検証します。サンプルでは失敗を見つけやすくするため自動リトライを無効にしています。

開発時はViteが `/api` を `127.0.0.1:8000` へ転送するので、CORSを全許可する必要はありません。
本番ビルドにプロキシ設定は含まれません。[Docker構成](Docker.md)ではビルド成果物をFastAPIへ渡し、同一オリジンで配信します。別の配信構成ではリバースプロキシ、または接続先設定と必要範囲のCORSを設計してください。

## フォーマット・Lint・型

入出力型の継承・型合成と、関数・コンポーネントの共通化は[設計・実装方針](設計・実装方針.md#継承より明示的な定義と合成)に従います。

| 機能 | ツール |
| --- | --- |
| JS / TS / Vueの不備検出 | ESLint + typescript-eslint + eslint-plugin-vue |
| Tailwindクラスの検査 | eslint-plugin-better-tailwindcss |
| 整形 | Prettier |
| Tailwindクラス順 | prettier-plugin-tailwindcss |
| SFCを含む型チェック | vue-tsc |

ESLintはflat configです。`eslint-config-prettier` を最後に適用し、整形の競合を避けます。クラス順・折り返しのESLintルールも無効にし、Prettierへ統一します。
Prettierはタブを使用し、TailwindのCSSエントリーを明示しています。TypeScriptはstrictと `noUncheckedIndexedAccess` を有効にしています。

## Tailwindの余白

要素間の距離は親のレイアウトが所有します。子にmarginを付けるより、並べ方と間隔を親で読める構成にします。

| 場面 | 使用するもの |
| --- | --- |
| 要素間の間隔 | `flex`／`grid` と `gap-*`・`gap-x-*`・`gap-y-*` |
| コンテナ内の余白 | `p-*`・`px-*`・`py-*` などのpadding |
| 中央寄せ | `mx-auto` などのauto marginを許容 |
| ブラウザーなどの既定余白のリセット | `m-0` などを許容 |
| Markdown本文の組版 | Typographyが提供する文章用marginを例外として許容（現在は未導入） |

通常の間隔調整には `mt-*`・`mb-*` などのmarginも、marginベースの `space-x-*`・`space-y-*` も使用しません。異なる間隔が必要なら意味のあるまとまりで親を分け、それぞれに `gap-*` を設定します。

```vue
<template>
	<section class="flex flex-col gap-6 p-5">
		<header class="flex flex-col gap-3">
			<h2>パイロット</h2>
			<p>名前を入力してください。</p>
		</header>
		<form class="flex flex-col gap-3">
			<label for="pilot-name">名前</label>
			<input id="pilot-name" />
		</form>
	</section>
</template>
```

`src/App.vue` もこの方針で記述しています。この余白ルールは現時点ではESLintの独自ルールで強制しておらず、実装・レビューで確認します。

## 依存・テスト

pnpmは `pnpm-lock.yaml` をコミットし、CIでは `--frozen-lockfile` で導入します。
`pnpm-workspace.yaml` の `allowBuilds` は必要な依存のインストールスクリプトだけを許可します。依存追加でエラーになっても一括許可せず、内容を確認して個別に設定してください。
Nodeとpnpmを更新する場合はルートmiseと `package.json` の `engines`・`packageManager` を同時に変更します。

Vitestはjsdomで動作します。APIクライアントの正常・HTTP失敗・不正形式と、Vue画面からの再取得を検証します。テストごとにQueryClientを作り、終了時にキャッシュを破棄します。
日本語のケース説明・準備と後片付け・通信モックの判断は[テスト方針](テスト方針.md)を参照してください。
実ブラウザーの見た目・フォーカス・ブラウザー間互換性や、実際のFastAPIとの通信は、このテストだけでは保証しません。

## Storybook

Story用のVitest設定は独立したVite設定なので、VueとTailwindのプラグインを明示します。Storybookのビルド成功だけでは、ブラウザーテスト側の変換設定が正しいことは保証されません。

Vue部品をAPIから独立して確認します。`GreetingResult` は表示の責務を持ち、取得状態はComposable、通信はAPIクライアントが担当します。クラス列の重複削減だけで部品化しません。

```sh
mise run storybook          # http://localhost:6006
mise run storybook:build    # storybook-staticへ出力
mise run browser:deps       # LinuxのOS依存。対話可能な端末で実行（sudoが必要）
mise run browser:install    # Chromiumの導入
mise run storybook:test     # 実ブラウザーでStoryのplayとa11y検査
```

Storyは正常・読み込み中・未取得・通信失敗の代表状態を用意します。操作・assertはplayへ記載し、a11y違反はテスト失敗として扱います。自動検査は手動のキーボード・読み上げ確認を代替しません。
jsdomのVitestは取得や状態の判断、Storyは部品の表示・操作、実APIとの結合は開発サーバーやDockerで確認し、同じ保証を重複させません。
ブラウザーの導入は通常のinstallに混ぜません。Storybookの出力はアプリのdistとは別で、Dockerへ配布しません。
