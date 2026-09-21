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
| 正常なexpressionのESLint診断 | `price * amount` は診断0件 |
| Compilerが返すAstro expressionの位置 | `start: 47, end: 80` |
| Astro expressionの範囲と変数名 | `[48, 64)` と `[49, 54)` |
| ESLint | `no-undef`。6行目の5列目から10列目 |
| Formatter | 24枚目の9行の出力と一致。コロンの前後に空白を追加しない |
| HTML補完 | `<a ` の直後で `target` と `title` を取得 |
| TypeScript | `TS2339`。型にない `nmae` の診断1件 |
| TSXとAstroの対応 | `[129, 133)` と `[95, 99)`。Source mapとVolarのmappingの両方で確認 |
| Editor向けの範囲 | `line: 7` と `character: 11` から `character: 15` |

ツールが使うRangeはUTF-16の0始まりで終端を含みません。Compilerの位置との比較にはASCIIの例を使っており、UTF-8のbyteとUTF-16の値が一致します。ESLintの行と列は1始まり、LSPの行と列は0始まりです。Virtual HTMLは文字オフセットを保持し、行番号は元のAstroと異なることを検証しています。

TypeScriptの検証にはLanguage Serverが配布する `env.d.ts` と `jsx-runtime-fallback.d.ts` を使っています。Editor全体の起動試験ではなく、補完と型診断と位置変換のAPIを呼び出す検証です。LinterのVirtual TSXは独自の変換、Language ToolのVirtual TSXはCompilerによる変換を確認しています。

正常なexpressionの `expression.astro` を19枚目と20枚目と21枚目で使い、誤記を含む `linter.astro` は22枚目で使います。公開ASTのexpressionの中身が文字列であることと、Astro expressionの補正後の範囲と、JavaScript ASTの識別子の範囲と、正常なexpressionの診断0件を確認します。誤記の初登場がLinterの最後の例であることも検査します。

17枚目のAPIの役割分担は、architectureの資料が対象とするCompiler 3.0.0を参照しています。コードと位置の実測は上記の2.12.2で行います。両版で `parse()` と `convertToTSX()` はLiteral modeを指定し、`transform()` は指定しません。

2026年9月21日、15枚目から28枚目の初期表示と全クリック状態、計28状態をブラウザで確認しました。総枚数は82枚です。入れ子の色分けと、フローの矢印と、誤記の波線と、文字の折り返しを確認しています。

コード検証とビルドは成功しました。変更範囲の文章チェックは、プロジェクトの検査と `avoid-ai-cliches-ja` の両方で指摘0件です。`pnpm lint:text` の全文チェックは、対象外の既存指摘128件により終了コード1になります。


2026年9月21日、expression表記の統一と第3章の再編後に再検証しました。以下は総枚数63枚での記録です。上の82枚での記録とは区別します。

SlidevのParserで63枚と確認しました。旧30枚目から56枚目を新30枚目から37枚目の8枚へ再編し、旧57枚目のOverviewが新38枚目と一致することを確認しています。発表時間は40分のままです。第4章以降の順序も維持しています。ノートの案内は新38枚目に合わせました。

ブラウザでは、次の22枚の初期表示と全クリック状態、計46状態を確認しました。追加クリック数は初期表示を含みません。

| 確認ページ | 追加クリック数 | 確認状態数 |
| --- | --- | --- |
| 13 | 4 | 5 |
| 17 | 0 | 1 |
| 18 | 3 | 4 |
| 19 | 0 | 1 |
| 20 | 2 | 3 |
| 21 | 0 | 1 |
| 23 | 2 | 3 |
| 24 | 0 | 1 |
| 27 | 3 | 4 |
| 28 | 0 | 1 |
| 30と31 | 各1 | 4 |
| 32から36 | 各0 | 5 |
| 37 | 1 | 2 |
| 43 | 1 | 2 |
| 45と46と56 | 各2 | 9 |

新30枚目から37枚目は計11状態です。30枚目と37枚目は1クリックで副題を表示し、次の操作で31枚目と38枚目へ進むことを確認しました。空白ページと不要なクリックはありません。変更ページの文字の折り返し、図との重なり、はみ出しを目視と要素の座標で確認しました。27枚目の改行と28枚目の小文字表記を調整し、新33枚目のラベルを黒に揃えています。ASTの枝と入れ子のガイドも維持しています。

OxcのparseSyncの呼び出し方は[Parserの資料](https://oxc.rs/docs/guide/usage/parser.html)、CSTとwhileの例は[Biomeの設計資料](https://biomejs.dev/internals/architecture/)と照合しました。[Astro SyntaxのDraft](https://github.com/withastro/compiler/blob/04170031ce2f30d1882fe480e87998197e0016aa/SYNTAX_SPEC.md)は2026年2月3日付のコミットに固定しています。各PRとIssueの内容も一次資料で確認し、AstroのPR #14080とPR #14181はいずれも未マージでcloseされていることをGitHub APIで確認しました。

`npm run check --prefix validation/chapter2` と `pnpm build:compiler` は成功しました。ASTと範囲と診断とFormatterの実測結果に変更はありません。再編範囲外のコードフェンスは変更前と一致し、`pirce` の初登場は22枚目のままです。`[48, 64)` は波かっこを含むAstro expressionの範囲、`[49, 54)` は `price` の範囲として維持しています。

変更した本文とノートは、プロジェクトの文章検査と `avoid-ai-cliches-ja` の両方で指摘0件です。`pnpm lint:text` の全文検査は、対象外の既存指摘85件により終了コード1になります。この85件は今回の追加行には含まれません。新しい8枚の全文も指摘0件です。
