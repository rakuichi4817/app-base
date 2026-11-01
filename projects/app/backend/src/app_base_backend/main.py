"""フロントエンドへ公開する最小API。"""

import os
from pathlib import Path
from typing import Annotated, Literal

from app_base_core.greeting import create_greeting
from fastapi import APIRouter, FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from app_base_backend.static_files import SPAStaticFiles

router = APIRouter(prefix="/api")


class HealthResponse(BaseModel):
    """ヘルスチェックの応答。"""

    status: Literal["ok"]


class GreetingResponse(BaseModel):
    """挨拶APIの応答。"""

    message: str


@router.get("/health")
def health() -> HealthResponse:
    """APIの稼働状態を返す。

    Returns:
        稼働中を表す応答。
    """
    return HealthResponse(status="ok")


@router.get("/greeting")
def greeting(
    name: Annotated[str, Query(min_length=1, max_length=80)] = "ルーク",
) -> GreetingResponse:
    """共通ライブラリで生成した挨拶を返す。

    Args:
        name: 挨拶の対象となる名前。

    Returns:
        挨拶メッセージ。

    Raises:
        HTTPException: 名前が空白のみの場合（422）。
    """
    try:
        message = create_greeting(name)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return GreetingResponse(message=message)


def create_app(static_dir: Path | None = None) -> FastAPI:
    """APIを登録し、指定された場合だけビルド済み画面を配信する。

    Args:
        static_dir: index.htmlを含むVueのビルド出力。NoneならAPI専用。

    Returns:
        APIと任意の静的配信を登録したアプリケーション。

    Raises:
        RuntimeError: 指定した配信先にindex.htmlが存在しない場合。
    """
    application = FastAPI(title="App Base", version="0.1.0")
    application.include_router(router)

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, error: RequestValidationError
    ) -> JSONResponse:
        """入力値を隠し、項目ごとの検証失敗を返す。

        Args:
            request: エラーが発生したリクエスト。
            error: 入力検証の失敗。

        Returns:
            公開理由コードと項目だけを含む422応答。
        """
        return JSONResponse(
            status_code=422,
            content={
                "code": "VALIDATION_ERROR",
                "reason": "入力内容を確認してください。",
                "errors": [
                    {"field": ".".join(map(str, item["loc"])), "code": "INVALID_VALUE"}
                    for item in error.errors()
                ],
            },
        )

    @application.exception_handler(StarletteHTTPException)
    async def http_error_handler(
        request: Request, error: StarletteHTTPException
    ) -> JSONResponse:
        """HTTPエラーの内部詳細を安全な公開理由へ置き換える。

        Args:
            request: エラーが発生したリクエスト。
            error: ステータスと必要なヘッダーを保持するHTTP例外。

        Returns:
            安全な公開理由を含むHTTPエラー応答。
        """
        code = "INVALID_NAME" if error.status_code == 422 else "HTTP_ERROR"
        return JSONResponse(
            status_code=error.status_code,
            content={
                "code": code,
                "reason": "入力内容を確認してください。"
                if code == "INVALID_NAME"
                else "リクエストを処理できませんでした。",
            },
            headers=error.headers,
        )

    @application.exception_handler(Exception)
    async def unexpected_error_handler(
        request: Request, error: Exception
    ) -> JSONResponse:
        """内部例外の内容を公開せず500を返す。

        Args:
            request: エラーが発生したリクエスト。
            error: 公開しない内部例外。

        Returns:
            内部詳細を含まない500応答。
        """
        return JSONResponse(
            status_code=500,
            content={
                "code": "INTERNAL_ERROR",
                "reason": "サーバーで問題が発生しました。",
            },
        )

    if static_dir is not None:
        if not (static_dir / "index.html").is_file():
            raise RuntimeError(
                "静的配信先にindex.htmlがありません。Vueをビルドしてください。"
            )

        application.mount("/", SPAStaticFiles(directory=static_dir, html=True))

    return application


static_directory = os.environ.get("STATIC_DIR")
app = create_app(static_dir=Path(static_directory) if static_directory else None)
