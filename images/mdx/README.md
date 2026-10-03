# MDX の提案を紹介する画像

## 2026 年 10 月 1 日の発表練習での変更

37 枚目から Astro の PR のスクリーンショットを外し、Compiler の統合と AST Bridge の二つの提案を文章で示す。元画像と撮影記録は保管する。

38 枚目のクリック 2 は bindings と配布の保守、クリック 3 は MDX の編集支援と OSS で受け取った助けの話に分ける。39 枚目は Astro への統合、40 枚目は本文と付随情報、互換性と計測条件を説明する。技術的な根拠と発話の補足は [xmdx の自作とベンチマークで分かったこと](../../xmdx-rehearsal-notes.md) にまとめた。

以下の画像記録のページ番号は、記録時点の構成に対応する。

51 枚目の口頭での導入には、[Pooya Parsa の Markdown Renderer の試作の投稿](https://bsky.app/profile/pi0.io/post/3mgwljerlik2h)を参照する。2026 年 3 月 13 日の投稿であり、画面に掲載する 4 月 9 日の Erika の Sätteri 紹介とは別。mk.gg が Discord で発表者にメンションして共有した経緯は、発表者の経験として記載する。投稿の倍率は、サイト全体のビルド時間の比較としては扱わない。

## 画像の撮影記録

2026年9月23日に GitHub の実ページを Chromium で撮影した。元画像はタイトルと投稿者と状態を含む。リポジトリの元画像は所有者と Public archive の表示を含む。元画像は変更せず保管する。

| 画像 | 出典 | 確認時の状態 |
| --- | --- | --- |
| `markdown-rs-184.png` | [markdown-rs PR #184](https://github.com/wooorm/markdown-rs/pull/184) | jp-knj、Open、未マージ |
| `markdown-rs-185.png` | [markdown-rs PR #185](https://github.com/wooorm/markdown-rs/pull/185) | jp-knj、Open、未マージ |
| `mdxjs-rs-71.png` | [mdxjs-rs Issue #71](https://github.com/wooorm/mdxjs-rs/issues/71) | jp-knj、Open |
| `astro-14080.png` | [Astro PR #14080](https://github.com/withastro/astro/pull/14080) | jp-knj、Closed、未マージ |
| `astro-14181.png` | [Astro PR #14181](https://github.com/withastro/astro/pull/14181) | jp-knj、Closed、未マージ |
| `xmdx.png` | [xmdx リポジトリ](https://github.com/jp-knj/xmdx) | 所有者 jp-knj、Public archive |

mdxjs-rs の提案は Issue と表記する。画像は確認時点の状態であり、提案時の画面ではない。

技術説明は [xmdx の固定コミット](https://github.com/jp-knj/xmdx/tree/7a89fdb17140e2b710e40d52d26338d978bc5c13) を参照する。第 4 章の原文引用と日付は、[Prettier plugin の投稿](https://bsky.app/profile/erika.florist/post/3mtjah7okdc22) と [Sätteri の投稿](https://bsky.app/profile/erika.florist/post/3mj2tfwryw226) を Bluesky の公開 API でも照合した。

## スライドに掲載する編集後の画像

38 と 39 ページは `-clean.png` を使用する。元画像と同じ寸法で、指定領域だけを周囲と同じ背景色に変更した。タイトルと投稿者を含む、それ以外の画素は元画像と一致する。元画像と出典と確認時の状態は保管する。

| 元画像 | 編集後の画像 | 削除した表示 |
| --- | --- | --- |
| `markdown-rs-184.png` | `markdown-rs-184-clean.png` | PR 番号と Open とマージに関する文言 |
| `markdown-rs-185.png` | `markdown-rs-185-clean.png` | PR 番号と Open とマージに関する文言 |
| `mdxjs-rs-71.png` | `mdxjs-rs-71-clean.png` | Issue 番号と Open |
| `astro-14080.png` | `astro-14080-clean.png` | PR 番号と Closed とマージに関する文言 |
| `astro-14181.png` | `astro-14181-clean.png` | PR 番号と Closed とマージに関する文言 |
| `xmdx.png` | `xmdx-clean.png` | Public archive と PR 番号とマージに関する文言 |

## スライドの出典

40 と 41 と 49 と 51 ページの図と投稿の出典を記録する。

| ページ | 内容 | 出典 |
| --- | --- | --- |
| 40 と 41 | Astro が実行する module への変換 | [load-handler.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/load-handler.ts) |
| 40 と 41 | Rust のコード生成と付随情報の取得 | [mdx_compiler.rs](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/crates/core/src/mdx_compiler.rs) |
| 40 と 41 | Node-API の受け渡し | [compiler.rs](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/crates/napi/src/compiler.rs#L399-L475) |
| 49 | Erika、2026年8月20日、Prettier plugin | [原文の投稿](https://bsky.app/profile/erika.florist/post/3mtjah7okdc22) |
| 51 | Erika、2026年4月9日、Sätteri | [原文の投稿](https://bsky.app/profile/erika.florist/post/3mj2tfwryw226) |

40 と 41 ページの実装の参照コミットは `7a89fdb17140e2b710e40d52d26338d978bc5c13`。49 と 51 ページは投稿者と投稿日と原文の引用と日本語の要約を掲載する。


## MDX への貢献の出典

39 ページのクリック 2 は [mdx-analyzer PR #528](https://github.com/mdx-js/mdx-analyzer/pull/528) と [Remco Haszing の告知投稿](https://bsky.app/profile/remcohaszing.nl/post/3mu5jnocvbk2r) と [貢献を紹介する返信](https://bsky.app/profile/remcohaszing.nl/post/3mu5jrfpj222r) を参照する。2026年9月24日に GitHub API と Bluesky の公開 API で照合した。PR は2026年8月25日にマージされ、返信の投稿日時は2026年8月28日14時04分 UTC である。告知投稿と返信の画像と、改善内容の短い日本語説明を掲載し、発表者ノートにも経緯を記載する。

2026年9月29日に、元の 41 枚目の MDX への貢献を upstream の提案と同じページへ統合した。初期表示は mdxjs-rs の Issue、クリック 1 は markdown-rs の二つの PR、クリック 2 はマージされた MDX の編集支援の改善と Remco の投稿を示す。同日に GitHub API で、markdown-rs の PR #184 と PR #185 は未マージ、mdx-analyzer の PR #528 はマージ済みと確認した。提案と試作には時期の重なりがあり、クリックの順序は厳密な時系列ではない。

39 枚目のノートでは、不完全な入力でも解析と編集支援を継続する必要を、ビルドと編集支援の要求の違いとして説明する。41 枚目のノートでは、互換性と Node.js からの利用方法と Astro との連携を検証したことから、採用には性能と既存機能との組み合わせと保守の分担も必要だと考察する。確認できた取り組みからの考察として記載する。

39 枚目の WASM bindings の説明に、wasm-bindgen による WASM の配布と、napi-rs によるネイティブコードの配布を比較する約 50 秒の説明を加えた。呼び出しと値の変換、OS と CPU と必要に応じた libc のビルド、実行環境での検証を説明する。2026年9月29日に [wasm-bindgen](https://wasm-bindgen.github.io/wasm-bindgen/)、[napi-rs の生成物と配布](https://napi.rs/docs/introduction/getting-started)、[napi-rs の WebAssembly と WASI](https://napi.rs/docs/concepts/webassembly) を確認した。現在の napi-rs の WASI 対応も説明し、現在の機能を PR 当時の状態として扱わない。

対象環境ごとのビルドとテストと配布も維持する範囲の広さに驚いたことを、本人が会話で述べた経験として一文加えた。[PR #182 の ChristianMurphy のコメント](https://github.com/wooorm/markdown-rs/pull/182#issuecomment-2993743993)を2026年9月29日に GitHub API で確認した。CI とローカルでのビルドとテスト、一部の環境をローカルで実行できないというコメントの発言者と、発表者本人の経験を区別する。PR #182 は他者の提案で、発表者の WASM bindings の PR #185 とは別である。

38 ページの upstream での開発を勧められた経緯は、[Astro PR #14181 のコメント](https://github.com/withastro/astro/pull/14181#issuecomment-3311059055) を参照する。Remco の紹介と、自作を選んだ判断は発表者の経験として記載している。38 枚目から 41 枚目は判断の経緯に沿った説明で、提案と試作の時期には重なりがある。


## 40 枚目の関連図と 41 枚目のデータの受け渡しと 39 枚目の投稿画像

40 枚目の関連図は、同じ固定コミットの次の実装も参照する。

| 内容 | 出典 |
| --- | --- |
| Astro integration による Vite plugin の登録 | [astro-xmdx の index.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/index.ts) |
| plugin 名と hook | [vite-plugin.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin.ts) |
| @xmdx/napi のロード | [binding-loader.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/vite/src/vite-plugin/binding-loader.ts) |
| Astro 5 と Vite 6 と Rollup 4 のバージョン | [Starlight の package.json](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/examples/starlight/package.json) と [pnpm-lock.yaml](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/pnpm-lock.yaml) |

41 枚目は、1 件の MDX ファイルが Vite plugin と Node-API bindings と Rust の Compiler を経て、Astro が実行するモジュールになる流れを示す。2026年9月29日に同じ固定コミットで確認した。生成コードと frontmatter と見出し情報を返し、JavaScript が `wrapMdxModule`、`transformPipeline`、`transformJsx` の順に実行する。図と発話では関数名を省き、Astro のモジュールへの変換、コンポーネントへの対応とシンタックスハイライト、JSX から JavaScript への変換、Vite への返却として説明する。

`load-handler.ts` は `compileMdxBatch` にファイル名とソースを 1 件渡し、`mdxResult.result.code` と `frontmatterJson` と `headings` を取得する。`frontmatterJson` は JSON 文字列で、JavaScript がオブジェクトにする。見出し情報は `depth` と `slug` と `text` を持つ。[wrapMdxModule](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/mdx-wrapper/index.ts) は、Astro のコンポーネントと `frontmatter` と `getHeadings()` と `Content` を提供するモジュールを作る。続く `runPipelineAndEsbuild` は `transformPipeline`、`transformJsx` の順に実行し、`code` と `map` を Vite へ返す。

[Node-API の公式資料](https://nodejs.org/api/n-api.html)を参照し、Node-API bindings は Node.js の JavaScript からネイティブの実装を呼び、値を受け渡す部分として説明する。この図では Rust の実装を呼ぶ。図には役割の短い説明を記載し、発話では MDX の文字列と 3 種類の戻り値を約 20 秒で説明する。

入力前の調整とキャッシュと設定値と fallback は図から省略し、MDX の変換の流れに絞る。38 枚目の AST Bridge とは別の試作であり、AST 全体を往復させる図ではない。

39 枚目のクリック 2 にある 2 投稿は2026年9月26日に Chromium と Playwright で実ページから別々に撮影した。投稿者とアカウント名と本文と投稿日を含み、返信には GitHub PR #528 のプレビュー全体も含む。ナビゲーションと返信入力欄と他の返信は撮影範囲から除いた。文字と表示色は変更していない。

| 画像 | 掲載位置 | 出典 | 画像の寸法 |
| --- | --- | --- | --- |
| `remco-mdx-release.png` | 左 | [告知投稿](https://bsky.app/profile/remcohaszing.nl/post/3mu5jnocvbk2r) | 1136 × 410 ピクセル |
| `remco-mdx-contribution.png` | 右 | [貢献を紹介する返信](https://bsky.app/profile/remcohaszing.nl/post/3mu5jrfpj222r) | 1136 × 1286 ピクセル |

撮影時の viewport は 1100 × 1100、deviceScaleFactor は 2、colorScheme は light。投稿要素と投稿日要素の座標から撮影範囲を指定し、投稿日直後までを PNG として保存した。画像内の投稿日は2026年8月28日で、時刻は撮影環境の日本時間で表示されている。2 列の幅は 422px、列間は 24px。画像は縦横比を維持し、幅 422px と高さ 392px を上限に全体を表示する。告知投稿の下には、編集支援の改善内容を記載する。画像から対応する投稿を開ける。下部の出典は告知投稿と返信と PR #528 を参照する。

`remco-mdx-editor.png` は2026年9月24日に撮影した旧画像として保管する。投稿者とアカウント名と本文を含む 1196 × 360 ピクセルの画像で、現在の 39 枚目では使用しない。

## 第 4 章の関連図の出典

2026年9月24日に公開文書と実装を確認した。2026年9月29日にデータの受け渡しの図を 41 枚目に追加し、元の 41 枚目の貢献の紹介を 39 枚目へ統合した。全体は 60 枚で、第 4 章の番号は変更前と同じ。Prettier plugin の投稿は 49 枚目、Sätteri の投稿は 51 枚目に掲載する。原文と日付と出典は維持している。

| ページ | 内容 | 出典 |
| --- | --- | --- |
| 46 | Go と Rust の全体比較と HTML correction の方針 | [RFC #1356](https://github.com/withastro/roadmap/issues/1356) |
| 47 | 公開 API による解析と変換の呼び出し | [astro_napi](https://github.com/withastro/compiler-rs/blob/main/crates/astro_napi/src/lib.rs) |
| 47 | Astro の変換と Oxc の利用 | [Astro Codegen](https://github.com/withastro/compiler-rs/tree/main/crates/astro_codegen/src/printer) と [依存関係](https://github.com/withastro/compiler-rs/blob/main/Cargo.toml) |
| 47 | Astro のスコープ規則と Lightning CSS の利用 | [css_scoping.rs](https://github.com/withastro/compiler-rs/blob/main/crates/astro_codegen/src/css_scoping.rs) |
| 50 と 53 | Processor の分担と unified の設定 | [Astro Docs](https://docs.astro.build/en/guides/markdown-content/#markdown-processors) |
| 52 | JavaScript の API と Rust の部品 | [Sätteri の package 一覧](https://github.com/bruits/satteri#packages) |
| 52 | visitor と ctx による node の検査と変更 | [Plugin API](https://satteri.bruits.org/docs/plugin-api/) |

52 枚目では `satteri-pulldown-cmark` を pulldown-cmark、`satteri-mdxjs-rs` を mdxjs-rs と略記する。正式名と `satteri-ast`、`satteri-arena`、`satteri-plugin-api` は発表者ノートに記録した。配布方法の説明は旧 60 枚目から 47 枚目のノートへ移動した。

52 枚目の発話には、40 枚目と 41 枚目の xmdx の MDX 統合と、Sätteri のプラグインの仕組みとの比較を加えた。生成コードと付随情報を受け取って Astro の実行形式にする JavaScript の担当と、Rust が保持する AST の node を参照して変更を依頼する担当を比較する。パッケージ全体の機能の比較ではない。2026年9月29日に [Sätteri の node の参照と変更](https://satteri.bruits.org/docs/plugin-api/#node-lifetime) と [Node-API](https://nodejs.org/api/n-api.html) を再確認した。Node-API はネイティブの実装と Node.js の呼び出しや値の受け渡しを支える API で、受け渡す情報は実装が決める。
