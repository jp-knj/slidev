# MDX の提案を紹介する画像

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

## スライドに掲載する編集版

37 と 38 ページは `-clean.png` を使用する。元画像と同じ寸法で、指定領域だけを周囲と同じ背景色に変更した。タイトルと投稿者を含む、それ以外の画素は元画像と一致する。元画像と出典と確認時の状態は保管する。

| 元画像 | 編集版 | 削除した表示 |
| --- | --- | --- |
| `markdown-rs-184.png` | `markdown-rs-184-clean.png` | PR 番号と Open とマージに関する文言 |
| `markdown-rs-185.png` | `markdown-rs-185-clean.png` | PR 番号と Open とマージに関する文言 |
| `mdxjs-rs-71.png` | `mdxjs-rs-71-clean.png` | Issue 番号と Open |
| `astro-14080.png` | `astro-14080-clean.png` | PR 番号と Closed とマージに関する文言 |
| `astro-14181.png` | `astro-14181-clean.png` | PR 番号と Closed とマージに関する文言 |
| `xmdx.png` | `xmdx-clean.png` | Public archive と PR 番号とマージに関する文言 |

## スライドの出典

39 と 48 と 50 ページの図と投稿の出典を記録する。

| ページ | 内容 | 出典 |
| --- | --- | --- |
| 39 | Astro が実行する module への変換 | [load-handler.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/load-handler.ts) |
| 39 | Rust のコード生成と付随情報の取得 | [mdx_compiler.rs](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/crates/core/src/mdx_compiler.rs) |
| 39 | Node-API の受け渡し | [compiler.rs](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/crates/napi/src/compiler.rs#L399-L475) |
| 48 | Erika、2026年8月20日、Prettier plugin | [原文の投稿](https://bsky.app/profile/erika.florist/post/3mtjah7okdc22) |
| 50 | Erika、2026年4月9日、Sätteri | [原文の投稿](https://bsky.app/profile/erika.florist/post/3mj2tfwryw226) |

39 ページの実装の参照コミットは `7a89fdb17140e2b710e40d52d26338d978bc5c13`。48 と 50 ページは投稿者と投稿日と原文の引用と日本語の要約を掲載する。


## MDX への貢献の出典

40 ページは [mdx-analyzer PR #528](https://github.com/mdx-js/mdx-analyzer/pull/528) と [Remco Haszing の告知投稿](https://bsky.app/profile/remcohaszing.nl/post/3mu5jnocvbk2r) と [貢献を紹介する返信](https://bsky.app/profile/remcohaszing.nl/post/3mu5jrfpj222r) を参照する。2026年9月24日に GitHub API と Bluesky の公開 API で照合した。PR は2026年8月25日にマージされ、返信の投稿日時は2026年8月28日14時04分 UTC である。40 ページには告知投稿と返信の画像を掲載し、改善内容の日本語説明は発表者ノートに記載する。

37 ページの upstream での開発を勧められた経緯は、[Astro PR #14181 のコメント](https://github.com/withastro/astro/pull/14181#issuecomment-3311059055) を参照する。Remco の紹介と、自作を選んだ判断は発表者の経験として記載している。37枚目から39枚目は判断の経緯に沿った説明で、提案と試作の時期には重なりがある。


## 39 枚目の関連図と 40 枚目の投稿画像

39 枚目の関連図は、同じ固定コミットの次の実装も参照する。

| 内容 | 出典 |
| --- | --- |
| Astro integration による Vite plugin の登録 | [astro-xmdx の index.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/index.ts) |
| plugin 名と hook | [vite-plugin.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin.ts) |
| @xmdx/napi のロード | [binding-loader.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/vite/src/vite-plugin/binding-loader.ts) |
| Astro 5 と Vite 6 と Rollup 4 のバージョン | [Starlight の package.json](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/examples/starlight/package.json) と [pnpm-lock.yaml](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/pnpm-lock.yaml) |

40 枚目の 2 投稿は2026年9月26日に Chromium と Playwright で実ページから別々に撮影した。投稿者とアカウント名と本文と投稿日を含み、返信には GitHub PR #528 のプレビュー全体も含む。ナビゲーションと返信入力欄と他の返信は撮影範囲から除いた。文字と表示色は変更していない。

| 画像 | 掲載位置 | 出典 | 画像の寸法 |
| --- | --- | --- | --- |
| `remco-mdx-release.png` | 左 | [告知投稿](https://bsky.app/profile/remcohaszing.nl/post/3mu5jnocvbk2r) | 1136 × 410 ピクセル |
| `remco-mdx-contribution.png` | 右 | [貢献を紹介する返信](https://bsky.app/profile/remcohaszing.nl/post/3mu5jrfpj222r) | 1136 × 1286 ピクセル |

撮影時の viewport は 1100 × 1100、deviceScaleFactor は 2、colorScheme は light。投稿要素と投稿日要素の座標から撮影範囲を指定し、投稿日直後までを PNG として保存した。画像内の投稿日は2026年8月28日で、時刻は撮影環境の日本時間で表示されている。2 列の幅は 422px、列間は 24px。画像は縦横比を維持し、幅 422px と高さ 392px を上限に全体を表示する。画像から対応する投稿を開ける。下部の出典は告知投稿と PR #528 を参照する。

`remco-mdx-editor.png` は2026年9月24日に撮影した旧画像として保管する。投稿者とアカウント名と本文を含む 1196 × 360 ピクセルの画像で、現在の 40 枚目では使用しない。

## 第 4 章の関連図の出典

2026年9月24日に公開文書と実装を確認した。章の整理に伴い、Prettier plugin の投稿は 53 枚目から 48 枚目、Sätteri の投稿は 55 枚目から 50 枚目へ移動した。原文と日付と出典は維持している。

| ページ | 内容 | 出典 |
| --- | --- | --- |
| 45 | Go 版と Rust 版の全体比較と HTML correction の方針 | [RFC #1356](https://github.com/withastro/roadmap/issues/1356) |
| 46 | 公開 API による解析と変換の呼び出し | [astro_napi](https://github.com/withastro/compiler-rs/blob/main/crates/astro_napi/src/lib.rs) |
| 46 | Astro の変換と Oxc の利用 | [Astro Codegen](https://github.com/withastro/compiler-rs/tree/main/crates/astro_codegen/src/printer) と [依存関係](https://github.com/withastro/compiler-rs/blob/main/Cargo.toml) |
| 46 | Astro のスコープ規則と Lightning CSS の利用 | [css_scoping.rs](https://github.com/withastro/compiler-rs/blob/main/crates/astro_codegen/src/css_scoping.rs) |
| 49 と 52 | Processor の分担と unified の設定 | [Astro Docs](https://docs.astro.build/en/guides/markdown-content/#markdown-processors) |
| 51 | JavaScript の API と Rust の部品 | [Sätteri の package 一覧](https://github.com/bruits/satteri#packages) |
| 51 | visitor と ctx による node の検査と変更 | [Plugin API](https://satteri.bruits.org/docs/plugin-api/) |

51 枚目では `satteri-pulldown-cmark` を pulldown-cmark、`satteri-mdxjs-rs` を mdxjs-rs と略記する。正式名と `satteri-ast`、`satteri-arena`、`satteri-plugin-api` は発表者ノートに記録した。配布方法の説明は旧 60 枚目から 46 枚目のノートへ移動した。
