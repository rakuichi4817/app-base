from fastapi.testclient import TestClient

from app_base_backend.main import create_app


class TestValidationErrorHandler:
    def test_入力エラーは理由コードと項目を返し入力値を公開しない(self) -> None:
        with TestClient(create_app()) as client:
            response = client.get("/api/greeting", params={"name": "secret" * 20})

        assert response.status_code == 422
        assert response.json()["code"] == "VALIDATION_ERROR"
        assert response.json()["errors"] == [
            {"field": "query.name", "code": "INVALID_VALUE"}
        ]
        assert "secret" not in response.text


class TestUnexpectedErrorHandler:
    def test_未知の内部例外を安全な500へ変換する(self) -> None:
        application = create_app()

        @application.get("/failure")
        def fail() -> None:
            raise RuntimeError("secret connection string")

        with TestClient(application, raise_server_exceptions=False) as client:
            response = client.get("/failure")

        assert response.status_code == 500
        assert response.json() == {
            "code": "INTERNAL_ERROR",
            "reason": "サーバーで問題が発生しました。",
        }
