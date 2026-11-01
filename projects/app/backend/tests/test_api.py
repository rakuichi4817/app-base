import pytest
from fastapi.testclient import TestClient

from app_base_backend.main import create_app


class TestHealth:
    def test_ヘルスチェックは稼働状態を返す(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/api/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestGreeting:
    def test_名前を渡すとcoreで生成した挨拶を返す(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/api/greeting", params={"name": " レイア "})

        assert response.status_code == 200
        assert response.json() == {"message": "こんにちは、レイアさん！"}

    @pytest.mark.parametrize(
        "name", ["", "   ", "a" * 81], ids=["空文字", "空白のみ", "上限超過"]
    )
    def test_不正な名前には422を返す(self, name: str) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/api/greeting", params={"name": name})

        assert response.status_code == 422
