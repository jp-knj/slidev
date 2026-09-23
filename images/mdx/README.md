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

## スライド用の編集版

34 ページは `-clean.png` を使用する。元画像と同じ寸法で、指定領域だけを周囲と同じ背景色に変更した。タイトルと投稿者を含む、それ以外の画素は元画像と一致する。元画像と出典と確認時の状態は保管する。

| 元画像 | 編集版 | 削除した表示 |
| --- | --- | --- |
| `markdown-rs-184.png` | `markdown-rs-184-clean.png` | PR 番号と Open とマージに関する文言 |
| `markdown-rs-185.png` | `markdown-rs-185-clean.png` | PR 番号と Open とマージに関する文言 |
| `mdxjs-rs-71.png` | `mdxjs-rs-71-clean.png` | Issue 番号と Open |
| `astro-14080.png` | `astro-14080-clean.png` | PR 番号と Closed とマージに関する文言 |
| `astro-14181.png` | `astro-14181-clean.png` | PR 番号と Closed とマージに関する文言 |
| `xmdx.png` | `xmdx-clean.png` | Public archive と PR 番号とマージに関する文言 |

## スライドの出典

35 と 48 と 49 ページから削除した脚注の出典を記録する。

| ページ | 内容 | 出典 |
| --- | --- | --- |
| 35 | Astro 用 module への変換 | [load-handler.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/load-handler.ts) |
| 35 | Rust のコード生成と付随情報の取得 | [mdx_compiler.rs](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/crates/core/src/mdx_compiler.rs) |
| 35 | Node-API の受け渡し | [compiler.rs](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/crates/napi/src/compiler.rs#L399-L475) |
| 48 | Erika、2026年8月20日、Prettier plugin | [原文の投稿](https://bsky.app/profile/erika.florist/post/3mtjah7okdc22) |
| 49 | Erika、2026年4月9日、Sätteri | [原文の投稿](https://bsky.app/profile/erika.florist/post/3mj2tfwryw226) |

35 ページの実装の参照コミットは `7a89fdb17140e2b710e40d52d26338d978bc5c13`。48 と 49 ページは投稿者と投稿日と原文の引用と日本語の要約を掲載する。
