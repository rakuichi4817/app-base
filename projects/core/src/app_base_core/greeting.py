"""挨拶メッセージの生成。"""


def create_greeting(name: str) -> str:
    """前後の空白を除去して挨拶を生成する。

    Args:
        name: 挨拶の対象となる名前。

    Returns:
        日本語の挨拶メッセージ。

    Raises:
        ValueError: 名前が空白のみ、または空文字の場合。
    """
    normalized = name.strip()

    if not normalized:
        raise ValueError("名前を入力してください。")

    return f"こんにちは、{normalized}さん！"
