# Python

## ツールの役割

| ツール | 役割 | 主な設定 |
| --- | --- | --- |
| uv | 仮想環境・依存解決・実行・パッケージビルド | `pyproject.toml`、`uv.lock` |
| Ruff | Lint・import整列・フォーマット | `[tool.ruff]` |
| ty | 型チェック・VS Code言語サービス | `[tool.ty.environment]` |
| pytest | 単体・APIテスト | `[tool.pytest.ini_options]` |
| FastAPI / Pydantic | HTTP API・入出力検証 | backendの `main.py` |

Pythonの版はmiseで固定し、各 `requires-python` でも対応するマイナー版を限定します。版を変える場合はRuffの `target-version` とロックも合わせて更新します。

## 独立したuv環境

`uv sync --locked` はロックを勝手に更新せず、各プロジェクトの `.venv` に開発依存を含めて導入します。
`uv run --locked` も同じロックを前提とします。coreはbackendの環境にもeditable導入されるため、coreの実装変更は再コピーなしで反映されます。

両方とも `src/` レイアウト・`uv_build` を使います。配布名は `app-base-core` / `app-base-backend`、import名は `app_base_core` / `app_base_backend` です。

## Lint・整形・型

Ruffは `E, F, W, I, UP` を選び、基本的な不備・未使用import・import順・Python構文更新を検出します。行幅は88です。
tyは各プロジェクトの `.venv` を参照します。CLIは `ty check`、VS Codeはty拡張を使います。
Black・isort・mypy・Pyrightを重ねては入れていません。

公開関数には型注釈と日本語docstringを付け、処理をまとめすぎず空行で区切ります。アプリ固有のHTTP処理はbackend、共通ロジックはcoreに置きます。
レイヤーごとの責務・配置、入出力モデルの継承や関数化の判断は[設計・実装方針](設計・実装方針.md)に従います。

## 依存変更

例としてbackendへの追加は、そのディレクトリで `mise exec -- uv add <パッケージ名>` を実行します。開発ツールは `uv add --dev <パッケージ名>` です。
既存版優先で全体を再解決する場合はルートの `mise run lock:refresh`、最新版へ明示的に更新する場合は対象で `mise exec -- uv lock --upgrade` を実行します。
coreの依存・メタデータを変更した場合はbackendのロックも再解決してください。

## 日時・非同期・説明

絶対時刻はタイムゾーン付きUTCで保持し表示時に変換します。営業日・繰り返し時刻は地域とタイムゾーンの意味を失わない表現を使い、naive datetimeを安易に追加しません。
async内で長時間の同期I/Oや重い計算を直接実行せず、非同期APIやexecutorを使います。外部I/Oでは再試行・冪等性・競合・部分失敗と整合性の所有者を明確にします。広い例外捕捉による正常扱いは禁止し、フォールバックの根拠と観測方法を決めます。
公開API・非自明な処理のGoogle Style docstringはArgs、None以外のReturns、generatorのYields、契約上伝播するRaisesを説明します。空の節を作らず、signature・return/yield・例外伝播と照合してください。contextmanagerは利用側へ渡す資源と解放をReturnsに、validatorは入力・返却値と拒否条件を記載します。型や変数名の逐語説明は避けます。

## FastAPIの依存注入

### 記法・責務・配置

依存は `Annotated[型, Depends(get_xxx)]` で引数へ明示します。`Depends` に関数を渡し、その場で `get_xxx()` を呼びません。共通の提供関数はbackendの `dependencies.py`、機能固有の組み立ては各機能の `dependencies.py` に置きます。現在の挨拶サンプルには外部資源がないので、DI用のクラスやファイルを先回りして追加しません。

- dependencyは設定・資源の提供やサービスの組み立てを担当し、生成するだけの関数に暗黙の通信・保存・業務判断を混ぜない。
- 認証・認可を行うdependencyは、その責務と副作用を名前・契約に明示して区別する。
- アプリケーションサービス（`application_service`）やcoreへ `Depends`・Requestを持ち込まない。組み立てた通常の引数で渡す。
- FastAPIは既定で同一リクエスト内の同じdependencyの結果をキャッシュする。グローバル共有とは異なる。`use_cache=False` は複数回の生成が必要な理由がある場合だけ使う。

### 共有資源はlifespanで所有する

