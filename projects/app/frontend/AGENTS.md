# フロントエンドの作業指示

- Vue SFCの `<script setup lang="ts">` を使い、props・API入出力に型を付ける。`any` に逃げない。
- サーバー状態はTanStack Query、画面内だけの状態はVueの `ref`・`computed` で管理する。
- 公開関数・型・設定の目的と制約は日本語JSDocで説明する。取得Composableと表示専用部品を分け、表示部品で通信しない。
- エラー理由は既知の公開コードから共通変換し、画面が操作説明を付ける。生の例外・任意のAPI本文を表示しない。表示部品の代表状態はStorybookで確認する。
- API通信は `src/api/` へ置き、HTTP失敗と応答形式の不正を検出する。
- UIプリミティブはReka UI、スタイルはTailwind CSSを使う。ラベル・キーボード操作・ローディング・エラー状態を考慮する。
- 要素間はflex／gridの `gap-*`、内側は `p-*` で調整する。間隔調整にmarginや `space-*` を使わない。中央寄せの `mx-auto` など、既定余白のリセット、Typographyの文章組版は例外とする。
- API入出力型はフィールドを明示し、フィールド共有だけの `extends`・`Omit`・交差型を避ける。共通子オブジェクトと明確な共通仕様は例外とする。
- ESLintでLint、Prettierで整形、vue-tscで型チェックする。クラス順はPrettierに任せる。
- VitestとVue Test Utilsで振る舞いを検証する。DOMテストは実ブラウザーのE2Eの代わりとはしない。
- `describe`・`it` の説明は日本語とし、複雑なケースは日本語のGIVEN／WHEN／THENで説明する。通信境界だけを差し替え、検証対象のQuery・画面・APIクライアントは実物を使う。
- QueryClientはケースごとに作り、失敗時もunmount・キャッシュ破棄・モック復元を行う。非同期状態は完了・条件を待つAPIで確認し、固定時間の待機で代用しない。
