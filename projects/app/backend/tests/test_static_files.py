from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app_base_backend.main import create_app


@pytest.fixture
def static_client(tmp_path: Path) -> Iterator[TestClient]:
    (tmp_path / "index.html").write_text("<html>App Base</html>", encoding="utf-8")
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets" / "app.js").write_text("// Vue asset", encoding="utf-8")

    with TestClient(create_app(static_dir=tmp_path)) as client:
        yield client


class TestSPAStaticFilesGetResponse:
    @pytest.mark.parametrize(
        "path", ["/", "/pilots/luke"], ids=["ルート", "深い画面パス"]
    )
    @pytest.mark.parametrize("method", ["GET", "HEAD"])
    def test_画面への直接アクセスは入口のHTMLを返す(
        self, static_client: TestClient, path: str, method: str
    ) -> None:
        response = static_client.request(method, path)

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")
        assert response.text == ("<html>App Base</html>" if method == "GET" else "")

    @pytest.mark.parametrize(
        "path",
        ["/api", "/api/missing", "/assets/missing", "/missing.js"],
        ids=["APIルート", "未配置API", "未配置アセット", "拡張子付きパス"],
    )
    def test_未配置のAPIとアセットはHTMLで隠さず404を返す(
        self, static_client: TestClient, path: str
    ) -> None:
        response = static_client.get(path)

        assert response.status_code == 404
        assert response.headers["content-type"].startswith("application/json")

    def test_既存のAPIとアセットはそのまま配信する(
        self, static_client: TestClient
    ) -> None:
        response = static_client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

        response = static_client.get("/assets/app.js")
        assert response.status_code == 200
        assert response.text == "// Vue asset"

    def test_POSTはHTMLへ置き換えず405を返す(self, static_client: TestClient) -> None:
        assert static_client.post("/pilots/luke").status_code == 405


class TestCreateApp:
    def test_静的配信未設定なら画面は404を返す(self) -> None:
        with TestClient(create_app()) as client:
            assert client.get("/pilots/luke").status_code == 404

    def test_ビルド成果物がなければアプリ生成時に失敗する(self, tmp_path: Path) -> None:
        with pytest.raises(RuntimeError, match="index.html"):
            create_app(static_dir=tmp_path)
