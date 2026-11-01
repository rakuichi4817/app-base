# App Base

普段使う開発構成・設定をまとめた、**新規プロジェクトのひな形兼リファレンス**です。
業務固有の処理や外部サービスに依存せず、開発設定と最小限の動作サンプルをまとめています。

## 技術構成

| 分類 | 採用ツール |
| --- | --- |
| 共通 | mise、モノレポ、VS Codeマルチルートワークスペース |
| Python | uv、FastAPI、Ruff（整形・Lint）、ty（型チェック）、pytest |
| フロントエンド | Vue、TypeScript、Vite、Reka UI、TanStack Query、Tailwind CSS v4 |
| フロントエンド検証 | ESLint、Prettier、vue-tsc、Vitest、Vue Test Utils |
| 自動化 | GitHub Actions、Dependabot |

## セットアップ

Linux / WSLを基準とします。[mise](https://mise.jdx.dev/getting-started.html)を導入し、リポジトリルートで実行してください。Dockerや外部サービス、環境変数の設定は不要です。

```sh
mise trust --all   # 内容を確認したうえで子プロジェクトの設定も信頼する
mise install
mise run install
mise run dev
```

- 画面：http://127.0.0.1:5173
- API仕様：http://127.0.0.1:8000/docs
- `Ctrl+C` で開発サーバーを終了

VS Codeは `app-base.code-workspace` を開き、推奨拡張を導入します。
Pythonの `.venv` は `mise run install` で各プロジェクトに作られます。

## 構成

```text
app-base/
├─ mise.toml                     # ツール固定・共通タスク
├─ app-base.code-workspace        # エディター共通設定
├─ AGENTS.md                     # AI向け共通指示
├─ .github/                      # 基本CI・依存更新・PRテンプレート
├─ projects/
│  ├─ core/                      # HTTPに依存しない共通Pythonライブラリ
│  └─ app/
│     ├─ backend/                # FastAPI、独立したuv環境
│     └─ frontend/               # Vue、独立したpnpm環境
└─ docs/                         # 設定の意図・使い方・転用方法
```

画面の入力 → TanStack Query → FastAPI → coreの挨拶生成、という流れを最小例にしています。

## よく使う操作

| コマンド | 内容 |
| --- | --- |
| `mise run install` | ロックどおりの依存導入 |
| `mise run dev` | backend・frontendの並列起動 |
| `mise run lint` | Lint・整形確認・型チェック |
| `mise run format` | 整形・Lintの自動修正（ファイルを変更） |
| `mise run test` | Python・フロントエンドのテスト |
| `mise run build` | フロントエンド本番ビルド |
| `mise run check` | CIと同じ基本検証 |
| `mise run lock:refresh` | ロックの再解決（既存版優先、全面アップグレードではない） |
| `mise run storybook` | 表示部品のカタログを起動 |
| `mise run storybook:build` | カタログの静的ビルド |
| `mise run storybook:test` | ChromiumでStoryの操作・a11y検査（ブラウザー準備が必要） |
| `mise run license` | 依存ライセンス一覧の生成・方針照合 |

個別実行は `mise run //projects/core:test` など。全タスクは `mise tasks --all` で確認できます。

## ガイド

| 目的 | 読むガイド |
| --- | --- |
| 動かす | [開発環境](docs/開発環境.md)（mise・VS Code・CI・PR運用）、[Docker](docs/Docker.md)（一体配信） |
| 実装する | [設計・実装方針](docs/設計・実装方針.md)（責務・継承・共通化・エラー処理）、[Python](docs/Python.md)、[TypeScript・Vue](docs/TypeScript・Vue.md)（Tailwind・Storybookも含む） |
| 検証する | [テスト方針](docs/テスト方針.md)（fixture・モック）、[OSSライセンス](docs/OSSライセンス.md) |
| 転用する | [転用ガイド](docs/転用ガイド.md)（Python／FastAPI／TS／Vue単独・一式・設定だけ） |

Dockerでの単一コンテナー起動は `mise run docker:up`、画面は http://127.0.0.1:8080 です。終了は `mise run docker:down`。DockerとDocker Composeが必要です。通常の開発起動とは別の、本番向け配信構成の参考例です。

認証・TLS・DB・監視・E2E・配備先へのデプロイは含みません。必要になったプロジェクトで追加してください。
GitHubリポジトリの作成・公開やライセンスの指定は、このひな形には含めていません。
