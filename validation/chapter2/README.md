19枚目から26枚目のコードとデータを再現する検証です。リポジトリのルートで実行します。

```sh
npm ci --prefix validation/chapter2 --ignore-scripts
npm run check --prefix validation/chapter2
pnpm build:compiler
pnpm lint:text
```

`verify.mjs` は四つのAstro入力を実際のツールへ渡し、結果を `results.json` に記録します。入力全文と整形結果がスライドのコードに一致することも確認します。

- Compiler 2.12.2とastro-eslint-parser 1.2.2とESLint 9.36.0
- prettier-plugin-astro 0.14.1とPrettier 3.6.2。行幅80、インデント2、LF
- TypeScript 5.9.3とHTML Language Service 5.5.2
- Language Server 2.15.5の `parseHTML` と `astro2tsx`。両ファイルの関数は、指定コミット `b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05` のソースをTypeScriptで変換して照合済み

| 確認対象 | 実測した結果 |
| --- | --- |
| 正常な式のESLint診断 | `price * amount` は診断0件 |
| Compilerが返す式の位置 | `start: 47, end: 80` |
| 式全体と変数名 | `[48, 64)` と `[49, 54)` |
| ESLint | `no-undef`。6行目の5列目から10列目 |
| Formatter | 24枚目の9行の出力と一致。コロンの前後に空白を追加しない |
| HTML補完 | `<a ` の直後で `target` と `title` を取得 |
| TypeScript | `TS2339`。型にない `nmae` の診断1件 |
| TSXとAstroの対応 | `[129, 133)` と `[95, 99)`。Source mapとVolarのmappingの両方で確認 |
| Editor向けの範囲 | `line: 7` と `character: 11` から `character: 15` |

ツールが使うRangeはUTF-16の0始まりで終端を含みません。Compilerの位置との比較にはASCIIの例を使っており、UTF-8のbyteとUTF-16の値が一致します。ESLintの行と列は1始まり、LSPの行と列は0始まりです。Virtual HTMLは文字オフセットを保持し、行番号は元のAstroと異なることを検証しています。

TypeScriptの検証にはLanguage Serverが配布する `env.d.ts` と `jsx-runtime-fallback.d.ts` を使っています。Editor全体の起動試験ではなく、補完と型診断と位置変換のAPIを呼び出す検証です。LinterのVirtual TSXは独自の変換、Language ToolのVirtual TSXはCompilerによる変換を確認しています。

正常な式の `expression.astro` を19枚目と20枚目と21枚目で使い、誤記を含む `linter.astro` は22枚目で使います。公開ASTの式が文字列であることと、式の補正後の範囲と、JavaScript ASTの識別子の範囲と、正常な式の診断0件を確認します。誤記の初登場がLinterの最後の例であることも検査します。

17枚目のAPIの役割分担は、architectureの資料が対象とするCompiler 3.0.0を参照しています。コードと位置の実測は上記の2.12.2で行います。両版で `parse()` と `convertToTSX()` はLiteral modeを指定し、`transform()` は指定しません。

2026年9月21日、15枚目から28枚目の初期表示と全クリック状態、計28状態をブラウザで確認しました。総枚数は82枚です。入れ子の色分けと、フローの矢印と、誤記の波線と、文字の折り返しを確認しています。

コード検証とビルドは成功しました。変更範囲の文章チェックは、プロジェクトの検査と `avoid-ai-cliches-ja` の両方で指摘0件です。`pnpm lint:text` の全文チェックは、対象外の既存指摘128件により終了コード1になります。
