# OSSライセンス

`mise run license` で各プロジェクトの既存CLIを呼び、導入済み依存を一覧保存・一次検査します。独自スクリプトや共有ポリシーファイルは使わず、ルートmiseは子タスクの集約だけを担当します。先に `mise run install` を実行してください。

| 対象 | 個別実行 | 一覧の保存先（ルート基準） |
| --- | --- | --- |
| core | `mise run //projects/core:license` | `projects/core/reports/licenses.json` |
| backend | `mise run //projects/app/backend:license` | `projects/app/backend/reports/licenses.json` |
| frontend | `mise run //projects/app/frontend:license` | `projects/app/frontend/reports/licenses.json` |

Pythonは `pip-licenses --allow-only`、frontendは `license-checker-rseidelsohn --onlyAllow` を使い、許可する表記を各miseタスクに明示します。検査前に一覧を保存するので、判定失敗時も確認できます。pip-licensesはuvのlicenseグループに分離しています。
通常の開発環境では開発依存も検査します。本番配布物だけの一覧とは区別してください。Pythonの自作パッケージとnpmのprivateパッケージは依存OSSの判定から除外しますが、自作コードの利用許諾が不要になるわけではありません。

判定は各CLIの仕様に従います。Pythonでは部分一致の `--partial-match` を使いません。frontendではSPDX式の解釈をCLIに任せるため、以前の独自処理の完全一致判定とは異なります。OR/ANDの意味と原文を確認し、不明・推測表記は一覧でレビューしてください。
これは一次検査です。汎用的な法的許可リストではなく、転用先の配布形態と組織基準で見直します。許可の追加理由はPRに記録し、単にCIを通すための一括許可はしません。

## 配布前の確認

現在のfrontendの許可には以下の条件付きライセンスも含みます。検査通過と義務履行は別なので、転用時に再審査してください。

- **MPL-2.0**：axe-core・lightningcssの開発／ビルド依存。ファイル単位のソース提供条件を配布時に確認する。
- **CC-BY-3.0**：SPDXの例外メタデータ。再配布時の帰属表示・変更表示を確認する。
- **MIT AND CC-BY-3.0**：SPDX範囲データ。両方の条件を確認し、MITだけとして扱わない。

1. 実際に配布するJS・Python依存・コンテナーベースイメージ・フォント等を特定する。
2. ライセンス原文、著作権表示、NOTICE、再配布・ソース提供等の条件を確認する。
3. 必要な本文・表示・NOTICEを成果物へ同梱し、配布物と一覧の整合を確認する。
4. 自作アプリのライセンスと元資料の再利用権限も別途確認する。

現在は一覧生成と方針検査までで、NOTICEの自動生成・Dockerへのライセンス本文同梱・OSパッケージの棚卸しは未実装です。CI成功は配布可否の法的判断や義務の充足を保証しません。