設定はアプリ生成時に解決し、共有クライアントはlifespanで生成・解放します。dependencyは `request.app.state` から貸し出すだけで、利用側はcloseしません。アプリごとに資源を持ち、モジュールimport時に接続を作りません。
以下は外部HTTPクライアントを追加する場合の独立した例です。`httpx2` を本番依存に追加したプロジェクトを前提とし、現在の挨拶APIへ追加が必要という意味ではありません。

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, cast

from fastapi import Depends, FastAPI, Request
from httpx2 import AsyncClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with AsyncClient(timeout=10) as client:
        app.state.http_client = client
        yield


def get_http_client(request: Request) -> AsyncClient:
    return cast(AsyncClient, request.app.state.http_client)


app = FastAPI(lifespan=lifespan)


@app.get("/client-status")
async def client_status(
    client: Annotated[AsyncClient, Depends(get_http_client)],
) -> dict[str, bool]:
    return {"ready": not client.is_closed}
```

`cast` は入力検証ではなく、lifespanで保証したstateの型を示します。アプリが持たない資源の存在を偽装するためには使いません。実装時は公開APIのdocstringも上の基準に従って記載します。
サービスを組み立てる場合は、例えば `get_pilot_service(client: Annotated[AsyncClient, Depends(get_http_client)]) -> PilotService` で `PilotService(client=client)` を返します。`PilotService` は通常の引数だけを受け取り、そこで通信を開始しません。

### リクエスト単位の資源とyield

セッションなどリクエスト固有の資源はyield dependencyで生成・解放します。共有クライアントをリクエストごとに閉じたり、可変セッションをlifespanで全リクエストへ共有したりしません。

```python
# SQLAlchemyを追加し、get_session_factoryを定義した場合の例。
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_session(
    factory: Annotated[
        async_sessionmaker[AsyncSession], Depends(get_session_factory)
    ],
) -> AsyncIterator[AsyncSession]:
    async with factory() as session:
        yield session
```

上はDB導入時の抜粋で、SQLAlchemyとセッション生成器は現在のサンプルにはありません。解放は `async with` や `try/finally` で失敗時も保証し、yield到達前の失敗にも注意します。
資源解放と業務のcommit/rollbackは別です。ユースケースのトランザクションはアプリケーションサービス（`application_service`）側で明示し、レスポンス送信後のdependency終了処理へ暗黙のcommitを置きません。
yield dependencyの終了時点はscopeで変わります。既定のrequest scopeはレスポンス送信後、function scopeはエンドポイント終了後・送信前です。ストリーミングが資源を使う場合も寿命を確認してください。バックグラウンド処理にはリクエストのセッションを渡さず、その処理自身の寿命で資源を用意します。

### テストでの差し替え

`application.dependency_overrides[元の提供関数] = テスト用提供関数` とし、ルーターが実際にDependsへ渡した関数オブジェクトをキーにします。文字列・戻り値ではありません。テストはアプリを新しく生成し、overrideを終了時に必ず復元します。

```python
# 上の共有クライアント例のappとget_http_clientを使う例。
from fastapi.testclient import TestClient


def test_依存を差し替える():
    previous = app.dependency_overrides.copy()

    async def replacement():
        async with AsyncClient() as client:
            yield client

    try:
        app.dependency_overrides[get_http_client] = replacement
        with TestClient(app) as client:
            assert client.get("/client-status").json() == {"ready": True}
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
```

上はoverrideの適用と復元を示す抜粋です。実際のケースは[テストクラス](テスト方針.md#ケースの選び方と読みやすさ)内に置き、共有するなら明示要求するfixtureへまとめます。
**overrideはlifespanの実行を止めません。** 起動時の通信が検証対象外なら、資源生成器をアプリファクトリーへ注入するか、起動fixtureをモックfixtureに依存させ、起動前から終了まで差し替えます。実接続テストを同じモックで隠しません。

## テストの実行方法

ケース名・fixtureの配置と寿命・モックと実物の使い分けは[テスト方針](テスト方針.md)に従います。

coreは純粋な関数、backendは `TestClient` によるHTTP境界を検証します。外部サービスは不要です。
現在のFastAPI / StarletteのTestClientに合わせ、開発用HTTPクライアントは `httpx2` を使用しています。
`GET /api/greeting` は名前を検証し、coreの `ValueError` を422へ変換します。`GET /api/health` はプロセス稼働の簡易チェックで、外部依存の健全性を保証するものではありません。
