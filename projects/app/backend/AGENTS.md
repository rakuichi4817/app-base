# バックエンドの作業指示

- Ruff・ty・pytestを使い、公開APIに型注釈と日本語のGoogle Style docstringを書く。
- HTTPの入出力はPydanticモデルで明示する。共通ロジックは `app_base_core` に置く。
- プレゼンテーション（`presentation`）はHTTPの入出力・エラー変換、アプリケーションサービス（`application_service`）はユースケースの調整・トランザクションを担当する。必要になるまで中継層を増やさない。
- クライアントの生成・注入・終了はアプリケーション側で管理し、coreのモデルへ持ち込まない。
- FastAPIの依存は `Annotated[型, Depends(get_xxx)]` で明示する。dependencyは提供・組み立てを担当し、暗黙の業務処理・通信をしない。共有資源はlifespan、リクエスト固有資源はyieldで寿命を管理し、利用側が共有資源を閉じない。
- dependency_overridesはテスト終了時に復元する。overrideだけではlifespanの接続生成を止められない点に注意する。詳細は [Pythonの依存注入](../../../docs/Python.md#fastapiの依存注入) を参照する。
- 業務エラーをHTTPエラーへ変換する場合は対象例外を限定し、包括的な例外捕捉を避ける。
- APIの正常系・入力不正・エラー変換を `TestClient` で検証する。
- テスト名は `test_条件と期待結果` の日本語とする。アプリケーションサービス（`application_service`）の判断は外部連携のドメインサービス（`domain_service`）の公開境界をモックし、HTTP変換・保存・配信そのものを検証するケースでは対象の実装を使う。
- 起動時の通信が検証対象外なら、起動fixtureをモックfixtureに依存させ、起動前から終了まで差し替える。fixture引数の並び順に依存しない。
- 実サービスの接続情報や認証情報をサンプルに埋め込まない。
- APIは安全な理由コード・理由と必要な項目別エラーを返し、入力値・内部例外を公開しない。絶対時刻はタイムゾーン付きUTC、async経路で同期I/Oをブロックさせない。
