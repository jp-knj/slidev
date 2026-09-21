17枚目から28枚目のコードとデータを再現する検証です。リポジトリのルートで実行します。

```sh
npm ci --prefix validation/chapter2 --ignore-scripts
npm run check --prefix validation/chapter2
pnpm build:compiler
pnpm lint:text
```

`verify.mjs` は三つのAstro入力を実際のツールへ渡し、結果を `results.json` に記録します。入力全文と整形結果がスライドのコードに一致することも確認します。

- Compiler 2.12.2とastro-eslint-parser 1.2.2とESLint 9.36.0
- prettier-plugin-astro 0.14.1とPrettier 3.6.2。行幅80、インデント2、LF
- TypeScript 5.9.3とHTML Language Service 5.5.2
- Language Server 2.15.5の `parseHTML` と `astro2tsx`。両ファイルの関数は、指定コミット `b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05` のソースをTypeScriptで変換して照合済み

| 確認対象 | 実測した結果 |
| --- | --- |
| Compilerが返す式の位置 | `start: 47, end: 80` |
| 式全体と変数名 | `[48, 64)` と `[49, 54)` |
| ESLint | `no-undef`。6行目の5列目から10列目 |
| Formatter | スライド23の9行の出力と一致。コロンの前後に空白を追加しない |
| HTML補完 | `<a ` の直後で `target` と `title` を取得 |
| TypeScript | `TS2339`。型にない `nmae` の診断1件 |
| TSXとAstroの対応 | `[129, 133)` と `[95, 99)`。Source mapとVolarのmappingの両方で確認 |
| Editor向けの範囲 | `line: 7` と `character: 11` から `character: 15` |

RangeはUTF-16の0始まりで終端を含みません。ESLintの行と列は1始まり、LSPの行と列は0始まりです。Virtual HTMLは文字オフセットを保持し、行番号は元のAstroと異なることを検証しています。

TypeScriptの検証にはLanguage Serverが配布する `env.d.ts` と `jsx-runtime-fallback.d.ts` を使っています。Editor全体の起動試験ではなく、補完と型診断と位置変換のAPIを呼び出す検証です。LinterのVirtual TSXは独自の変換、Language ToolのVirtual TSXはCompilerによる変換を確認しています。

2026年9月20日の確認結果です。ビルドとコード検証は成功しました。17枚目から28枚目の初期表示と全クリック状態、計26状態をブラウザで確認し、コードの横幅と本文と参考リンクの間隔を調整しました。コードの省略箇所は発表者ノートに記しています。

文章は本文と見出しと図のラベルと発表者ノートを手動で確認しました。改修範囲の既存指摘7件を解消し、プロジェクトの文章チェックと `avoid-ai-cliches-ja` は範囲内で指摘0件です。`pnpm lint:text` の全文チェックは、対象外の既存指摘130件により終了コード1になります。
