# backend

FastAPIがcoreの挨拶ロジックをHTTP APIとして公開します。

APIの安全な公開理由コード・入力検証・内部例外の扱いは [設計・実装方針のエラー処理](../../../docs/設計・実装方針.md#エラー処理) を参照してください。

- 開発起動：ルートで `mise run //projects/app/backend:dev`
- API仕様：http://127.0.0.1:8000/docs
- テスト：`mise run //projects/app/backend:test`
- 静的検証：`mise run //projects/app/backend:lint`

Vueの開発サーバー経由で `/api` にアクセスするため、開発用のCORS全許可は不要です。

`STATIC_DIR` にVueのビルド出力を指定すると、FastAPIから画面も配信します。未設定ならAPI専用で起動します。Dockerでは自動設定されます。構成・起動方法は [Dockerガイド](../../../docs/Docker.md) を参照してください。
