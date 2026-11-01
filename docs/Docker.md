# DockerでVueとPythonをまとめて配信する

`projects/app/.docker/Dockerfile` でVueとPythonをまとめてビルドします。本番向けの単一コンテナーの参考例であり、認証・TLS・デプロイ先の設定は含みません。

## ビルドと起動

DockerとDocker Composeを用意し、リポジトリルートで実行します。ホスト側のNode.jsやPython環境はビルドに使用しません。

```sh
mise run docker:check  # Compose設定の検証
mise run docker:up    # ビルド・バックグラウンド起動・正常性確認
```

- 画面：http://127.0.0.1:8080
- API仕様：http://127.0.0.1:8080/docs
- ログ：`docker compose logs -f app`
- 終了・コンテナー削除：`mise run docker:down`（イメージ・ビルドキャッシュは保持）

ホストのポートは `APP_PORT=18080 mise run docker:up` のように変更できます。コンテナー内は8000固定です。公開先はホストの `127.0.0.1` に限定しているため、外部へ公開する場合は配備先に合わせて変更してください。
イメージの作成だけなら `mise run docker:build` です。Composeを使わずビルドする場合も、コンテキストはリポジトリルートにします。

```sh
docker build -f projects/app/.docker/Dockerfile -t app-base:local .
```

## 3段階のマルチステージビルド

| ステージ | 処理 |
| --- | --- |
| `frontend-build` | Node.js・pnpmでロックどおりに依存導入し、Vueをビルド |
| `backend-build` | Python・uvでbackendとcoreの本番依存を非editable導入 |
| `runtime` | 仮想環境とVueの `dist/` を受け取り、FastAPIを起動 |

backendからcoreへの相対参照を保つため、ビルド時も `projects/app/backend` と `projects/core` の位置関係を維持します。
最終イメージにはNode.js・pnpm・uvや開発依存を持ち込まず、UID/GID 10001の非rootユーザーで実行します。ヘルスチェックはPython標準ライブラリで `/api/health` を呼び出します。
BuildKitのキャッシュマウントでpnpm・uvのダウンロードを再利用します。`.dockerignore` はホストの `.venv`・`node_modules`・`dist`・環境ファイルなどを除外します。
ツール版はルート `mise.toml` とDockerfileで揃えます。Node.js・pnpmの変更時はfrontendの `package.json`、Pythonの変更時は各 `pyproject.toml` とロックも確認してください。

## FastAPIからの配信

Dockerでは `STATIC_DIR=/app/frontend` を設定し、その配下にVueの成果物をコピーします。APIを先に登録し、最後に `/` へ静的配信をマウントします。

- API・OpenAPI・Swagger UIは通常どおり動作する。
- 実ファイルが存在すれば、その内容を配信する。
- 拡張子のない画面URLへのGET/HEADは `index.html` にフォールバックする。
- 未配置の `/api`・`/api/*`・`/assets/*`・拡張子付きパスは404を維持する。
- POSTなど、静的配信が対応しないメソッドは405とし、HTMLへ置き換えない。
- `STATIC_DIR` 指定時に `index.html` がなければ起動時に失敗させる。

フォールバックの実装は `SPAStaticFiles` に置き、フレームワークの振る舞いを拡張する継承として扱います。フィールド共有だけの継承を避けるルールとは区別します。
画面パスは拡張子を持たず、APIとビルド済みアセットはそれぞれ `api` と `assets` を予約する前提です。現在はVue Router未導入なので、深いURLでも同じ最小画面を表示します。将来ルーターを導入する場合、未知の画面の表示はフロントエンド側で制御してください。

## 開発時との違い・転用時の注意

依存OSSを含む配布前には [OSSライセンス](OSSライセンス.md) の確認が必要です。Storybookの成果物はアプリの配布イメージに含めません。

`mise run dev` は従来どおりViteとFastAPIを別起動し、ホットリロードを使います。通常は `STATIC_DIR` を設定しないため、FastAPIはAPI専用です。
Dockerでは同一オリジンで画面とAPIを提供するので、Viteの開発プロキシやCORS全許可は不要です。Composeにソースのバインドマウントはなく、ソース変更後は再ビルドします。
core/backendの名前やパスを変える場合は、DockerfileのCOPYと起動コマンドも更新してください。Terraformなどの配備資源が必要なら `infra/` などに別途用意します。

バックエンドの配信テストは `mise run //projects/app/backend:test`、実イメージの確認は `mise run docker:up` を使います。通常のCIではDockerビルドを実行せず、Pythonの配信テストとVueのビルドまでを検証します。
