"""API・アセットの404を維持し、画面への直接アクセスをSPAへ引き継ぐ。"""

from pathlib import PurePosixPath

from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.types import Scope


class SPAStaticFiles(StaticFiles):
    """実ファイルを優先し、拡張子のない画面パスだけをHTMLへフォールバックする。"""

    async def get_response(self, path: str, scope: Scope) -> Response:
        """実ファイル、または画面の入口となるindex.htmlを返す。

        Args:
            path: StaticFilesが正規化した相対パス。
            scope: ASGIリクエストの情報。

        Returns:
            静的ファイルまたは画面HTMLの応答。

        Raises:
            HTTPException: API・アセット・拡張子付きパスが未配置の場合、
                または配信時に404以外のHTTPエラーが発生した場合。
        """
        first_segment = path.split("/", 1)[0]

        if first_segment == "api":
            raise HTTPException(status_code=404)

        try:
            response = await super().get_response(path, scope)
        except HTTPException as error:
            if error.status_code != 404:
                raise
        else:
            if response.status_code != 404:
                return response

        if first_segment == "assets" or PurePosixPath(path).suffix:
            raise HTTPException(status_code=404)

        return await super().get_response("index.html", scope)
