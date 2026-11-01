import pytest

from app_base_core.greeting import create_greeting


class TestCreateGreeting:
    def test_名前の前後の空白を除去した挨拶を返す(self) -> None:
        assert create_greeting("  ルーク  ") == "こんにちは、ルークさん！"

    @pytest.mark.parametrize("name", ["", " \t\n"], ids=["空文字", "空白文字のみ"])
    def test_空の名前なら入力エラーにする(self, name: str) -> None:
        with pytest.raises(ValueError, match="名前を入力してください"):
            create_greeting(name)
