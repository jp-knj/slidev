---
theme: ./theme-light
author: jp-knj
title: Astro と Rust で考えるフロントエンドツールチェーンの今
info: |
  動いていた Go Compiler を、Astro はなぜ Rust で書き直したのか。
  当時の判断と発見した問題と前提の変化と新しい判断の4章で、歴史を読み解く。
duration: 25min
mdc: true
transition: fade
colorSchema: light
themeConfig:
  primary: "#bc52ee"
layout: center-vertical
class: text-center
---

<h1 class="!text-5xl !font-700 leading-tight">
  Astro と Rust で考える<br />フロントエンドツールチェーンの今
</h1>

<div class="text-2xl text-black mt-10">Vue Fes 2026</div>

<div class="text-2xl text-black mt-3">kenji(jp-knj)</div>

<!--
予定時間 00:00 から 00:15（15 秒）。発話 90 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

こんにちは、kenji です。今日は Astro Compiler を題材に、動いていたツールをなぜ書き直すのかを考えます。実装言語に加えて、必要な情報と、利用できる基盤の変化を追います。


-->

---
class: flex items-center justify-center h-full
---

<div class="grid grid-cols-2 gap-10">
  <div>
    <div class="flex items-center gap-4">
      <img src="./images/profile.jpeg" class="w-24 rounded-full" alt="profile" />
      <div class="flex flex-col justify-center gap-0">
        <p class="text-2xl !my-0">ケンジ</p>
        <p class="text-xl !my-0">GitHub: <a href="https://github.com/jp-knj">jp-knj</a></p>
      </div>
    </div>
  </div>
  <div>
    <ul class="text-xl">
      <li>Astro Maintainer</li>
      <li>Astro Japan Community</li>
    </ul>
  </div>
</div>

<!--
改稿前の予定時間 00:15 から 00:25（10 秒）。発話 51 文字。練習での発話に基づいて改稿した。時間配分は再調整する。実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

ケンジです。Astro のメンテナをしています。Astro Japan Community も運営しています。

### 確認メモ（発表では話さない）

自己紹介は本人が共有した内容に限定する。

### 出典と確認資料（発表では話さない）

- [jp-knj](https://github.com/jp-knj)
-->

---
layout: default
class: community-story
---

## Vue Fes 2025 から Astro Japan Community へ

<ol class="community-thread" data-community-step="thread">
  <li class="thread-post thread-continues">
    <span class="thread-avatar avatar-pilcrow" aria-hidden="true"></span>
    <div>
      <p class="thread-meta"><b>pilcrow</b> @pilcrowonpaper</p>
      <p class="thread-text">Why isn’t anyone from @astrodotbuild here at @vuefes :(</p>
    </div>
  </li>
  <li class="thread-post thread-continues">
    <span class="thread-avatar avatar-astro" aria-hidden="true"></span>
    <div>
      <p class="thread-meta"><b>Astro</b> @astrodotbuild</p>
      <p class="thread-text">@jp_knj was there!</p>
    </div>
  </li>
  <li class="thread-post thread-continues">
    <span class="thread-avatar avatar-pilcrow" aria-hidden="true"></span>
    <div>
      <p class="thread-meta"><b>pilcrow</b> @pilcrowonpaper</p>
      <p class="thread-text">We need more people!</p>
    </div>
  </li>
  <li class="thread-post">
    <span class="thread-avatar avatar-astro" aria-hidden="true"></span>
    <div>
      <p class="thread-meta"><b>Astro</b> @astrodotbuild</p>
      <p class="thread-text">Who is organizing Astro meetups in Japan?</p>
    </div>
  </li>
</ol>

<!--
改稿前の予定時間 00:25 から 00:45（20 秒）。発話 200 文字。練習での発話に基づいて改稿した。時間配分は再調整する。実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。引用全文の朗読はしない。発話後に次へ進む。

### 発話

実は、このコミュニティを立ち上げたきっかけが、去年の Vue Fes だったんですね。
この投稿をした pilcrow は学生で、認証ライブラリの Lucia を開発した人です。Astro の認証まわりにも貢献しています。
その pilcrow が、Vue Fes に Astro の人はいないのか、と投稿したんです。そこから Astro 公式も交えて、もっと人が必要だよね、日本の Meetup は誰がやるんだろう、という話になりました。

### 確認メモ（発表では話さない）

学生という紹介は、発表者が今回の練習で共有した内容に基づく。Lucia は認証ライブラリとしての活動を紹介する。Astro との関係は、本人が公開した Astro DB adapter などで確認できる。
画面の投稿は原文の引用。投稿の日時と出典と画像の撮影方法は images/community/README.md を参照する。

### 出典と確認資料（発表では話さない）

- [2025-10-25 16:12](https://x.com/pilcrowonpaper/status/1981982063650812385)
- [2025-10-26 04:02](https://x.com/astrodotbuild/status/1982160958450520242)
- [2025-10-26 10:32](https://x.com/pilcrowonpaper/status/1982259070112292924)
- [2025-10-27 01:25](https://x.com/astrodotbuild/status/1982483654858441181)
- [pilcrow の GitHub](https://github.com/pilcrowonpaper)
- [Lucia と Astro DB を組み合わせる実装](https://github.com/pilcrowonpaper/lucia-adapter-astrodb)
- [Lucia の Astro での利用例](https://v2.lucia-auth.com/getting-started/astro/)
-->

---
layout: default
class: community-story
---

## Vue Fes 2025 から Astro Japan Community へ

<div class="community-state" data-community-step="meetup">
  <a class="community-post" href="https://x.com/PLAID_Tech/status/1991667457032089615" target="_blank" rel="noreferrer" aria-label="PLAID の開催告知を開く">
    <img src="./images/community/plaid-meetup.png" alt="PLAID の開催告知。コミュニティを設立し、PLAID で Meetup を開催。投稿者とアカウント名と本文と投稿日を含む。添付の開催告知画像も含む。" />
  </a>
  <p class="community-caption">コミュニティを設立し、PLAID で Meetup を開催</p>
  <a class="community-source" href="https://x.com/PLAID_Tech/status/1991667457032089615" target="_blank" rel="noreferrer">PLAID の開催告知を見る</a>
</div>

<!--
改稿前の予定時間 00:45 から 00:55（10 秒）。発話 93 文字。練習での発話に基づいて改稿した。時間配分は再調整する。実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

そこで僕が手を挙げて、Astro Japan Community を立ち上げました。その後、Meetup も開催しています。
そのきっかけになった Vue Fes に、今年は登壇者として参加しています。

### 確認メモ（発表では話さない）

投稿の日時と出典と画像の撮影方法は images/community/README.md を参照する。

### 出典と確認資料（発表では話さない）

- [PLAID の開催告知](https://x.com/PLAID_Tech/status/1991667457032089615)
-->

---
layout: statement
class: flex flex-col justify-center h-full
---

# Go で動いていたものを、<br />なぜ、Rust に書き直すのか？

<!--
予定時間 00:55 から 01:05（10 秒）。発話 49 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Go で動いていたものを、なぜ Rust に書き直すのか。今日の問いです。要件と設計の判断から考えます。


-->

---
layout: default
class: body-center
---

## 話すこと

<div class="grid grid-cols-1 gap-4 mt-10">
  <div>
    <div class="text-3xl font-600 mt-1" style="color: var(--astro-heading)">1. 当時の判断</div>
    <div class="text-lg mt-2">なぜ最初に Go と WASM を選んだのか</div>
  </div>
  <div>
    <div class="text-3xl font-600 mt-1" style="color: var(--astro-heading)">2. 発見した問題</div>
    <div class="text-lg mt-2">使い続けるなかで何が見えたのか</div>
  </div>
  <div>
    <div class="text-3xl font-600 mt-1" style="color: var(--astro-heading)">3. 前提の変化</div>
    <div class="text-lg mt-2">2026年までに周囲はどう変わったのか</div>
  </div>
  <div>
    <div class="text-3xl font-600 mt-1" style="color: var(--astro-heading)">4. 新しい判断</div>
    <div class="text-lg mt-2">その結果、責務をどう分け直したのか</div>
  </div>
</div>

<!--
予定時間 01:05 から 01:15（10 秒）。発話 38 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

当時の判断、発見した問題、前提の変化、新しい判断。この四つを順に確認します。


-->

---
layout: section
---

# 1. 当時の判断
## なぜ最初に Go と WASM を選んだのか

<!--
予定時間 01:15 から 01:20（5 秒）。発話 22 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

まず、Go と WASM を選んだときの条件です。
-->

---
layout: center
---

<Overview
  visible="source,compiler,build,browser"
  :labels="{ compiler: 'Svelte Compiler', build: 'Snowpack' }"
  :icons="{ compiler: 'svelte', build: 'snowpack' }"
/>

<div class="text-center text-xl mt-2">Astro 0.x の出発点</div>



<!--
改稿前の予定時間 01:20 から 01:35（15 秒）。発話 172 文字。Snowpack の説明を追加した。改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

初期の Astro は、Svelte Compiler の fork で Astro のコードを解析していました。その先のビルドを担当したのが Snowpack です。
Snowpack はフロントエンドのビルドツールで、開発サーバーから JavaScript や CSS をブラウザへ配信します。開発中は、変更したファイルを個別に更新できます。
この全体図に、あとで戻ります。

### 確認メモ（発表では話さない）

Svelte の fork は Compiler の実装。Snowpack はビルドを担当する。
配信は開発サーバーからブラウザへのファイル配信を指す。Snowpack の開発中の動作を説明し、本番環境でのサイト公開やホスティングとは区別する。
CultRepo の VITE: The Documentary は確認資料。動画の概要欄で、7 分 40 秒から Snowpack との比較、20 分 21 秒から Astro の Vite 採用を扱うことを確認した。8 枚目の画面には動画のリンクを表示しない。Vite の採用経緯は 10 枚目のトークスクリプトで話す。

### 話す場合の補足（任意）

ちなみに、Astro の Fred は Snowpack のメンテナでもありました。それでも、Astro のビルド基盤には Vite を選び直しています。Vite の改善や Rollup のプラグインを、Astro でも利用できるようになるからです。

### 補足の確認事項（発表では話さない）

Fred Schott と Drew Powers は、当時 Astro と Snowpack の両方のメンテナだった。Fred が執筆した Astro 0.21 の紹介記事で確認できる。
Snowpack と Vite は、図の Build の役割を担う基盤。Astro 0.21 では、ビルド基盤を Snowpack から Vite へ移行した。同時期に行った、Svelte Compiler の fork から Go Compiler への移行とは担当が異なる。
Vite の採用理由として、当時の記事は保守と資料の充実、性能、エラーメッセージ、コミュニティと Rollup のプラグインを挙げている。改善を複数のフレームワークで共有できることも説明している。
この補足は、利用できる基盤を選び直すという講演の主題につながる。人物紹介を詳説する必要はなく、本編の時間に合わせて省略できる。任意の補足は発話文字数に含めていない。

### 出典と確認資料（発表では話さない）

- [Fred による Snowpack から Vite への移行の説明](https://astro.build/blog/astro-021-preview/)
- [VITE: The Documentary（CultRepo）](https://www.youtube.com/watch?v=bmWQqAKLgT4)
- [Astro が Vite を採用した経緯（20 分 21 秒から）](https://www.youtube.com/watch?v=bmWQqAKLgT4&t=1221s)
- [Astro 初期の Compiler とビルド基盤](https://astro.build/blog/astro-021-release/)
- [Snowpack の開発サーバー](https://www.snowpack.dev/concepts/dev-server)
- [Snowpack のファイル単位の更新](https://www.snowpack.dev/concepts/how-snowpack-works)
-->

---
layout: default
class: body-center
---

## 2021年は、Rust 一色ではなかった

<div class="mt-12 relative">

  <!-- 軸。ドットの中心（上から 50px）に合わせて引く -->
  <div class="absolute left-0 right-0 top-[50px] h-[2px] bg-[#D9D3E2]"></div>

  <div class="relative flex items-start">
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Feb</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-vitejs class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Vite 2.0</div>
      <img src="./images/logos/gopher-classic.png" alt="Go" class="h-16 mt-6" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Sep</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-rome-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Rome</div>
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-11 mt-9" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Oct</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-parcel-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Parcel 2</div>
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-11 mt-9" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Oct</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-nextjs-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Next.js 12</div>
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-11 mt-9" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-primary font-700 h-11 leading-none">Nov</div>
      <div class="w-5 h-5 rounded-full bg-[#BC52EE] -mt-[3px]"></div>
      <logos-astro-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug text-primary font-600">Astro 0.21</div>
      <img src="./images/logos/gopher-classic.png" alt="Go" class="h-16 mt-6" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Dec</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-turborepo-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Turborepo</div>
      <img src="./images/logos/gopher-classic.png" alt="Go" class="h-16 mt-6" />
    </div>
  </div>
</div>

<!--
予定時間 01:35 から 01:50（15 秒）。発話 79 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

2021 年は Rust の採用が増えた年ですが、Go の選択肢もありました。Vite が利用した esbuild と、当時の Turborepo は Go で実装されていました。

### 確認メモ（発表では話さない）

Vite 自体を Go で実装したという説明ではない。製品の採用時期は既存の参照資料に基づく。
-->

---
layout: default
class: go-era-slide go-era-build
---

<div class="go-era-heading">
  <h2>Astro v1</h2>
  <span class="go-era-year">2022年</span>
</div>

<div class="go-era-body">
  <div class="go-era-summary">Build のための Compiler だった</div>

  <Overview
    visible="source,compiler,build,browser"
    era="go"
    :subnotes="{ build: 'Rollup\nesbuild' }"
  />

  <div class="go-era-reason">
    <div class="text-2xl font-600 text-primary">深く考えすぎずに選んだ</div>
    <div class="text-xl mt-2">esbuild が Go だった。Go は学びやすかった。</div>
  </div>
</div>

<Ref>
  <a class="block w-fit" href="https://natemoo.re/posts/hello-from-the-other-side/" target="_blank" rel="noreferrer">Nate Moore: Hello from the other side</a>
  <a class="block w-fit mt-1" href="https://www.youtube.com/watch?v=bmWQqAKLgT4&amp;t=1221s" target="_blank" rel="noreferrer">VITE: The Documentary（Astro の Vite 採用は 20:21 から）</a>
</Ref>

<!--
予定時間 01:50 から 02:20（30 秒）。発話 167 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Astro は Go Compiler と Vite に移行しました。JavaScript からは WASM を介して Compiler を呼びます。Nate Moore が挙げた Go の選定理由は、esbuild が Go だったことと、学びやすかったことです。
Compiler は Astro のコードを変換し、Vite につなぎます。Parser は Go 公式の HTML5 Parser の fork で、CSS の解析には esbuild の CSS Parser を取り込んでいます。一方で、JavaScript を完全にパースする仕組みは持っていません。

### 確認メモ（発表では話さない）

Go の経験者だったという理由へ変更しない。Compiler 内の esbuild は CSS の解析と生成、Vite の部分の esbuild は TypeScript の変換を担当する。HTML5 Parser 由来の実装を Astro syntax に対応させた。原文は "esbuild was written in Go and it was easy to learn. We didn't overthink it." で、深い技術的判断として語らない。`internal/parser.go` と `internal/token.go` は `golang.org/x/net/html` の fork（Copyright The Go Authors）。JavaScript は `tdewolff/parse` による走査（`internal/js_scanner`）だけで、完全な JS Parser はない。

### 出典と確認資料（発表では話さない）

- [esbuild の CSS Parser の導入](https://github.com/withastro/compiler/pull/329)
- [Astro v1 の Vite plugin](https://github.com/withastro/astro/blob/astro%401.0.0/packages/astro/src/vite-plugin-astro/index.ts)
- [Go Compiler と Vite を採用した Astro v0.21](https://astro.build/blog/astro-021-release/)
- [Nate Moore: Hello from the other side](https://natemoo.re/posts/hello-from-the-other-side/)
-->

---
layout: section
---

# 2. 発見した問題
## 使い続けるなかで何が見えたのか

<!--
予定時間 02:20 から 02:25（5 秒）。発話 22 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

使い続けるなかで、何が分かったのでしょうか。
-->

---
layout: default
class: go-era-slide go-era-tools
---

<div class="go-era-heading">
  <h2>Astro v2〜v5</h2>
  <span class="go-era-year">2023〜2025年</span>
</div>

<div class="go-era-summary">Astro を使う人が増えていった</div>

<Overview
  era="go"
/>

<!--
発話 182 文字。利用の広がりと構文の例への案内に改稿した。改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

この時期、Astro を使う人も増えていきました。GitHub の Octoverse 2025 でも、Astro が成長率の高い言語の一つとして紹介されています。ここで数えているのは、1 か月の間に Astro のコードにコントリビュートした人の数です。前年の同じ月から、78% を超えて増えています。
まずは、利用者が Astro の構文に何を期待し、実際にどう動いたのかを確認します。

### 確認メモ（発表では話さない）

成長率は Octoverse 2025 の言語別集計に基づく。月間の貢献者が 1,000 人以上の言語を対象とし、2024 年 8 月と 2025 年 8 月を比較する。Astro のコードにコントリビュートした人の数を月ごとに集計した指標。コントリビュートの回数やコミットの回数は示さない。Astro の利用者全体を数えた統計ではなく、利用の広がりを示す一つの指標として紹介する。Astro 本体の開発者数や GitHub のスター数を示す値ではない。言語の分類には Linguist を使う。
成長の指標は、Astro を使う開発の広がりを示す資料として紹介する。利用の増加が Compiler の書き直しの直接の理由だという説明はしない。
図は Astro v2 から v5 の時期の役割をまとめたもの。Editor のツールや MDX がすべて v2 で初めて登場したという意味ではない。

### 出典と確認資料（発表では話さない）

- [GitHub Octoverse 2025 の言語別成長率と集計方法](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- [Astro v1 の MDX 対応](https://astro.build/blog/astro-1/)
- [Astro v2 の Content Collections](https://astro.build/blog/astro-2/)
- [Astro v5 の TypeScript 変換](https://github.com/withastro/astro/blob/astro%405.0.0/packages/astro/src/vite-plugin-astro/compile.ts)
-->

---
layout: default
class: syntax-overview body-center
clicks: 6
---

## Astro Syntax

````md magic-move
```astro
---
const products = await getProducts();
---
```
```astro
---
const products = await getProducts();
---

<ul>
  <!-- template -->
</ul>
```
```astro
---
const products = await getProducts();
---

<ul>
  {products.map((product) => (
    <li>{product.name}: {product.price}</li>
  ))}
</ul>
```
```astro {3,7}
---
const products = await getProducts();
const props = { title: "second" };
---
<ul>
  {products.map((product) => (
    <li title="first" {...props}>{product.name}</li>
  ))}
</ul>
```
````

<div class="mt-0 text-center text-2xl">
  <div v-if="$clicks === 0"><span class="text-primary font-600">Component script</span><br /><code>---</code> で囲む。ビルド時とサーバーで実行する JavaScript と TypeScript</div>
  <div v-if="$clicks === 1"><span class="text-primary font-600">Template</span><br />HTML を基礎に、JavaScript expression や<br />コンポーネントを書ける</div>
  <div v-if="$clicks === 2"><span class="text-primary font-600">JavaScript expression（式）</span><br />波かっこの中の JavaScript expression を評価し、結果を表示する<br />Astro の書き方って、JSX っぽいですよね。</div>
  <div v-if="$clicks === 3"><span class="text-primary font-600">Q. </span>この <code>title</code> は、どちらの値になる？</div>
  <div v-if="$clicks === 3" class="mt-4"><code>first</code> か、<code>second</code> か</div>
  <div v-if="$clicks === 4"><span class="text-primary font-600">A. </span><code>first</code></div>
  <Overlay v-if="$clicks >= 5" aria-label="Astro Syntax への問いと答え">
    <template #title>
      <span v-if="$clicks === 5">JSX なら second。なぜ first になった？</span>
      <span v-else>重複した属性を HTML の規則で扱ったため</span>
    </template>
    <p v-if="$clicks >= 6">
      この報告では、Astro が同じ属性を二つ出力した。<br />
      ブラウザは HTML の規則で先の <code>title="first"</code> を採用した。
    </p>
    <template v-if="$clicks >= 6" #reference>
      <a href="https://html.spec.whatwg.org/multipage/parsing.html#attribute-name-state" target="_blank" rel="noopener noreferrer">HTML Standard：同じ名前の属性は後のものを取り除く</a>
    </template>
  </Overlay>
</div>

<Ref v-if="$clicks < 3" href="https://docs.astro.build/en/reference/astro-syntax/">Astro Syntax</Ref>
<Ref v-if="$clicks === 4" href="https://github.com/withastro/astro/issues/5558#issuecomment-1343799494">astro#5558 の説明</Ref>

<!--
予定時間 02:40 から 03:15（35 秒）。発話 248 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

クリック 3 の問いで長く待たず、1 秒ほどで答えへ進む。6 回のクリックを発話に合わせる。

### 発話

[初期表示]
Astro は、上の三本線の中にスクリプトを書きます。
[クリック 1]
下は HTML を基礎とした記述です。
[クリック 2]
波かっこの中にあるのが JavaScript expression、JavaScript の式です。これを評価して、その結果を表示します。
[クリック 3]
ここで、title は first と second のどちらでしょう。
[クリック 4]
当時の答えは first でした。
[クリック 5]
なぜでしょうか。
[クリック 6]
それ、ブラウザの解釈です。同じ属性を二つ出力し、ブラウザが先の属性を採用しました。HTML の仕様では、同じ名前の属性は後のものを取り除きます。JSX の期待とは違いました。

### 確認メモ（発表では話さない）

2022 年の報告を説明する。現在の Astro の挙動ではない。報告の class 属性を title に簡略化した例。HTML の重複属性と、JSX で後の指定を優先する props の合成を区別する。JavaScript expression は日本語では式。発話では初出で説明し、以後は JavaScript expression に統一する。Astro AST の expression node は波かっこを含む領域を指すため、その中の JavaScript expression と区別する。

### 出典と確認資料（発表では話さない）

- [astro#5558 の説明](https://github.com/withastro/astro/issues/5558#issuecomment-1343799494)
- [Astro Syntax](https://docs.astro.build/en/reference/astro-syntax/)
- [HTML Standard の attribute name state](https://html.spec.whatwg.org/multipage/parsing.html#attribute-name-state)
-->

---
layout: default
class: body-center
clicks: 3
---

## Astro Syntax

```astro
<span>Astro</span>
<span>1200</span>
```

<!-- クイズと答えの表示領域を固定し、Astro Syntax への問いと短い答えは Overlay で切り替える -->
<div class="mt-4 h-[96px] flex flex-col items-center justify-center text-center text-2xl">
  <div v-if="$clicks === 0"><span class="text-primary font-600">Q. </span>このコードは、どちらの表示になる？</div>
  <div v-if="$clicks === 0" class="mt-4"><code>Astro1200</code> か、<code>Astro 1200</code> か</div>
  <div v-if="$clicks === 1"><span class="text-primary font-600">A. </span><code>Astro 1200</code></div>
  <Overlay v-if="$clicks >= 2" aria-label="Astro Syntax への問いと答え">
    <template #title>
      <span v-if="$clicks === 2">JSX なら空白なし。なぜ空白が入った？</span>
      <span v-else>Astro が保持した改行を、ブラウザが空白にする</span>
    </template>
    <p v-if="$clicks >= 3">
      この報告では、Astro が要素間の改行を HTML に保持した。<br />
      ブラウザがその改行を空白として表示し、<code>Astro 1200</code> になった。
    </p>
    <template v-if="$clicks === 3" #reference>
      <a href="https://github.com/withastro/astro/issues/6011" target="_blank" rel="noopener noreferrer">astro#6011: 要素間の空白テキスト node</a>
      <a href="https://blog.dwac.dev/posts/html-whitespace/" target="_blank" rel="noopener noreferrer" class="ml-8">HTML Whitespace is Broken</a>
    </template>
  </Overlay>
</div>

<!--
予定時間 03:15 から 03:35（20 秒）。発話 98 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

3 回のクリックを発話に合わせる。

### 発話

[初期表示]
改行して並べた二つの span は、どう表示されるでしょう。
[クリック 1]
当時は間に空白が入りました。
[クリック 2]
この理由も、
[クリック 3]
それ、ブラウザの解釈です。出力に保持された改行を、ブラウザが空白として表示します。空白の規則も利用者の期待に関係します。

### 確認メモ（発表では話さない）

2023 年の報告。既定の CSS の空白規則を前提とする。この空白の話は HTML correction と別の論点。35 枚目で Astro v7 の設定の変更へ戻る。

### 出典と確認資料（発表では話さない）

- [astro#6011: 要素間の空白テキスト node](https://github.com/withastro/astro/issues/6011)
- [参照資料 2](https://blog.dwac.dev/posts/html-whitespace/)
-->

---
layout: default
class: table-comparison body-center code-example-compact
clicks: 4
---

## Astro Syntax

<div>

<div class="flex gap-8 w-full">
  <div class="min-w-0 code-split" :class="$clicks >= 1 ? 'w-[calc(50%-1rem)]' : 'w-full'">
    <div class="text-primary font-600 text-xl mb-1 flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro</div>

```astro
<table>
  <tr><td>{'foo'}</td></tr>
</table>
<h2>Chats</h2>
```

  </div>
  <Transition name="reveal-right">
  <div class="min-w-0 w-[calc(50%-1rem)]" v-if="$clicks >= 1">
    <div class="text-primary font-600 text-xl mb-1 flex items-center gap-2"><logos-html-5 class="w-5 h-5" />生成された HTML</div>

```html
<table>
  <tr><td>foo</td></tr>
  <h2>Chats</h2>
</table>
```

  </div>
  </Transition>
</div>

<Overlay v-if="$clicks >= 2" aria-label="Astro Syntax への問いと答え">
  <template #title>
    <span v-if="$clicks === 2">table の外に書いた h2 が、なぜ中に入った？</span>
    <span v-else-if="$clicks === 3">Compiler のパース状態を戻せなかった不具合</span>
    <span v-else>HTML Standard の <code>sarcasm</code> 終了タグ</span>
  </template>
  <p v-if="$clicks === 3">
    波かっこの領域のパース後に、Compiler がパースの状態を戻せなかった。<br />
    そのため、表の後の <code>h2</code> が <code>table</code> の中に入った。<br />
    HTML5 の正しい補正結果ではない。
  </p>
  <img v-if="$clicks === 4" src="./images/html-spec/sarcasm-deep-breath.png" alt="HTML Standard の in body insertion mode の項目。An end tag whose tag name is &quot;sarcasm&quot; に対し、Take a deep breath, then act as described in the &quot;any other end tag&quot; entry below. と書かれている。" class="w-full" />
  <template v-if="$clicks === 3" #reference>
    <a href="https://html.spec.whatwg.org/multipage/parsing.html#tree-construction" target="_blank" rel="noopener noreferrer">HTML Standard：Tree construction</a>
  </template>
  <template v-else-if="$clicks === 4" #reference>
    <a href="https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody" target="_blank" rel="noopener noreferrer">HTML Standard：The "in body" insertion mode</a>
  </template>
</Overlay>

</div>

<Ref href="https://github.com/withastro/compiler/issues/870">compiler#870</Ref>

<!--
予定時間 03:35 から 04:15（40 秒）。発話 235 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

4 回のクリックを発話に合わせる。

### 発話

[初期表示]
次は、表の中に JavaScript expression を含む例です。
[クリック 1]
表の後に書いた h2 が、生成結果では表の中に入っています。
[クリック 2]
JSX の感覚なら、表の後に書いた h2 は表の外にあるはずですよね。なぜ中に入ったんでしょうか。
[クリック 3]
これは Compiler の不具合でした。波かっこの領域のパース後に、パースの状態を戻せなかったためです。Astro の式と HTML5 Parser を組み合わせる難しさが、この例に出ています。
[クリック 4]
HTML5 Parser の仕様には、sarcasm の終了タグに Take a deep breath と書かれています。それほど補正の規則は複雑です。

### 確認メモ（発表では話さない）

compiler#870 と修正 PR #925。この例で h2 が table に入った直接の理由は、波かっこの領域の終了時に解析状態を戻せなかった不具合。修正は resetInsertionMode() で解析状態を選び直すもの。発表では、Browser が行う補正を Compiler が担っていた点を強調する。Compiler の生成 HTML と Browser が作る DOM は区別する。sarcasm の画像の出典と撮影方法は images/html-spec/README.md を参照する。

### 出典と確認資料（発表では話さない）

- [JavaScript expression を含む表の解析を修正した PR #925](https://github.com/withastro/compiler/pull/925)
- [compiler#870](https://github.com/withastro/compiler/issues/870)
- [HTML Standard：Tree construction](https://html.spec.whatwg.org/multipage/parsing.html#tree-construction)
- [HTML Standard：The "in body" insertion mode](https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody)
-->

---
layout: default
class: ch2-detail
---

## Astro syntax を振り返る

<div class="ch2-reflection">
  <div>
    <h3>HTML らしさ</h3>
    <ul><li>HTML に似た構文と、利用者が期待する挙動</li></ul>
  </div>
  <div>
    <h3>空白の扱い</h3>
    <ul><li>Browser で空白になる改行を、Astro syntax の規則で扱えないか</li></ul>
  </div>
  <div>
    <h3>HTML5 Parser のふるまい</h3>
    <ul><li>タグの補完や入れ子の補正まで、Astro で採用する必要があるか</li></ul>
  </div>
</div>
<div class="ch2-next-question">HTML5 Parser は必要なのか？</div>

<!--
予定時間 04:05 から 04:20（15 秒）。発話 85 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

ここには、属性の規則、空白の規則、Parser の不具合という別の論点があります。HTML に似た構文で、ブラウザと同じタグの補正まで Compiler が担うかを考え直します。

### 確認メモ（発表では話さない）

HTML correction の有無は実装言語とは独立した設計判断。Rust ならこれらが自動的に解消されるとは説明しない。
-->

---
layout: default
class: go-era-slide go-era-tools
---

<div class="go-era-heading">
  <h2>Astro v2〜v5</h2>
  <span class="go-era-year">2023〜2025年</span>
</div>

<div class="go-era-summary">ビルドに加え、書いている間のサポートも必要になる</div>

<Overview
  highlight="source,compiler,editor"
  era="go"
/>

<!--
発話 227 文字。コードを書いている間のサポートの説明を 12 枚目から移した。改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

次は、同じ Compiler を編集ツールが使う場面です。Astro で開発するときには、ビルドに加えて、コードを書いている間のサポートも必要になります。
コードを検査したり、整形したり、補完候補を表示したりするために、Linter と Formatter と Language Server も Go Compiler を利用していました。
実行できるコードを作ることと、書いている途中のコードをサポートすることでは、必要な情報が違うんですね。まずは Linter の例で確認します。
-->

---
layout: default
class: ch2-detail ch2-tool-overview
---

## Linter が .astro を検査するまで

<div class="ch2-tool-route">
<div class="ch2-route-step"><div class="ch2-route-node">.astro</div><div class="ch2-route-caption">検査したい元のコード</div></div>
<svg class="ch2-route-arrow" viewBox="0 0 24 18" aria-hidden="true"><path d="M12 0 V15 M7 10 L12 15 L17 10" /></svg>
<div class="ch2-route-step"><div class="ch2-route-node">JavaScript と JSX</div><div class="ch2-route-caption">JavaScript をパースするために変換<br />JSX は JavaScript にタグを書ける構文</div></div>
<svg class="ch2-route-arrow" viewBox="0 0 24 18" aria-hidden="true"><path d="M12 0 V15 M7 10 L12 15 L17 10" /></svg>
<div class="ch2-route-step"><div class="ch2-route-node">AST</div><div class="ch2-route-caption">JavaScript の Parser でパース<br />AST はコードを node で表すデータ</div></div>
<svg class="ch2-route-arrow" viewBox="0 0 24 18" aria-hidden="true"><path d="M12 0 V15 M7 10 L12 15 L17 10" /></svg>
<div class="ch2-route-step"><div class="ch2-route-node">AST とスコープ情報</div><div class="ch2-route-caption">宣言と参照を対応させる<br />位置を元の .astro に対応させて返す</div></div>
<svg class="ch2-route-arrow" viewBox="0 0 24 18" aria-hidden="true"><path d="M12 0 V15 M7 10 L12 15 L17 10" /></svg>
<div class="ch2-route-step"><div class="ch2-route-node">ESLint の診断</div><div class="ch2-route-caption">ルールが検査し、元の .astro の範囲で報告</div></div>
</div>

<Ref href="https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/index.ts">JavaScript のパースと位置対応</Ref>

<!--
改稿前の予定時間 04:25 から 04:35（10 秒）。発話 110 文字。練習での発話に基づいて改稿した。時間配分は再調整する。実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Linter の検査には、JavaScript expression の識別子や演算子をたどれる AST が必要です。ESLint のルールが扱う AST を得るために、まず Astro のコードを JavaScript と JSX へ変換します。

### 確認メモ（発表では話さない）

astro-eslint-parser は Go Compiler の Astro AST を使って JavaScript と JSX を生成する。型注釈のない例では Espree を利用する。スコープ解析は Espree 自体の返却機能とは区別する。

### 出典と確認資料（発表では話さない）

- [スコープ解析の実装](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/script.ts)
- [ESLint のスコープ情報](https://eslint.org/docs/latest/extend/scope-manager-interface)
- [astro-eslint-parser 1.2.2 の解析と位置対応](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/index.ts)
-->

---
layout: default
class: ch2-detail
---

## Go Compiler の AST だけで検査できるのか

<div class="ch2-cols">
<div>
<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro の構文は Espree へ直接渡せない</div>

```astro
---
const price = 10;
const amount = 3;
---

<p>{price * amount}</p>
```

</div>
<div>
<div class="ch2-label">Go Compiler が返す Astro AST</div>

```js
{
  type: "expression",
  children: [{
    type: "text",
    value: "price * amount"
  }]
}
```

<div class="ch2-note"><code>TextNode.value</code> は文字列</div>
</div>
</div>
<div class="ch2-summary">JavaScript と JSX へ変換し、JavaScript expression を再解析する</div>

<Ref href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#parse-astro-and-return-an-ast">Compiler 2.12.2 と AST</Ref>

<!--
改稿前の予定時間 04:35 から 05:00（25 秒）。発話 255 文字。練習での発話に基づいて改稿した。時間配分は再調整する。実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

ESLint が利用するのは、ESTree に基づく AST です。ESTree は JavaScript の AST の形式を定める仕様です。
右のデータを確認すると、Go Compiler が返す Astro AST では、price と amount の掛け算が TextNode の文字列になっています。このデータだけでは、識別子や演算子を node としてたどれません。
ツールが欲しいのは、JavaScript expression が AST として解析されたデータなんですね。そこで、ツールが JavaScript expression を再解析します。

### 確認メモ（発表では話さない）

ESTree は JavaScript の AST の形式を定める仕様。JavaScript 言語の仕様である ECMAScript と区別する。Go Compiler の Astro AST 全体が文字列という意味ではない。この JavaScript expression が TextNode.value の文字列であり、JavaScript の node を提供しない点を説明する。実装言語が Go であることの制約とは説明しない。
Compiler 2.12.2 の parse(source, { position: true }) の抜粋。Astro AST の expression node は子に Markup の node を含められるため、JavaScript expression 全体が常に一つの文字列という意味ではない。入力の行と末尾の LF は元の検証例に基づく。

### 出典と確認資料（発表では話さない）

- [Compiler 2.12.2 と AST](https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#parse-astro-and-return-an-ast)
- [ESTree の AST の定義](https://github.com/estree/estree/blob/master/es5.md)
-->

---
layout: default
class: ch2-detail ch2-expression-static
---

## 変数名と演算子をどう取得するのか

<div class="ch2-cols">
<div>
<div class="ch2-label flex items-center gap-2"><logos-javascript class="w-5 h-5 shrink-0" aria-hidden="true" />JavaScript と JSX</div>

```jsx
const price = 10;
const amount = 3;
<>
  <p>{price * amount}</p>
</>;
```

<div class="ch2-note">元の <code>.astro</code> を<br />JavaScript と JSX に変換する</div>
</div>
<div>
<div class="ch2-label">JavaScript expression の AST</div>

```text
BinaryExpression
├─ operator: "*"
├─ left: Identifier
│  └─ name: "price"
└─ right: Identifier
   └─ name: "amount"
```

<div class="ch2-note"><strong>BinaryExpression</strong> は二項演算<br /><strong>Identifier</strong> は識別子</div>
</div>
</div>
<div class="ch2-summary">Espree で解析し、変数名と演算子を AST の項目として取得する</div>

<!--
改稿前の予定時間 05:00 から 05:25（25 秒）。発話 208 文字。練習での発話に基づいて改稿した。時間配分は再調整する。実測ではない。

### 進行案内（発表では話さない）

クリックなし。左で変換後のコード、右で JavaScript expression の AST を説明する。

### 発話

元の Astro のコードから、astro-eslint-parser が JavaScript と JSX を作ります。これを Espree で解析します。
解析すると、price と amount は Identifier、掛け算は BinaryExpression として表せます。演算子も項目として取得できます。
JavaScript expression を検査するためのデータがそろったので、次は結果を元のコードのどこに表示するかを考えます。

### 確認メモ（発表では話さない）

Identifier という node の種類と、変数の型の情報は区別する。この例で参照先の宣言を調べるにはスコープ解析が必要。AST の種類を説明するときに Typed AST という名称は使わない。
画面の JavaScript と JSX は説明のために一部のセミコロンと空行を省いた抜粋。Language Tool の convertToTSX() とは生成元と目的が異なる。

### 出典と確認資料（発表では話さない）

- [astro-eslint-parser 1.2.2 と processTemplate](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/process-template.ts)
-->

---
layout: default
class: ch2-detail ch2-position-slide body-center
---

## 位置の対応と位置情報の不具合

<SourcePositionComparison />

<!--
改稿前の予定時間 05:25 から 05:30（5 秒）。発話 237 文字。練習での発話に基づいて改稿した。時間配分は再調整する。実測ではない。

### 進行案内（発表では話さない）

図の上段で変換前後の位置対応、下段で Compiler の範囲の誤りと修正を説明する。数値は発話しない。

### 発話

ここは、位置に関する二つの話を分けます。
図の上段は、JavaScript と JSX への変換で文字位置が変わる話です。診断を元のコードに表示するには、変換前後の対応が必要です。
下段は、Go Compiler が返す Astro AST の位置そのものが不正確だった例です。波かっこを含む範囲を誤って返すため、Linter の Adapter は、その位置の修正も引き受けていました。
Compiler から必要な AST と正確な位置を受け取れれば、ツールで再解析や不具合の補正を行う範囲を減らせます。

### 確認メモ（発表では話さない）

図の上段は変換前後の位置対応、下段は Compiler の位置計算の不具合を示す。不具合の例は expression.astro を Compiler 2.12.2 と astro-eslint-parser 1.2.2 に渡して再確認した。Compiler が返す Astro AST の expression node の範囲は [47, 80)、元の波かっこを含む範囲は [48, 64)。astro-eslint-parser が後者へ修正する。変換した JavaScript の AST の位置を元のコードへ対応させる工程と、この修正を区別する。
数値は発話しない。変換で位置が変わることと、Compiler 2.12.2 の Astro AST の expression node の範囲計算の不具合は別。例の price は変換後の全文で [46, 51)、元の全文で [49, 54)。一定の差をファイル全体に加える方式ではない。ASCII の例なので UTF-8 と UTF-16 の値が一致する。

### 出典と確認資料（発表では話さない）

- [Compiler 2.12.2 の位置情報の実装](https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/internal/printer/print-to-json.go#L134-L175)
- [astro-eslint-parser の位置対応](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/context/restore.ts)
- [astro-eslint-parser 1.2.2 の解析と位置対応](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/index.ts)
- [位置情報を再確認するコード](/Users/kenji/Projects/slidev/validation/chapter2/verify.mjs)
-->

---
layout: default
class: ch2-detail code-example-dense ch2-linter-check
disabled: true
---

## 未定義の変数をどう検出するのか

<div class="ch2-context-flow ch2-lint-context" aria-label="Linter の全体図から、AST の取得と位置対応と診断の工程を再掲">
  <div class="ch2-context-node">AST</div>
  <svg class="ch2-context-arrow" viewBox="0 0 28 24" aria-hidden="true"><path d="M1 12 H25 M19 6 L25 12 L19 18" /></svg>
  <div class="ch2-context-node">AST とスコープ情報<span>位置を元の .astro に対応させる</span></div>
  <svg class="ch2-context-arrow" viewBox="0 0 28 24" aria-hidden="true"><path d="M1 12 H25 M19 6 L25 12 L19 18" /></svg>
  <div class="ch2-context-node is-current">ESLint の診断</div>
</div>

<div class="ch2-cols ch2-scope">
<div>
<div class="ch2-label">ここで変数名を誤記する</div>

```astro
---
const price = 10;
const amount = 3;
---

<p>{pirce * amount}</p>
<!-- pirce は診断のための誤記 -->
```

</div>
<div>
<div class="ch2-label">スコープ情報で宣言と参照を照合する</div>
<div class="ch2-lint-matches"><div><code>price</code><span>宣言あり</span></div><div><code>amount</code><span>参照先の宣言あり</span></div><div><code>pirce</code><span>参照先の宣言なし</span></div></div>
<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro への診断</div>
<pre class="ch2-lint-diagnostic">&lt;p&gt;{<span>pirce</span> * amount}&lt;/p&gt;</pre>
<div class="ch2-note">元のコードの範囲 <code>[49, 54)</code><br /><code>no-undef</code>: <code>'pirce' is not defined.</code></div>
</div>
</div>
<div class="ch2-summary">未定義の参照を検出し、元の5文字に波線を表示する</div>

<Ref href="https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/index.ts">ESLint へ AST を渡すまで</Ref>

<!--
本編から省略。参考としてソースに保持する。

予定時間 05:30 から 05:45（15 秒）。発話 71 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

price を pirce と誤記すると、対応する宣言がありません。スコープ情報でこれを検出し、位置の対応を使って、元の五文字に波線を表示できます。

### 確認メモ（発表では話さない）

ESLint の no-undef は未定義の参照を検査する。正しい綴りを推測して修正する機能ではない。元の検証は ESLint 9.36.0 と astro-eslint-parser 1.2.2。

### 出典と確認資料（発表では話さない）

- [astro-eslint-parser と ESLint への返却値](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/index.ts)
-->

---
layout: default
class: ch2-detail ch2-tool-overview
---

## Formatter が .astro を整形するまで

<div class="ch2-tool-route">
<div class="ch2-route-step"><div class="ch2-route-node">.astro</div><div class="ch2-route-caption">整形したい元のコード</div></div>
<svg class="ch2-route-arrow" viewBox="0 0 24 18" aria-hidden="true"><path d="M12 0 V15 M7 10 L12 15 L17 10" /></svg>
<div class="ch2-route-step"><div class="ch2-route-node">JavaScript expression<br />のコード</div><div class="ch2-route-caption">JavaScript をパースするために取り出す</div></div>
<svg class="ch2-route-arrow" viewBox="0 0 24 18" aria-hidden="true"><path d="M12 0 V15 M7 10 L12 15 L17 10" /></svg>
<div class="ch2-route-step"><div class="ch2-route-node">JavaScript expression<br />の AST</div><div class="ch2-route-caption">JavaScript の Parser でパース<br />AST はコードを node で表すデータ</div></div>
<svg class="ch2-route-arrow" viewBox="0 0 24 18" aria-hidden="true"><path d="M12 0 V15 M7 10 L12 15 L17 10" /></svg>
<div class="ch2-route-step"><div class="ch2-route-node">中間表現 Doc</div><div class="ch2-route-caption">文字と改行候補と字下げの指示</div></div>
<svg class="ch2-route-arrow" viewBox="0 0 24 18" aria-hidden="true"><path d="M12 0 V15 M7 10 L12 15 L17 10" /></svg>
<div class="ch2-route-step"><div class="ch2-route-node">整形後の .astro</div><div class="ch2-route-caption">Prettier が行幅に合わせて文字列を生成</div></div>
</div>

<!--
改稿前の予定時間 05:45 から 05:57（12 秒）。発話 205 文字。練習での発話に基づいて改稿した。時間配分は再調整する。実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Formatter も JavaScript expression の AST が必要なので、プラグインがコードを取り出して Babel で再解析します。
続いて Prettier は、AST から Doc という整形のための中間表現を作ります。Doc は、出力する文字と改行候補と字下げの指示を表します。この指示から、行幅に合わせてコードを整形します。
Compiler から AST を受け取れる設計でも、Doc を作って整形する工程は必要です。

### 確認メモ（発表では話さない）

prettier-plugin-astro 0.14.1 と Prettier 3.6.2 の例。Babel が解析し、Prettier の Printer が Doc を作る。再解析と整形指示への変換は別の工程。

### 出典と確認資料（発表では話さない）

- [Prettier の Parser と Printer](https://prettier.io/docs/plugins)
- [Prettier の整形方式](https://prettier.io/docs/technical-details)
- [prettier-plugin-astro 0.14.1 と JavaScript expression の整形](https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/printer/embed.ts)
-->

---
layout: default
class: ch2-detail ch2-formatter-failure
clicks: 2
---

## コードの再生成で、整形が止まった

<FormatterFailureExample :step="$clicks" />

<!--
発話 334 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

初期表示で入力と工程を説明する。クリック 1 で再生成された不正なタグ、クリック 2 で整形エラーを表示する。

### 発話

[初期表示]
Formatter の困りごとを具体例で確認します。この JavaScript expression には、中身が空の Fragment があります。Go Compiler はこの記述を変換でき、解析した AST にも Fragment があります。
[クリック 1]
ただし、JavaScript expression を AST として受け取れないため、プラグインは JavaScript expression のコードを再生成して Babel に渡します。ここで Compiler に付属する文字列化の機能が、空の Fragment を不正なタグに変えてしまいました。
[クリック 2]
Babel が構文エラーを返し、整形できません。JavaScript expression の AST を取得するまでに、こうした再生成の不具合にも対応する必要がありました。

### 確認メモ（発表では話さない）

prettier-plugin-astro の空の Fragment に関する報告を簡略化し、Compiler 2.12.2 と prettier-plugin-astro 0.14.1 と Prettier 3.6.2 で再現した。現在の版の挙動を示すものではない。
入力は {true ? <p>OK</p> : <></>}。Compiler の transform() は成功し、parse() は空の fragment node を返す。条件演算子を含む JavaScript expression 全体は AST として返らない。
プラグインの printRaw() は Astro AST の expression node の子を Compiler package の serialize() で文字列にする。serialize() の初期設定 selfClose は true で、子が空の fragment を < /> にする。文字列化の実装は Compiler package の JavaScript の補助機能である。Go Parser が Fragment を解析できなかったという説明はしない。
再生成された true ? <p>OK</p> : < /> を astroExpressionParser が JSX Fragment と波かっこで囲み、Babel に渡すと構文エラーになる。整形前の元の入力を Babel で解析できることも確認する。
以前の JSX で囲む理由は補足にする。オブジェクトリテラルを文と区別するために <>{式}</> の形式を使い、閉じ波かっこの前の改行で行コメントとの混同を避ける。

### 出典と確認資料（発表では話さない）

- [空の Fragment を含む JavaScript expression の整形エラー](https://github.com/withastro/prettier-plugin-astro/issues/444)
- [JavaScript expression を文字列にするプラグインの実装](https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/printer/embed.ts)
- [Compiler の serialize()](https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/packages/compiler/src/node/utils.ts)
- ローカルの再現: validation/chapter2/formatter-fragment.mjs。
-->

---
layout: default
class: ch2-detail ch2-formatter-requirements
---

## Formatter は Compiler に何を求めたのか

<FormatterResponsibilities />

<!--
発話 230 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。左で Compiler に求める情報、右で Formatter の担当を説明する。

### 発話

Compiler からは、JavaScript expression を、識別子や演算子をたどれる AST として受け取りたいんですね。Astro のタグとコメント、元のコードの正確な位置も必要です。
この情報があれば、AST を得るためにコードを再生成して、もう一度解析する工程を減らせます。
その AST を使って改行と字下げを決めるのは、引き続き Formatter の担当です。Compiler が解析結果を提供し、Formatter が整形を行う。この分担にしたい、という話です。

### 確認メモ（発表では話さない）

このページは第 2 章の要求を整理する。Rust 版の実装が再解析をすべて廃止したという説明はしない。Astro の node を含む AST は、Prettier の AST とそのまま同じとは限らず、対応する Printer や変換が必要になる。
旧ページの group と softline と indent の詳説は本編では扱わない。group は改行を判断するまとまり、softline は 1 行なら空文字で改行時には改行、indent は字下げを表す。JavaScript expression を解析して AST を取得する工程と、AST から Doc を作る工程は区別する。
前の Fragment の例では、Astro AST に Fragment は保持されていた。必要なのは、タグの認識に加えて JavaScript expression 全体の AST を提供し、整形ツールが文字列の再生成と再解析を引き受ける範囲を減らすこと。

### 出典と確認資料（発表では話さない）

- [新 Compiler と Prettier plugin の検討](https://github.com/withastro/roadmap/discussions/1306)
- [Prettier の整形工程](https://prettier.io/docs/plugins#the-printing-process)
- [Doc の定義と命令](https://github.com/prettier/prettier/blob/main/commands.md)
-->

---
layout: default
class: ch2-detail ch2-language-overview
---

## Go Compiler と Language Tool の分担

<LanguageToolOverview />

<Ref><a href="https://code.visualstudio.com/api/language-extensions/language-server-extension-guide">LSP と Language Server</a> と <a href="https://volarjs.dev/core-concepts/embedded-languages/">Volar と位置対応</a> と <a href="https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/index.ts">Astro の実装</a></Ref>

<!--
発話 379 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。サーバー内部の Compiler の返却値、Astro の言語対応と Volar と Language Service、Editor との通信の順に説明する。

### 発話

Language Tool では、Compiler が何を返し、その後は誰が担当するのかを分けます。Go Compiler は TSX と Source map を返します。TSX は TypeScript でタグを扱うコード、Source map は生成前後の位置の対応表です。
Astro の言語対応は HTML も作り、TSX と位置対応を Volar に登録します。Volar は、解析器に渡すコードと位置の対応を管理する基盤です。
属性の補完は HTML Language Service、型の診断と補完は TypeScript が担当します。Language Service は言語機能を提供するライブラリです。
これらを組み合わせて Editor に機能を提供するプログラムが Astro Language Server です。Editor との通信の規約を LSP、Language Server Protocol と呼びます。

### 確認メモ（発表では話さない）

この図は Go Compiler と Volar を使う参照実装の分担を示す。LSP は Editor と Language Server の通信規約であり、サーバー内部の矢印を LSP の通信として説明しない。
Compiler の convertToTSX() は code と map に加え、diagnostics と metaRanges も返す。図は型の診断に必要な TSX と Source map を抜粋している。Compiler も構文の診断を返す。TypeScript が担当するのは型に関する検査と補完である。
Astro の言語対応は parseHTML() で Virtual HTML を作り、astro2tsx() で convertToTSX() を呼び、TSX と Source map を Volar が扱う形式にする。Language Tool の機能すべてを Go Compiler が生成するという説明はしない。

### 出典と確認資料（発表では話さない）

- [AstroVirtualCode](https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/index.ts)
- [TSX と位置対応の登録](https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/astro2tsx.ts)
- [LSP と Language Server](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide)
- [Volar と埋め込まれた言語](https://volarjs.dev/core-concepts/embedded-languages/)
-->

---
layout: default
class: ch2-detail code-example-dense ch2-language-example
clicks: 2
---

## 誰が HTML と TSX を作るのか

<div class="ch2-cols">
<div>
<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro</div>

```astro
---
const product = {
  name: "Notebook", price: 1200,
};
---

<a href="/products">
  {product.nmae}
</a>
```

</div>
<div class="ch2-language-results">
<div v-if="$clicks === 0" class="ch2-language-purpose">
  <div><div class="ch2-label">Astro の言語対応が HTML を作る</div><p>HTML Language Service で<br />属性を補完する。</p></div>
  <div><div class="ch2-label">Go Compiler が TSX を返す</div><p>TypeScript で型を検査する。<br />Source map も返す。</p></div>
</div>
<div v-if="$clicks === 1">
<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-6 h-6 shrink-0" aria-hidden="true" />Astro の言語対応が作る HTML</div>

```html
<a href="/products">
  {product.nmae}
</a>
```

<div class="ch2-note">HTML Language Service<br />属性補完: <code>target</code> と <code>title</code></div>
<div class="ch2-result">Component script を空白化し、<br />文字オフセットを保持する</div>
</div>
<div v-if="$clicks >= 2">
<div class="ch2-label flex items-center gap-2"><img src="./images/logos/gopher-classic.png" class="w-6 h-6 object-contain" alt="" />Go Compiler が返す TSX</div>

```tsx
const product = {
  name: "Notebook", price: 1200,
};
<Fragment>
<a href="/products">
  {product.nmae}
</a>
</Fragment>
```

<div class="ch2-note"><logos-typescript-icon class="inline-block w-5 h-5 align-middle" aria-hidden="true" /> TypeScript が型を検査<br /><code>nmae</code> は型にない。位置の対応には Source map を使う</div>
</div>
</div>
</div>

<Ref href="https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/index.ts">language-tools b4bcb4f と AstroVirtualCode</Ref>

<!--
発話 239 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリック 1 で Astro の言語対応が生成する HTML、クリック 2 で Go Compiler が返す TSX を表示する。

### 発話

[初期表示]
同じ Astro のコードでも、使いたい言語機能に合わせて二つのコードを用意します。こうした解析器に渡すコードを Virtual Code と呼びます。
[クリック 1]
HTML は Astro の言語対応が作ります。上のスクリプトを空白に変え、HTML Language Service で属性を補完します。
[クリック 2]
TSX は Go Compiler が作り、元の位置との対応表も返します。TypeScript はそのコードから product の型を調べ、nmae という誤記を診断します。Compiler が型を調べるわけではありません。

### 確認メモ（発表では話さない）

入力と二つの生成コードは、以前の検証と同じ抜粋である。コードの文字列と改行は変更していない。Virtual HTML の空白化は UTF-16 の文字オフセットを保持する。行番号が一致するという意味ではない。
画面の TSX は pragma と空行と末尾の関数などを省略した抜粋。Go Compiler の convertToTSX() が TSX と Source map を返し、Astro の言語対応が Volar の Virtual Code と位置対応データを作る。
Virtual Code は解析器が扱うために生成するコードの呼称。TSX と HTML への変換には、それぞれ利用する言語機能のための役割がある。

### 出典と確認資料（発表では話さない）

- [AstroVirtualCode](https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/index.ts)
- [HTML の生成](https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/parseHTML.ts)
- [TSX と位置対応の登録](https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/astro2tsx.ts)
-->

---
layout: default
class: ch2-detail ch2-mapping-slide
---

## 診断を元の .astro へ返す分担

<LanguageDiagnosticFlow />

<Ref><a href="https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/astro2tsx.ts">Compiler の返却値と Volar への位置対応</a> と <a href="https://volarjs.dev/core-concepts/embedded-languages/">Volar の位置対応</a></Ref>

<!--
発話 275 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。左の型の診断と右の位置対応データを説明し、Volar と Editor の順に進む。位置の数値は発話しない。

### 発話

Compiler が返す二つの情報は、その後の役割も違います。左の TSX を TypeScript が検査し、型にない nmae を診断します。この診断は、生成したコードの位置を指しています。
右の Source map は、Astro の言語対応が Volar の位置対応データへ変換します。Volar はそれを使い、診断する範囲を元の Astro の文字に対応させます。
最後に Astro Language Server が LSP で結果を送り、Editor が四文字に波線を表示します。Compiler が渡すコードと位置の情報を、Language Tool が編集支援につないでいるんですね。

### 確認メモ（発表では話さない）

左右の列はデータの利用関係であり、診断の後に Source map を生成するという時系列を示すものではない。Source map の生成は Compiler、Volar の mapping への変換は Astro の言語対応、診断範囲の対応は Volar、波線の表示は Editor が担当する。
位置対応はコード変換に伴う工程である。21 枚目の Compiler の不正確な位置情報とは区別する。
以前の位置の数値は確認資料に保持する。Compiler 2.12.2 と TypeScript 5.9.3 の検証で、型診断 TS2339 は TSX の [129, 133) を指し、元の .astro は [95, 99) に対応する。LSP では start: { line: 7, character: 11 } と end: { line: 7, character: 15 }。終端を含まない。

### 出典と確認資料（発表では話さない）

- [convertToTSX と位置対応](https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/astro2tsx.ts)
- [Volar と埋め込まれた言語](https://volarjs.dev/core-concepts/embedded-languages/)
- [LSP と Language Server](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide)
-->

---
layout: default
class: ch2-detail
---

## Compiler の課題とツールの分担

<CompilerToolRequirements />

<!--
発話 250 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。左の返却値を確認し、右の ESLint と Prettier と Language Tool の仕事へ進む。

### 発話

Go Compiler は、JavaScript expression を文字列として返していたので、ESLint と Prettier ではパースし直す必要がありました。位置情報の不具合も、Linter の Adapter で修正していたんですね。
Language Tool は TSX と Source map を受け取り、HTML も作って、Volar や TypeScript の機能につなぎます。
ツールが本来担当する仕事に加えて、Compiler の不足や不具合への対応も必要だった。使い続けるなかで、そういう負担が分かってきました。

### 確認メモ（発表では話さない）

18 枚目から 27 枚目は、ツールが必要とする情報、Compiler の情報不足と不具合、利用するツールに必要な変換の順で振り返る。Virtual Code と位置対応と Doc の生成を、それ自体が Go Compiler の不具合であるとは説明しない。
未定義の参照の詳説は本編から省略し、補足にする。23 枚目は再解析のためのコード生成の途中の不具合、24 枚目は Compiler と Formatter の分担に改稿した。JSX で囲む理由と Doc の命令の詳説は確認メモに移した。LSP と Volar の分担は本編で説明する。
AST があればスコープ解析や型検査が不要という意味ではない。Compiler が生成したコードの位置対応は Compiler が、Adapter が独自に生成したコードの位置対応は Adapter が管理する。
-->

---
layout: statement
---

<h1 class="!text-5xl !leading-relaxed !m-0">Astro が使える基盤は、<br />2021年からどう変わったのか？</h1>

<!--
予定時間 07:30 から 07:35（5 秒）。発話 23 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

では、今はどんな基盤を利用できるのでしょうか。
-->

---
layout: section
---

# 3. 前提の変化
## Astro が再利用できる基盤はどう変わったのか

<!--
予定時間 07:35 から 07:40（5 秒）。発話 17 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

ここから、前提の変化を確認します。
-->

---
layout: default
class: ch3-detail chapter-three ch3-tools
---

## Rust とフロントエンドツールチェーン

<div class="ch3-tool-grid">
  <div class="ch3-tool">
    <logos-swc class="ch3-tool-logo" aria-hidden="true" />
    <h3><a href="https://swc.rs/">SWC</a></h3>
    <p>JavaScript と TypeScript の<br />変換</p>
  </div>
  <div class="ch3-tool">
    <logos-oxc-icon class="ch3-tool-logo" aria-hidden="true" />
    <h3><a href="https://oxc.rs/">Oxc</a></h3>
    <p>JavaScript と TypeScript の<br />解析と変換</p>
  </div>
  <div class="ch3-tool">
    <logos-biomejs-icon class="ch3-tool-logo" aria-hidden="true" />
    <h3><a href="https://biomejs.dev/">Biome</a></h3>
    <p>検査と整形</p>
  </div>
  <div class="ch3-tool">
    <img src="./images/tools/lightning-css.svg" class="ch3-tool-logo" alt="" />
    <h3><a href="https://lightningcss.dev/">Lightning CSS</a></h3>
    <p>CSS の変換と最適化</p>
  </div>
  <div class="ch3-tool">
    <logos-rolldown-icon class="ch3-tool-logo" aria-hidden="true" />
    <h3><a href="https://rolldown.rs/">Rolldown</a></h3>
    <p>バンドル</p>
  </div>
  <div class="ch3-tool">
    <img src="./images/tools/rspack.svg" class="ch3-tool-logo" alt="" />
    <h3><a href="https://rspack.rs/">Rspack</a></h3>
    <p>バンドル</p>
  </div>
  <div class="ch3-tool">
    <logos-turbopack-icon class="ch3-tool-logo" aria-hidden="true" />
    <h3><a href="https://nextjs.org/docs/app/api-reference/turbopack">Turbopack</a></h3>
    <p>Next.js のバンドル</p>
  </div>
  <div class="ch3-tool">
    <logos-turborepo-icon class="ch3-tool-logo" aria-hidden="true" />
    <h3><a href="https://turborepo.dev/blog/turbo-1-11-0">Turborepo</a></h3>
    <p>タスク実行</p>
  </div>
</div>

<!--
発話 218 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Go Compiler を使い続けている間に、フロントエンドツールチェーンにも Rust で作られたツールが増えてきました。Oxc や Biome、Rolldown などですね。
ここで注目したいのは、ツールの中のライブラリを、自分たちの実装にも組み込めることです。たとえば Oxc を使えば、JavaScript expression の AST を取得できます。
先ほど欲しかった情報を、既存のライブラリで取得する選択肢があるんですね。次は、その例を確認します。

### 確認メモ（発表では話さない）

Astro が図のすべてのツールを採用しているという説明ではない。SWC は 2021 年にも利用されていた。Lightning CSS は CSS の解析と変換と生成と最適化を担当し、SCSS から CSS への変換は Sass の担当。

### 出典と確認資料（発表では話さない）

- [SWC](https://swc.rs/)
- [Oxc](https://oxc.rs/)
- [Biome](https://biomejs.dev/)
- [Lightning CSS](https://lightningcss.dev/)
- [Rolldown](https://rolldown.rs/)
- [Rspack](https://rspack.rs/)
- [Turbopack](https://nextjs.org/docs/app/api-reference/turbopack)
- [Turborepo](https://turborepo.dev/blog/turbo-1-11-0)
- [参照資料 9](https://nextjs.org/blog/next-12)
- [参照資料 10](https://biomejs.dev/blog/announcing-biome/)
-->

---
layout: default
class: ch3-detail chapter-three code-example-dense
---

## Oxc で JavaScript expression を解析する

<div class="ch3-cols ch3-oxc">
<div>
<div class="ch3-label">JavaScript から Parser を呼ぶ</div>

```js
import { parseSync } from "oxc-parser";

const { program } = parseSync(
  "example.js",
  "price * amount",
);
```

</div>
<div>
<div class="ch3-label">AST の抜粋</div>

```text
BinaryExpression
├─ operator: "*"
├─ left: Identifier
│  └─ name: "price"
└─ right: Identifier
   └─ name: "amount"
```

</div>
</div>
<div class="ch3-summary">Rust で実装された Parser を npm package から利用できる</div>

<Ref href="https://oxc.rs/docs/guide/usage/parser.html">Oxc Parser</Ref>

<!--
発話 107 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。左のコードを Oxc に渡し、右の AST で変数名と演算子を確認する。

### 発話

Oxc に、先ほどの price と amount の掛け算を渡してみます。

変数名と演算子を持つ AST が取得できます。Astro の構文にも対応させる必要はありますが、JavaScript の部分には Oxc を利用できるんですね。

### 確認メモ（発表では話さない）

ここは oxc-parser の JavaScript API の例。Astro Compiler の内部では Astro syntax に対応させた Oxc の Rust crate を利用する。実装言語と、npm パッケージと、ネイティブ版や WASM という配布方法は別の判断。

### 出典と確認資料（発表では話さない）

- [Oxc Parser](https://oxc.rs/docs/guide/usage/parser.html)
- [参照資料 2](https://vite.dev/blog/announcing-vite8)
- [参照資料 3](https://napi.rs/docs/introduction/simple-package)
- [参照資料 4](https://napi.rs/blog/announce-v2)
-->

---
layout: default
class: ch3-detail chapter-three ch3-information-slide
---

## 整形ツールの基盤を比べる

<FormattingInformation :stage="1" />

<!--
発話 222 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。発話後に次へ進む。

### 発話

前半では、Go Compiler から JavaScript expression の AST を受け取れなくて、Prettier のプラグインでコードを作り直し、Babel でパースし直していました。
この間に、参考にできる基盤の設計も増えてきました。たとえば Rust で作られた Biome は、JavaScript の構文に加えて、元の空白やコメントも保持します。
整形とコードの修正で必要な情報を、基盤で持つ。その一例が、ここから説明する Lossless CST です。

### 確認メモ（発表では話さない）

上段は Go Compiler と Astro の Prettier plugin の課題の振り返り。下段は JavaScript を扱う Biome の設計例。入力言語と目的が異なるため、性能や対応範囲の直接比較にはしない。空の Fragment の再生成の不具合は、コードの再生成で整形が止まったページを参照する。
Biome は Rust で実装された別のツール。Prettier の内部に Biome があるという意味ではない。Astro が Biome や Lossless CST を採用したとは説明しない。Rust Compiler を基盤にした Astro の Prettier plugin は、第 4 章で説明する。

### 出典と確認資料（発表では話さない）

- [Prettier の整形工程](https://prettier.io/docs/plugins#the-printing-process)
- [Biome の設計資料](https://biomejs.dev/internals/architecture/)
-->

---
layout: default
class: ch3-detail chapter-three ch3-information-slide body-center
---

## AST と Lossless CST が保持する情報

<FormattingInformation :stage="2" />

<!--
発話 237 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。発話後に次へ進む。

### 発話

同じ JavaScript のコードで比べます。Prettier が Babel から受け取る AST には、変数名や演算子の情報があります。コメントも受け取り、空白などを判断するときは元のコードも参照します。
Biome の Lossless CST は、構文の木の中に、空白が二文字だったこと、コメント、末尾の改行まで保持します。
CST は具象構文木で、記号なども表す構文の木です。Lossless は、元のコードを一文字も変えずに再現できる性質です。では、この情報があると何ができるのでしょうか。

### 確認メモ（発表では話さない）

図の AST は BinaryExpression の抜粋で、Prettier の全データを表さない。Prettier は言語とプラグインにより Parser が異なり、ここでは Babel の例を扱う。コメントを持つ AST もあり、コメントの保持だけで CST と分類しない。
Biome では空白とコメントなどを trivia として token に付随させる。token は名前や記号など、コードを分けた単位。CST が常に lossless とは限らない。元の文字を保持することと、不完全な入力からパースを続けるエラー回復は別の性質。

### 出典と確認資料（発表では話さない）

- [Prettier の整形工程](https://prettier.io/docs/plugins#the-printing-process)
- [Biome の Parser と CST](https://biomejs.dev/internals/architecture/#parser-and-cst)
-->

---
layout: default
class: ch3-detail chapter-three ch3-information-slide
---

## 名前だけを変え、空白とコメントを保つ

<FormattingInformation :stage="3" />

<!--
発話 232 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。発話後に次へ進む。

### 発話

たとえば、この一か所の price を unitPrice に変えたいとします。Lossless CST の名前の部分を変更して、ほかの情報を引き継げば、空白二文字も、コメントも、末尾の改行もそのままです。
直したい場所だけを変えて、ほかの場所の書式を保てる。コードの修正を作るときに、こういう情報を基盤から使えるのが嬉しいんですね。
整形するときは、Prettier も Biome も空白や改行を決め直します。ここで説明したのは、一か所を修正するときに、変更しない文字を保つ例です。

### 確認メモ（発表では話さない）

一か所の token の変更を示す模式例。biome_rowan の BatchMutation::replace_token は replace_element を呼び、元の token の leading trivia と trailing trivia を新しい token に引き継ぐ。commit で反映する。宣言と参照をまとめて改名するには、名前の参照関係を調べる機能も必要。
元の書式を保つ修正は、AST と元のコードの範囲を使うツールでも実装できる。Lossless CST だけが可能にする機能とは説明しない。利点は、構文と元の文字を一つの木で保持し、編集 API で扱えること。

### 出典と確認資料（発表では話さない）

- [Biome の Parser と CST](https://biomejs.dev/internals/architecture/#parser-and-cst)
- [biome_rowan の token の変更](https://github.com/biomejs/biome/blob/main/crates/biome_rowan/src/ast/batch.rs)
-->

---
layout: default
class: content-overview
---

## Markdown と MDX を変換する

<Overview
  highlight="mdsource,content,build,browser"
  :labels="{ build: 'Build' }"
/>

<div class="content-overview-summary">Content Processor が Markdown と MDX を変換し、Build へ渡す</div>

<!--
発話 75 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

ここから、私が取り組んだ Markdown と MDX の話です。Markdown と MDX も Parser を使い、変換したコードを Astro のビルドへ渡します。

-->

---
layout: default
class: ch3-detail chapter-three mdx-proposals mdx-astro-proposal
---

## Astro に MDX の高速化を提案した

<div class="mdx-lead">Rust で実装した Compiler の統合と AST Bridge を試作</div>
<div class="mdx-proposal-steps">
  <section>
    <div class="mdx-proposal-date">2025 年 7 月</div>
    <h3>Compiler を統合する</h3>
    <p>MDX の変換を高速化したい。<br />remark と rehype plugin との<br />互換性が課題になった</p>
  </section>
  <section>
    <div class="mdx-proposal-date">2025 年 8 月</div>
    <h3>AST Bridge を試す</h3>
    <p>Rust でパースした AST を<br />JavaScript の plugin に渡す</p>
  </section>
</div>

<Ref><a href="https://github.com/withastro/astro/pull/14080">Astro PR #14080</a> と <a href="https://github.com/withastro/astro/pull/14181#issuecomment-3311059055">PR #14181 での提案と助言</a></Ref>

<!--
発話 368 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Astro の公式ドキュメントには MDX が多くあるんですね。Astro は content-first を掲げているので、Markdown と MDX でも高速な実装を使ってほしいと思いました。取り組みの背景には、Markdown と MDX がボトルネックだというやり取りもありました。
2025 年 7 月に、Rust で実装した MDX Compiler を Astro に組み込む提案をしました。試すと、既存の remark と rehype のプラグインをどう使い続けるかが問題になりました。導入には、変換の速さに加えてプラグインの互換性も必要でした。
同じ年の 8 月には、AST Bridge も提案しました。Rust でパースした AST を、JavaScript のプラグインへ渡す方法です。
Astro での採用の見通しが立たなかったので、MDX のライブラリにも提案することにしました。

### 確認メモ（発表では話さない）

最初の統合提案は 2025 年 7 月 16 日、AST Bridge の提案は 2025 年 8 月 3 日（日本時間）。PR の作成日であり、試作を開始した日とは限らない。提案と試作を並行して進めた時期もある。
動機とボトルネックについてのやり取りは、本人がこの会話で共有した経験。相手と対象工程と計測範囲は未特定。一般的なベンチマーク事実や特定人物の発言として提示しない。6999 ページ、10 秒、半減などの数値は使わない。Astro の PR #14080 と PR #14181 は未マージで終了。拒否されたとは断定しない。AST Bridge と、xmdx の生成コードと付随情報を返す仕組みは別。

### 出典と確認資料（発表では話さない）

- [Astro PR #14080](https://github.com/withastro/astro/pull/14080)
- [PR #14181 での提案と助言](https://github.com/withastro/astro/pull/14181#issuecomment-3311059055)
-->

---
layout: default
class: ch3-detail chapter-three mdx-proposals mdx-upstream-proposal mdx-upstream-story
clicks: 2
---

## ライブラリへの提案と MDX の編集支援

<div v-if="$clicks === 0" class="mdx-lead">JavaScript から利用するための配布方法と機能を提案</div>
<div v-if="$clicks === 0" class="mdx-library-proposals">
  <section>
    <h3>mdxjs-rs</h3>
    <ul>
      <li>npm で配布する</li>
      <li>native bindings で<br />Node.js から呼ぶ</li>
    </ul>
  </section>
  <section>
    <h3>markdown-rs</h3>
    <ul>
      <li>GFM のテーブルを<br />AST から Markdown に戻す</li>
      <li>WASM bindings を作る</li>
    </ul>
  </section>
</div>

<BindingsRoutes v-if="$clicks === 1" />

<div v-if="$clicks >= 2" class="mdx-upstream-contribution">
  <div class="mdx-upstream-contribution-copy">
    <a class="mdx-upstream-post" href="https://bsky.app/profile/remcohaszing.nl/post/3mu5jnocvbk2r" target="_blank" rel="noreferrer" aria-label="Remco Haszing の告知投稿を開く">
      <img src="./images/mdx/remco-mdx-release.png" alt="Remco Haszing、@remcohaszing.nl による2026年8月28日の告知投稿。Volar ベースの MDX ツールの最終リリースと TypeScript 7.1 content mapper への移行を伝えている。" />
    </a>
    <div class="mdx-upstream-improvement">
      <h3>マージされた MDX の改善</h3>
      <p>不完全な import と export があっても、<br />補完と診断とホバーを継続できる。<br />Remco がリリースで紹介した。</p>
    </div>
  </div>
  <a class="mdx-upstream-post" href="https://bsky.app/profile/remcohaszing.nl/post/3mu5jrfpj222r" target="_blank" rel="noreferrer" aria-label="Remco Haszing の貢献を紹介する返信を開く">
    <img src="./images/mdx/remco-mdx-contribution.png" alt="Remco Haszing、@remcohaszing.nl による2026年8月28日の返信。構文エラーがあっても Editor の支援を継続できる貢献を紹介している。mdx-analyzer PR #528 のプレビュー全体を含む。" />
  </a>
</div>

<Ref v-if="$clicks === 0"><a href="https://github.com/wooorm/mdxjs-rs/issues/71">mdxjs-rs Issue #71</a> と <a href="https://github.com/wooorm/markdown-rs/pull/184">markdown-rs PR #184</a> と <a href="https://github.com/wooorm/markdown-rs/pull/185">PR #185</a></Ref>
<Ref v-else-if="$clicks === 1"><a href="https://nodejs.org/api/n-api.html">Node-API</a> と <a href="https://napi.rs/docs/introduction/simple-package">NAPI-RS</a> と <a href="https://wasm-bindgen.github.io/wasm-bindgen/">wasm-bindgen</a></Ref>
<Ref v-else><a href="https://github.com/mdx-js/mdx-analyzer/pull/528" target="_blank" rel="noreferrer">MDX PR #528</a> と <a href="https://bsky.app/profile/remcohaszing.nl/post/3mu5jnocvbk2r" target="_blank" rel="noreferrer">Remco の告知</a> と <a href="https://bsky.app/profile/remcohaszing.nl/post/3mu5jrfpj222r" target="_blank" rel="noreferrer">貢献を紹介する返信</a></Ref>

<!--
発話 1217 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

初期表示で二つのライブラリへの提案をまとめる。クリック 1 で NAPI-RS と wasm-bindgen の図、クリック 2 で MDX の編集支援と OSS の話へ進む。改稿後の時間は未計測。
読みの目安：NAPI-RS（ナピ アールエス）。公式のプロジェクト表記は NAPI-RS。発音の公式指定は未確認。

### 発話

[初期表示]
利用しているライブラリの開発元にも提案しました。mdxjs-rs には、npm での配布と native bindings を Issue で提案しました。
markdown-rs には、テーブルを AST から Markdown へ戻す機能と、WASM bindings を提案しました。
[クリック 1]
bindings についての説明なんですが、JavaScript から Rust の関数を呼び、文字列などの値を受け渡す部分です。
Node-API は、Node.js からネイティブのコードを呼ぶための API です。NAPI-RS を使うと、Rust の関数を JavaScript に公開するコードや、TypeScript の型定義を作れます。JavaScript からは、その関数を呼んで結果を受け取れます。ネイティブのバイナリは、OS と CPU などに合うものをビルドして配布します。
wasm-bindgen は、Rust を WASM にしたときに、JavaScript と呼び出しや値をやり取りするコードを作ります。文字列を渡して、結果を文字列で受け取ることもできます。WASM と補助コードを配布して、対応する環境で動かします。
同じ Rust でも、何にビルドして、JavaScript からどう呼ぶかが違うんですね。どちらも、使ってもらう環境での検証が必要です。
NAPI-RS でネイティブの実装を配布するなら、対応する OS と CPU の組み合わせで、ビルドして、テストして、配布し続ける必要があります。NAPI-RS はその仕組みも用意してくれますが、対応する環境と、どこまで保守を続けるかは自分たちで決めるんですね。
僕は、その範囲の広さに驚きました。JavaScript から呼べて便利、速くなりそう、だけでは採用を決められない。保守を続けられるかも考える必要がありました。
MDX のライブラリへの提案は採用の見通しが立たなかったため、必要な機能を自分で検証する xmdx も作りました。

[クリック 2]
提案がすぐ採用されなくて、しんどいこともあったんですね。でも、そこでやり取りが終わったわけでもなくて。MDX にもコントリビュートしたいと話したら、Astro のメンバーに Remco を紹介してもらいました。親切に、手取り足取り教えてもらって、編集支援の改善に取り組めました。
不完全な import と export があると、ファイル全体の補完と診断とホバーが止まっていたんですね。試作で学んだエラー回復を使って、書いている途中でも支援を続けられるようにしました。この改善はマージされて、Remco がリリースで紹介してくれました。
僕は、OSS の面白さは、人とのやり取りにもあると思っています。自分が使っているライブラリも、誰かが作ってくれたものなんですよね。
助けてくれた人に直接返すこともあるし、別のプロジェクトに貢献することもある。受け取った知識や助けを、次の人へ渡せる。そのバトンがつながっていく感じが、OSS をやっていて楽しいんですよね。

### 確認メモ（発表では話さない）

mdxjs-rs #71 は Issue、markdown-rs #184 と #185 は未マージの PR、mdx-analyzer #528 はマージ済みの PR。#528 は 2026 年 8 月 25 日、Remco の投稿は 8 月 28 日。ESM は acorn-loose、JavaScript expression は厳密な Parser で解析する。図は napi-rs でネイティブのアドオンを作る方法と、wasm-bindgen で WASM と JavaScript を呼び合う方法の例。現在の napi-rs は WASM と WASI にも対応しており、napi-rs がネイティブだけを扱うという分類ではない。Node-API の Node は Node.js を指し、AST の node とは別。配布の比較は現在の選択肢であり、提案当時の機能一覧ではない。必要な環境では libc の違いも確認する。OS と CPU ごとの最適化コードを必ず手書きするという意味ではない。保守範囲の広さに驚いたことは本人の経験。環境の確認に関する ChristianMurphy のコメントは他者の PR #182 に対するもので、本人の PR #185 とは区別する。

### 出典と確認資料（発表では話さない）

- [Node-API](https://nodejs.org/api/n-api.html)
- [wasm-bindgen](https://wasm-bindgen.github.io/wasm-bindgen/)
- [NAPI-RS の生成物とビルドとテストと配布](https://napi.rs/docs/introduction/simple-package)
- [NAPI-RS の対象環境とクロスビルド](https://napi.rs/docs/cross-build)
- [napi-rs の WebAssembly と WASI](https://napi.rs/docs/concepts/webassembly)
- [PR #182 に対する ChristianMurphy のコメント](https://github.com/wooorm/markdown-rs/pull/182#issuecomment-2993743993)
- [参照資料](https://bsky.app/profile/remcohaszing.nl/post/3mu5jnocvbk2r)
- [参照資料](https://bsky.app/profile/remcohaszing.nl/post/3mu5jrfpj222r)
- [mdxjs-rs Issue #71](https://github.com/wooorm/mdxjs-rs/issues/71)
- [markdown-rs PR #184](https://github.com/wooorm/markdown-rs/pull/184)
- [PR #185](https://github.com/wooorm/markdown-rs/pull/185)
- [MDX PR #528](https://github.com/mdx-js/mdx-analyzer/pull/528)
-->

---
layout: default
class: ch3-detail chapter-three mdx-integration
clicks: 2
---

## Processor を自作して Astro に組み込む

<div class="mdx-relation" :class="{ 'is-rust-focus': $clicks === 1 }" role="group" aria-label="Astro と Vite と Rollup、および Astro integration と Vite plugin と Node-API bindings と Compiler の関係">
  <svg class="mdx-relation-lines" viewBox="0 0 868 398" aria-hidden="true">
    <defs><marker id="mdx-relation-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 1 1 L 9 5 L 1 9" /></marker></defs>
    <g class="mdx-relation-context">
      <path d="M 240 64 H 300" /><path d="M 550 64 H 634" />
      <path d="M 120 104 V 162" /><path d="M 240 206 H 300" />
      <path d="M 425 104 V 162" />
    </g>
    <path class="mdx-relation-call" d="M 425 254 V 306" />
    <path class="mdx-relation-native" d="M 550 350 H 634" />
  </svg>
  <div class="mdx-relation-context">
    <div class="mdx-starlight">Starlight のサイトが利用</div>
    <section class="mdx-relation-node mdx-node-astro"><strong>Astro</strong></section>
    <section class="mdx-relation-node mdx-node-vite"><strong>Vite</strong></section>
    <section class="mdx-relation-node mdx-node-rollup"><span>Bundler</span><strong>Rollup</strong><small>module をまとめる</small></section>
    <section class="mdx-relation-node mdx-node-integration"><strong>Astro integration</strong></section>
    <section class="mdx-relation-node mdx-node-plugin"><strong>Vite plugin</strong><small>Astro の<br />モジュールに変換</small></section>
    <span class="mdx-edge-label mdx-edge-use">利用</span>
    <span class="mdx-edge-label mdx-edge-build">本番で<br />利用</span>
    <span class="mdx-edge-label mdx-edge-introduce">導入</span>
    <span class="mdx-edge-label mdx-edge-register">登録</span>
    <span class="mdx-edge-label mdx-edge-hook">hook を実行</span>
  </div>
  <section class="mdx-relation-node mdx-node-bindings"><strong>Node-API bindings</strong><small>JavaScript から Rust を呼ぶ</small></section>
  <section class="mdx-relation-node mdx-node-compiler"><strong>Compiler</strong><small>Rust でパースと変換<br />MDX のコードを生成</small></section>
  <span class="mdx-edge-label mdx-edge-binding-call">呼び出し</span>
  <span class="mdx-edge-label mdx-edge-compiler-call">呼び出し</span>
</div>

<Ref href="https://github.com/jp-knj/xmdx">xmdx と Astro integration</Ref>

<!--
発話 296 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリック 1 で bindings と Rust を強調し、クリック 2 で全体図へ戻す。

### 発話

[初期表示]
ここからは、自作した xmdx の中身です。Astro の integration として導入し、Vite plugin を登録する形にしました。

[クリック 1]
Rust の Compiler では、MDX のコードを作る部分に mdxjs-rs を使っています。JavaScript から呼ぶために、先ほどの Node-API bindings を組み合わせました。

[クリック 2]
ここまでを Astro integration としてまとめて、Starlight のサイトに組み込みました。当時の Astro の公式ドキュメントで、本文が変換できるか、表示とビルドが動くかを確認しました。次は、Rust から何を返し、JavaScript で何をする必要があったかです。

### 確認メモ（発表では話さない）

参照する試作は Astro 5 と Vite 6 と Rollup の組み合わせ。本番ビルドと開発時の依存関係の事前バンドルを混同しない。Rust の MDX コード生成には mdxjs-rs を利用。frontmatter と見出し情報は xmdx が取得する。実装の関数名は発話しない。

### 出典と確認資料（発表では話さない）

- [参照資料 1](https://github.com/jp-knj/xmdx/tree/7a89fdb17140e2b710e40d52d26338d978bc5c13)
-->

---
layout: default
class: ch3-detail chapter-three mdx-transfer
clicks: 2
---

## 本文の変換に加えて必要だったこと

<div class="mdx-transfer-diagram" :data-transfer-step="$clicks" role="group" aria-label="MDX の文字列を Rust に渡し、生成コードと frontmatter と見出し情報を JavaScript で Astro に統合する流れ">
  <div class="mdx-transfer-call">
    <section class="mdx-transfer-node mdx-transfer-source">
      <strong>Vite plugin</strong>
      <span>MDX ファイルの<br />文字列を渡す</span>
    </section>
    <svg class="mdx-transfer-arrow" viewBox="0 0 40 24" aria-hidden="true"><path d="M2 12 H36 M29 5 L36 12 L29 19" /></svg>
    <section class="mdx-transfer-node mdx-transfer-binding">
      <strong>Node-API bindings</strong>
      <span>Node.js の JavaScript から<br />Rust を呼び、値を受け渡す</span>
    </section>
    <svg class="mdx-transfer-arrow" viewBox="0 0 40 24" aria-hidden="true"><path d="M2 12 H36 M29 5 L36 12 L29 19" /></svg>
    <section class="mdx-transfer-node mdx-transfer-rust" :class="{ 'is-current': $clicks === 0 }">
      <strong>Rust の Compiler</strong>
      <span>MDX をパースし、<br />コードに変換する</span>
    </section>
  </div>
  <div class="mdx-transfer-return">
    <span>Node-API bindings 経由で返す</span>
    <svg viewBox="0 0 868 36" aria-hidden="true"><path d="M736 0 V16 H434 V32 M428 26 L434 32 L440 26" /></svg>
  </div>
  <section class="mdx-transfer-result" :class="{ 'is-current': $clicks === 1 }">
    <div class="mdx-transfer-label">JavaScript が受け取る 3 種類の情報</div>
    <div class="mdx-transfer-values">
      <div><strong>生成コード</strong><span>本文を描画するコード</span></div>
      <div><strong>frontmatter</strong><span>タイトルなどのデータ</span></div>
      <div><strong>見出し情報</strong><span>目次と見出しの ID</span></div>
    </div>
  </section>
  <svg class="mdx-transfer-down" viewBox="0 0 24 22" aria-hidden="true"><path d="M12 1 V19 M6 13 L12 19 L18 13" /></svg>
  <section class="mdx-transfer-js" :class="{ 'is-current': $clicks >= 2 }">
    <div class="mdx-transfer-label">JavaScript が Astro に統合する</div>
    <div class="mdx-transfer-pipeline">
      <div class="mdx-transfer-step"><span>Astro の<br />モジュールに<br />変換する</span></div>
      <svg class="mdx-transfer-arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M1 12 H21 M15 6 L21 12 L15 18" /></svg>
      <div class="mdx-transfer-step"><span>コンポーネントへの<br />対応と<br />シンタックスハイライト</span></div>
      <svg class="mdx-transfer-arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M1 12 H21 M15 6 L21 12 L15 18" /></svg>
      <div class="mdx-transfer-step"><span>JSX を<br />JavaScript に<br />変換する</span></div>
      <svg class="mdx-transfer-arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M1 12 H21 M15 6 L21 12 L15 18" /></svg>
      <div class="mdx-transfer-step"><span>Vite に<br />モジュールを返す</span></div>
    </div>
  </section>
</div>

<Ref href="https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/load-handler.ts">xmdx の MDX 変換と Astro への統合</Ref>

<!--
発話 441 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

初期表示で入力を短く説明する。クリック 1 で戻り値と見出し情報の不具合、クリック 2 で Astro への統合と学びを話す。

### 発話

[初期表示]
Rust には MDX の文字列を渡します。そこから、サイトに必要な情報をどう受け取るかも、自分たちで実装する必要がありました。

[クリック 1]
返すのは、本文のコードと frontmatter と見出し情報です。frontmatter はページのデータで、見出し情報は目次やリンクに使います。
実際、インデントしたコードブロックの終わりを判定できず、その後の見出しを取得できない不具合もありました。本文に加えて、こうした情報も正しくそろえる必要があったんですね。

[クリック 2]
JavaScript では、Astro のモジュールに合わせ、Starlight のコンポーネントやコードの色付けにも対応しました。扱えない入力には、既存の JavaScript の MDX Compiler を使う仕組みも用意しました。
だから、ベンチマークを比べるときも、同じ入力と機能、キャッシュの条件をそろえたいんですね。必要なプラグインが動くか、本文や目次の結果が保てるかも確認する。その条件で、サイト全体がどれだけ速くなるかを比べる必要があると思いました。

### 確認メモ（発表では話さない）

Astro に提案した AST Bridge と別の試作。この図は生成コードと付随情報を返し、AST 全体を往復させる図ではない。参照コミットは 7a89fdb17140e2b710e40d52d26338d978bc5c13。キャッシュと入力前の調整と設定値は図で省略。生成コードに JSX が含まれるかは設定で異なる。非対応の入力には JavaScript の MDX 実装を使う fallback がある。実装の関数名と参照先は images/mdx/README.md に記録。
見出しの不具合は astro-xmdx の CHANGELOG の修正記録を参照する。MDX の JSX 内でインデントしたコードブロックの終了を見落とし、後続の見出しを取得できなかった。今回は再現テストを実行していない。xmdx の試作で必要だった対応の例として説明し、2025 年 7 月の提案時点で発生したとは断定しない。詳しい確認内容は xmdx-rehearsal-notes.md にまとめた。

### 出典と確認資料（発表では話さない）

- [xmdx の MDX 変換と Astro への統合](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/load-handler.ts)
- [astro-xmdx の見出し情報などの修正記録](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/CHANGELOG.md)
- [JavaScript の MDX Compiler を使う仕組み](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/fallback/compile.ts)
-->

---
layout: default
class: ch3-detail chapter-three ch3-recap-slide
---

## 第 3 章の結論

<table class="ch3-recap">
<thead><tr><th>必要な情報と条件</th><th>参考にできる基盤と経験</th></tr></thead>
<tbody>
<tr><td>JavaScript expression の AST</td><td>Oxc の Parser</td></tr>
<tr><td>元の空白とコメントの保持</td><td>Biome の Lossless CST</td></tr>
<tr><td>互換性と配布と統合</td><td>Markdown と MDX の試作</td></tr>
</tbody>
</table>
<div class="ch3-summary">欲しい情報と導入の条件から、基盤を選び直せる</div>

<!--
発話 175 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。発話後に次へ進む。

### 発話

JavaScript expression の AST は Oxc から取得できる。Biome には、元の文字も保持する設計があります。
MDX の試作では、既存プラグインとの互換性、配布、Astro への統合を考えました。
欲しい機能を基盤から利用できるか。それを、どんな条件で自分たちのツールに組み込めるか。ここまでを踏まえて、Astro が選び直した内容を確認します。

### 確認メモ（発表では話さない）

MDX の編集支援は本人の貢献の経験として、MDX のページで説明する。前提の変化をまとめるこの表では扱わない。MDX の試作と Astro Compiler の変更、xmdx と Sätteri の間に、未確認の直接的な因果関係を作らない。Astro syntax の規則と空白の設定は、第 4 章の新しい判断として説明する。
-->

---
layout: section
---

# 4. 新しい判断
## Astro は何を実装し、何を基盤に任せるのか

<!--
発話 26 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

これを踏まえて、Astro の新しい判断を確認します。

-->

---
layout: center
---

<Overview
  era="rust"
  :roles="{
    editor: 'Source の情報を、診断や補完につなげる',
    build: '変換されたコードをまとめ、実行や配信につなげる',
    content: 'Markdown と MDX のパースと変換',
  }"
/>

<!--
発話 106 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

全体像に戻ると、Astro Compiler は Oxc と Lightning CSS を使う形になりました。Astro のコードをパースして、ビルドで使うコードに変換する。そのときに得られる AST は、編集ツールでも使えます。

### 確認メモ（発表では話さない）

このページは全体の案内に絞る。Go と Rust の比較、Astro syntax の規則と空白の扱い、Compiler 内部の担当の順に説明する。

### 出典と確認資料（発表では話さない）

- [Astro の構文解析と AST](https://github.com/withastro/compiler-rs/blob/main/crates/astro_napi/src/lib.rs)
- [CSS の解析と生成](https://github.com/withastro/compiler-rs/blob/main/crates/astro_codegen/src/css_scoping.rs)
-->

---
layout: default
class: chapter-four ch4-choices
---

## Astro が選んだ実装

<table class="ch4-choice-table">
  <thead><tr><th>必要な機能</th><th>利用する基盤</th></tr></thead>
  <tbody>
    <tr><td>JavaScript の Parser と AST</td><td>Astro に対応させた Oxc</td></tr>
    <tr><td>TypeScript の変換と JS の出力</td><td>Oxc</td></tr>
    <tr><td>CSS のパースと出力</td><td>Lightning CSS</td></tr>
  </tbody>
</table>
<div class="ch4-choice-takeaway">Astro syntax と変換の規則は、Astro が保守する</div>

<!--
発話 118 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

一文で案内して次へ進む。

### 発話

具体的には、JavaScript の Parser と AST、TypeScript の変換には Oxc を使います。CSS は Lightning CSS です。Astro の構文にどう対応するか、どんなコードに変換するかは、Astro が実装して保守します。

### 確認メモ（発表では話さない）

再利用する基盤を具体名で示し、次の Go と Rust の図へ進む。Oxc の Astro 拡張と CSS のスコープ規則も Astro が保守する。
-->

---
layout: default
class: chapter-four ch4-comparison
clicks: 1
---

## Go 版と Rust 版のツールチェーン

<div class="ch4-state"><b>{{ $clicks === 0 ? 'Before　Go 版' : 'After　Rust 版' }}</b><span>{{ $clicks === 0 ? 'Build 時の変換で HTML correction' : 'Compiler は HTML correction を行わない' }}</span></div>
<Overview
  :era="$clicks === 0 ? 'go' : 'rust'"
  :labels="{ build: 'Vite' }"
  :subnotes="{ build: '' }"
/>

<Ref href="https://github.com/withastro/roadmap/issues/1356">新 Compiler の方針と RFC #1356</Ref>

<!--
発話 292 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

初期表示は前半の Go の図。クリック 1 で、新しいツールチェーンを紹介した Rust の図へ切り替える。

### 発話

[初期表示]
前半と同じ Go の図です。Compiler は HTML5 Parser を基礎に、Astro の構文と変換を実装していました。ビルド時には HTML correction も担っていました。

[クリック 1]
Rust 版では、Astro に対応させた Oxc を使います。CSS で使っていた esbuild 由来の実装も、Lightning CSS に変わりました。
それから、Compiler では HTML correction を行わず、書かれた親子関係を保つ方針にしました。出力された HTML から DOM を作るのは、引き続きブラウザです。
言語を Rust に変えただけではなくて、Compiler がどこまで担当するかも選び直しているんですね。

### 確認メモ（発表では話さない）

Go の parse() には literal parsing があり、すべての API が常に HTML correction を行うとは説明しない。書かれた親子関係の保持と、構文エラーを許容することは別。閉じ忘れたタグや未終了の属性はエラーになる。Build の表示は Vite にそろえ、Compiler の変更を比較する。詳細な独自 AST と HTML correction と Astro Codegen の担当はノートと Compiler 内部の関連図で説明し、全体図の内部項目は共通設定に従う。

### 出典と確認資料（発表では話さない）

- [RFC #1356](https://github.com/withastro/roadmap/issues/1356)
- [Go の parse API](https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#parse-astro-and-return-an-ast)
-->

---
layout: default
class: ch3-detail chapter-four ch3-syntax-spec
---

## Astro syntax の規則と空白の扱い

<div class="ch3-syntax-date">2026 年 2 月、構文の共通基準を仕様ドラフトにまとめる</div>
<div class="ch3-syntax-setting">
  <p>Astro v7 の既定値は <code>compressHTML: 'jsx'</code></p>
  <p>JSX の規則で空白を扱う</p>
</div>

<div class="ch3-cols ch3-syntax">
<div>

```astro
---
const name = "Astro";
---
<h1 class="title">{name}</h1>
<p>複数のルート要素</p>
```

</div>
<div class="ch3-syntax-labels">
  <div><strong>Component script</strong><span><code>---</code> で囲んだ領域</span></div>
  <div><strong>HTML 属性</strong><span><code>class="title"</code></span></div>
  <div><strong>JavaScript expression</strong><span><code>{name}</code> の中の <code>name</code></span></div>
  <div><strong>複数のルート要素</strong><span><code>h1</code> と <code>p</code> を並べた Template</span></div>
</div>
</div>

<Ref><a href="https://github.com/withastro/compiler/blob/04170031ce2f30d1882fe480e87998197e0016aa/SYNTAX_SPEC.md">Astro syntax の仕様ドラフト</a> と <a href="https://docs.astro.build/en/guides/upgrade-to/v7/#new-default-whitespace-handling-compresshtml-jsx">v7 の空白規則</a> と <a href="https://docs.astro.build/en/reference/configuration-reference/#compresshtml">compressHTML の設定</a></Ref>

<!--
発話 254 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

クリックなし。発話後に次へ進む。

### 発話

Astro 自身も、どんな規則でコードを扱うかを整理しました。2026 年 2 月の仕様ドラフトで、構文の共通の基準を確認できるようになりました。
空白の扱いも選び直しています。Astro v7 では compressHTML の既定値が jsx になり、JSX の規則で空白を扱います。前半の、二つの span を改行して並べる例は、Astro1200 という表示になります。以前の扱いを続けることも設定で選べます。
構文の規則を文書化することと、出力する HTML の空白をどう扱うかを決めること。この二つも、Astro が担当する判断です。

### 確認メモ（発表では話さない）

仕様は 2026 年 2 月 3 日付の Draft。Component Script と Component Template は以前からの呼称。構文の呼称がこの時点で初めて定義されたとは説明しない。
compressHTML は既存の設定。Astro v7 では既定値が true から 'jsx' に変更された。14 枚目の二つの span を改行して並べる例では、'jsx' は Astro1200、従来の true は Astro 1200。既定の CSS の空白規則を前提とする。false は空白を保持する。
仕様ドラフトは位置情報の精度やエラー回復を保証しない。元の文字を保持する Lossless CST と、出力する HTML の空白をどう扱うかは別の判断。

### 出典と確認資料（発表では話さない）

- [Astro v7 の空白規則](https://docs.astro.build/en/guides/upgrade-to/v7/#new-default-whitespace-handling-compresshtml-jsx)
- [compressHTML の設定](https://docs.astro.build/en/reference/configuration-reference/#compresshtml)
- [Astro syntax の仕様ドラフト](https://github.com/withastro/compiler/blob/04170031ce2f30d1882fe480e87998197e0016aa/SYNTAX_SPEC.md)
-->

---
layout: default
class: chapter-four ch4-compiler
---

## Compiler 内部の関連図

<div class="ch4-diagram ch4-compiler-diagram">
  <svg class="ch4-lines" viewBox="0 0 868 398" aria-hidden="true">
    <defs><marker id="ch4-compiler-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1,1 L9,5 L1,9" /></marker></defs>
    <path d="M175,68 V145" /><path d="M675,68 V145" />
    <path d="M350,191 H479" />
    <path d="M600,236 V269 H404 V301" /><path d="M745,236 V301" />
  </svg>
  <div class="ch4-node ch4-api"><strong>Astro の公開 API と Node-API bindings</strong><span>parse() と transform()</span></div>
  <div class="ch4-node ch4-parser"><strong>Oxc Parser と AST</strong><span>Astro syntax への対応</span></div>
  <div class="ch4-node ch4-codegen ch4-owned"><strong>Astro Codegen</strong><span>Astro の変換と CSS スコープ規則</span></div>
  <div class="ch4-node ch4-oxc"><strong>Oxc Transformer と Codegen</strong><span>TypeScript の変換と JS の生成</span></div>
  <div class="ch4-node ch4-css"><strong>Lightning CSS</strong><span>CSS のパースと出力</span></div>
  <span class="ch4-edge ch4-edge-parse">パースを呼ぶ</span>
  <span class="ch4-edge ch4-edge-transform">変換を呼ぶ</span>
  <span class="ch4-edge ch4-edge-ast">AST を渡す</span>
  <span class="ch4-edge ch4-edge-js">変換と生成を利用</span>
  <span class="ch4-edge ch4-edge-css">パースと出力を利用</span>
</div>

<Ref href="https://github.com/withastro/compiler-rs/tree/main/crates">Compiler の実装と依存関係</Ref>

<!--
発話 300 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

もう少し中を見ると、Astro の構文に対応させた Oxc でパースします。前半で欲しかった JavaScript expression の AST も、ここから受け取れるんですね。Oxc を Astro に対応させた部分は、Astro が保守します。
そこから実行するコードを作るのが Astro Codegen です。TypeScript の変換と JavaScript の出力には、Oxc の機能を使います。
CSS をパースして出力するのは Lightning CSS です。ただ、このスタイルをどのコンポーネントに限定するか、その規則は Astro が実装します。ライブラリの機能を使いながら、Astro として決める部分を実装しているんですね。

### 確認メモ（発表では話さない）

parse() は AST と位置情報を返す。transform() は解析の後に Astro Codegen を呼ぶ。Oxc の Astro 拡張も保守範囲に含む。CSS のスコープ規則まで Lightning CSS に任せる説明はしない。実装言語、Node-API や WASM という配布方法、AST の設計は別の判断。

### 出典と確認資料（発表では話さない）

- [astro_napi](https://github.com/withastro/compiler-rs/blob/main/crates/astro_napi/src/lib.rs)
- [Astro Codegen](https://github.com/withastro/compiler-rs/tree/main/crates/astro_codegen/src/printer)
- [CSS scoping](https://github.com/withastro/compiler-rs/blob/main/crates/astro_codegen/src/css_scoping.rs)
- [Cargo.toml](https://github.com/withastro/compiler-rs/blob/main/Cargo.toml)
- [Compiler の実装と依存関係](https://github.com/withastro/compiler-rs/tree/main/crates)
-->

---
layout: default
class: chapter-four ch4-tools
---

## Compiler とツールの分担

<div class="ch4-responsibilities">
  <section><h3>Compiler が提供する情報</h3><ul class="ch4-list"><li>Astro の親子関係と Source の位置情報</li><li>埋め込まれた JavaScript の AST</li><li>JavaScript expression の演算子と識別子</li></ul></section>
  <section><h3>ツールが担当する機能</h3><ul class="ch4-list"><li>Linter は規則の検査、Formatter は整形を行う</li><li>Language Tool は宣言と参照、型情報を使って診断と補完を作る</li><li>Astro syntax と位置情報、不完全な入力を扱う</li></ul></section>
</div>

<Ref href="https://github.com/withastro/compiler-rs">Rust Compiler の公開 API と AST</Ref>

<!--
発話 172 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Compiler から、JavaScript expression の AST と位置情報を受け取れるようになりました。前半では、欲しいデータを得るために、ツールでパースし直していましたよね。その入口を変えられるわけです。
そのデータで何を検査するか、どう整形するかは、引き続きツールが決めます。実際に使っている例が、次の Prettier plugin です。

### 確認メモ（発表では話さない）

RFC は実行コードの生成と Language Server に渡す TSX を別の要件として扱う。現在のツールがすべて Rust Compiler へ移行済みとは説明しない。

### 出典と確認資料（発表では話さない）

- [Rust Compiler の公開 API と AST](https://github.com/withastro/compiler-rs)
-->

---
layout: default
class: chapter-four ch4-formatter-reuse
---

## Compiler を整形ツールでも再利用する

<FormatterReuse />

<Ref><a href="https://github.com/withastro/prettier-plugin-astro/blob/12c5a89d63227c7992f63a1d4e5ad08baecbf705/src/parser.ts">Astro plugin の実装</a> と <a href="https://github.com/oxc-project/oxc/issues/19715">Oxfmt の対応計画</a></Ref>

<!--
発話 262 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Rust Compiler を使う Astro の Prettier plugin は、すでに公開されています。Compiler から受け取った AST をプラグインで扱える形にして、Prettier の機能と組み合わせて整形します。
それから、Oxc の Formatter である Oxfmt でも、このプラグインと Rust Compiler を使う計画があります。ここは、まだ Astro 対応が提供されたわけではありません。
別のツールが Astro に対応するときも、Compiler とプラグインを再利用できる。この先につながる話として、ここも気になっています。

### 確認メモ（発表では話さない）

上段は公開済みの呼び出し関係。Astro plugin の Parser は Rust Compiler の parse() を呼ぶ。AST の調整とコメントの扱い、Prettier の ESTree Printer の利用も行う。Rust Compiler に変われば、すべての調整や再パースが不要になるとは説明しない。

下段は Oxfmt の対応計画で、実装済みの機能ではない。2026 年 10 月 1 日の公式の対応表は Astro を未対応とし、Issue #19715 の Astro の項目も未完了。計画では Prettier plugin と @astrojs/compiler-rs を利用する。Astro の全体を Oxfmt が直接 Rust で整形するという説明はしない。

2026 年 8 月 20 日の Erika の投稿は、Astro の Prettier plugin 1.0 の beta の紹介。発表者が関心を持った今後の再利用の例として Oxfmt を紹介し、Astro が Rust を選んだ原因としては扱わない。

### 出典と確認資料（発表では話さない）

- [Erika の投稿と Prettier plugin](https://bsky.app/profile/erika.florist/post/3mtjah7okdc22)
- [Astro plugin の Parser](https://github.com/withastro/prettier-plugin-astro/blob/12c5a89d63227c7992f63a1d4e5ad08baecbf705/src/parser.ts)
- [Astro plugin の Printer](https://github.com/withastro/prettier-plugin-astro/blob/12c5a89d63227c7992f63a1d4e5ad08baecbf705/src/printer/index.ts)
- [Oxfmt の対応表](https://oxc.rs/compatibility.html)
- [Oxfmt の Astro 対応計画](https://github.com/oxc-project/oxc/issues/19715)
-->

---
layout: default
class: chapter-four ch4-content
---

## Astro と Content Processor の分担

<Overview highlight="mdsource,content,build,browser" :labels="{ build: 'Build' }" />
<ul class="ch4-list">
  <li>Astro は Processor を選ぶ入口と、Collections と Build への統合を担当</li>
  <li>Processor は Markdown と MDX の解析と変換、plugin の実行を担当</li>
</ul>

<!--
予定時間 19:53 から 20:13（20 秒）。発話 110 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Content でも分担を選びます。Astro は、Processor を選ぶ入口と、Collections とビルドへの統合を担当します。Markdown と MDX の解析と変換、プラグインの実行は Processor が担当します。

### 確認メモ（発表では話さない）

Astro Compiler と Content Processor は別に選ぶ。

### 出典と確認資料（発表では話さない）

- [Astro の Markdown Processors](https://docs.astro.build/en/guides/markdown-content/#markdown-processors)
-->

---
layout: default
class: mdx-source-post
---

## Sätteri が選んだ Rust と JavaScript の分担

<div class="mdx-post-author">Erika <span>@erika.florist</span><time>2026年4月9日</time></div>
<div class="satteri-growth-body">
  <div class="satteri-growth-context">計算負荷の高い部分は Rust。<br />柔軟な plugin は JavaScript。</div>
  <div class="satteri-growth-title">npm ダウンロードの推移</div>
  <div class="satteri-growth-rows">
    <div><span>9 月 3 日から 9 日</span><i style="--bar-width:45.6%"></i><strong>1,827,292</strong></div>
    <div><span>9 月 10 日から 16 日</span><i style="--bar-width:77.2%"></i><strong>3,094,168</strong></div>
    <div><span>9 月 17 日から 23 日</span><i style="--bar-width:93.2%"></i><strong>3,735,680</strong></div>
    <div><span>9 月 24 日から 30 日</span><i style="--bar-width:100%"></i><strong>4,009,697</strong></div>
  </div>
  <div class="satteri-growth-note">2026 年の satteri パッケージ。人数ではなく、ダウンロード回数。</div>
</div>

<Ref><a href="https://api.npmjs.org/downloads/range/2026-08-01:2026-09-30/satteri">npm のダウンロード集計</a> と <a href="https://bsky.app/profile/pi0.io/post/3mgwljerlik2h">Pooya の Markdown の試作</a> と <a href="https://bsky.app/profile/erika.florist/post/3mj2tfwryw226">Erika の Sätteri 紹介</a></Ref>

<!--
発話 255 文字。今回の改稿後の所要時間は未計測。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

3 月に Pooya さんが紹介した md4x の試作を、mk.gg さんが Discord で共有して、僕にメンションをくれたんですね。Markdown と MDX がボトルネックかもしれないから、何かできるかもしれない、という問いかけでした。
そこから Erika さんが取り組むことになりました。僕も気になっていたところなので、実装が進んでいくのは嬉しかったです。
4 月に紹介された Sätteri では、計算負荷の高い部分を Rust に、柔軟に変更したいプラグインを JavaScript に分けています。次は、その間で何を受け渡すのかです。

### 確認メモ（発表では話さない）

Pooya Parsa の投稿は 2026 年 3 月 13 日で、md4x を利用する Astro の Markdown Renderer の試作を紹介している。2026 年 10 月 1 日に Bluesky の公開 API で投稿者と本文と日時を確認した。MDX Compiler の紹介ではない。

画面の Erika の投稿は 2026 年 4 月 9 日。3 月の投稿と区別して話す。49 枚目との順序は話題によるもので時系列ではない。mk.gg が Discord で投稿を共有し、発表者にメンションして問いかけ、Erika が取り組むことになった経緯は、発表者が練習で話した経験として記載する。非公開の会話を外部資料で確認したという意味ではない。イベントの翌日という日付の記憶は未確認のため発話へ含めない。

Pooya の投稿には 50 倍から 70 倍という数字と、コードの色付けは未実装という記載がある。試作の README にも remark と rehype のプラグインの実行は未実装と記載されている。投稿者が示した単体のベンチマークの数字であり、Astro のビルド全体の高速化や完全な互換性として説明しない。発話には倍率を加えない。

xmdx の提案が後から採用された、という説明にはしない。発表者も関心を持っていた課題に、別の実装で取り組む人がいた嬉しさを短く話す。以前の提案の採否と、Sätteri の開発を混同しない。

### 出典と確認資料（発表では話さない）

- [Erika の投稿と Sätteri](https://bsky.app/profile/erika.florist/post/3mj2tfwryw226)
- [Pooya の Markdown Renderer の試作](https://bsky.app/profile/pi0.io/post/3mgwljerlik2h)
- [astromd4x のベンチマークと未実装の機能](https://github.com/pi0/astro-md4x/blob/9ef1c52c8fdcdc964d847ee1642a1af32da65463/README.md)
-->

---
layout: default
class: chapter-four ch4-satteri
---

## Sätteri と plugin の関連図

<div class="ch4-diagram ch4-satteri-diagram">
  <svg class="ch4-lines" viewBox="0 0 868 402" aria-hidden="true">
    <defs><marker id="ch4-satteri-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1,1 L9,5 L1,9" /></marker></defs>
    <path d="M155,80 V146" /><path d="M155,210 V247" />
    <path d="M398,170 H545 V80" /><path d="M808,80 V191 H398" />
    <path class="ch4-branch" d="M155,316 V330 M143,330 H728" /><path d="M143,330 V343" /><path d="M434,330 V343" /><path d="M728,330 V343" />
  </svg>
  <div class="ch4-node ch4-satteri-api"><strong>JavaScript の satteri</strong><span>公開 API と plugin の登録</span></div>
  <div class="ch4-node ch4-visitor ch4-owned"><strong>JavaScript の plugin</strong><span>対象 node の visitor と ctx</span></div>
  <div class="ch4-node ch4-binding"><strong>satteri-napi-binding</strong><span>Node-API bindings</span></div>
  <div class="ch4-node ch4-rust"><strong>Rust の satteri</strong><span>解析と変換の API</span></div>
  <div class="ch4-node ch4-rust-parser"><strong>pulldown-cmark</strong><span>Markdown と MDX の解析</span></div>
  <div class="ch4-node ch4-rust-ast"><strong>satteri-ast</strong><span>MDAST と HAST</span></div>
  <div class="ch4-node ch4-rust-mdx"><strong>mdxjs-rs と Oxc</strong><span>MDX を JavaScript に変換</span></div>
  <span class="ch4-edge ch4-edge-call">API を呼ぶ</span>
  <span class="ch4-edge ch4-edge-native">Rust を呼ぶ</span>
  <span class="ch4-edge ch4-edge-visit">node 情報を渡す<br />visitor を実行</span>
  <span class="ch4-edge ch4-edge-mutations">ctx の変更内容を返す</span>
  <span class="ch4-edge ch4-edge-rust-parts">解析と AST と MDX 変換の部品を利用</span>
</div>

<Ref href="https://satteri.bruits.org/docs/plugin-api/">Sätteri の Plugin API</Ref>

<!--
予定時間 20:33 から 23:03（150 秒）。発話 943 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。最初の比較に約 1 分、続く Oxc の別の例に約 90 秒。画面の図が Sätteri であることを保ち、Oxc の例は言葉で区別する。

### 発話

xmdx の図では、MDX の文字列を Rust に渡し、生成コードと frontmatter と見出し情報を受け取り、JavaScript が Astro の実行形式に合わせました。ここで比較する Sätteri のプラグインの仕組みでは、AST を Rust が保持します。JavaScript は対象の node の情報を参照し、API で変更を依頼します。Rust がその変更を反映します。
Node-API は、Node.js の JavaScript とネイティブの実装の呼び出しや値の受け渡しを支える API です。ここでは Rust の実装を呼びます。どの情報を受け渡すかは、Node-API を利用する実装の設計です。
この比較は、xmdx の Astro への統合と Sätteri のプラグインの仕組みを選んで、JavaScript と Rust の担当を説明したものです。パッケージ全体の機能の比較ではありません。

別の例として、Oxc の AST の受け渡しを見ます。Rust で解析を速くしても、その結果を JavaScript から使える形にする時間がかかります。

分かりやすい方法は、Rust の AST を JSON の文字列にして渡し、JavaScript で JSON.parse() することです。文字列への変換と、そこからオブジェクトを作る工程が必要です。

バイナリ形式なら JSON の文字列は避けられます。ただし、受け渡すための別形式へ変換する設計なら、その変換にも時間がかかります。

Oxc が公開した raw transfer では、JavaScript が用意したメモリに Rust が AST を作ります。JavaScript は、Rust のメモリ上の配置に対応したコードで、AST のオブジェクトを作ります。Rust の AST を別の形式に変換する工程を省けるわけです。

JavaScript のオブジェクトを作る時間はかかるので、必要な部分だけを、参照した時点で作る工夫もあります。遅延デシリアライズです。使わない部分の生成と、その後のメモリの回収を減らせます。2025 年の記事では、これは試作段階でした。

Node-API を選ぶだけで、これらが決まるわけではありません。どの情報を、どれだけ、どんな形式で渡すか。プラグインの互換性と使いやすさも含めて設計する必要があります。

### 確認メモ（発表では話さない）

Astro に提案した AST Bridge の試作と、xmdx で生成コードを返す仕組みは別。Node-API は Rust に限らず、ネイティブの実装を Node.js から利用するための API である。xmdx の経験から Sätteri が生まれたという因果関係や、同じ受け渡し方式だという説明はしない。
Oxc は受け渡しの設計を比較する別の例である。このページの図は Sätteri を示す。xmdx と Sätteri が Oxc と同じ raw transfer を実装しているとは説明しない。Node-API 自体が任意の Rust の AST を自動的に JavaScript のオブジェクトにするわけではない。
JSON は文字列への変換と JSON.parse()、別のバイナリ形式はその形式への変換と復元を要する。Oxc の raw transfer は Rust の AST のメモリ配置を受け渡しの形式として使い、別形式への変換を省く。JavaScript のオブジェクトの生成は必要であり、その生成を必要な部分まで延期する遅延デシリアライズは別の工夫である。
2025 年 3 月の PR #9516 は、JavaScript が用意した ArrayBuffer を Rust の allocator のメモリにし、解析した AST をその領域に作る方式を説明している。JavaScript はそのデータから ESTree に対応するオブジェクトを作る。Rust の型のメモリ配置と、それを復元する JavaScript のコードを一致させる必要がある。配置や enum の値などに基づいて復元コードを生成する。
復元が終わるまで元のメモリを有効に保つ必要がある。遅延デシリアライズを行うなら、後で参照するデータがその時点でも有効でなければならない。対象環境のバイト順とメモリの配置や確保の制約も確認する。初期 PR は little-endian の環境を条件としており、すべての環境で任意の Rust のメモリを共有できるという説明ではない。
2025 年 10 月 9 日の記事は、raw transfer を採用したことと、遅延デシリアライズが試作段階だったことを分けて説明している。この記事だけで現在の全 API が遅延デシリアライズを行うとは判断しない。確認した eager.js の実装では AST 全体を復元してから buffer を再利用する。getter があることだけで、AST を遅延して復元していると説明しない。性能の数値は原稿に含めない。
51 枚目は上段が JavaScript、中段が Node-API bindings、下段が Rust の機能。npm の satteri package は公開 API と plugin の登録を提供する。satteri-napi-binding を介して Rust の satteri を呼ぶ。
図の pulldown-cmark は satteri-pulldown-cmark、mdxjs-rs は satteri-mdxjs-rs の略記。Rust の satteri は、MDX に対応した Parser の satteri-pulldown-cmark、MDAST と HAST を担う satteri-ast、Oxc を利用する MDX Compiler の satteri-mdxjs-rs を組み合わせる。関連部品には satteri-arena と Rust plugin を実装するための satteri-plugin-api もある。図は主な依存関係であり、すべての入力で同じ手順を実行するという意味ではない。
JavaScript plugin は対象の node の種類を指定し、visitor で検査する。node のプロパティは直接変更できず、変更は ctx の setProperty() や replaceNode() などで指定する。図の往復する線は、bindings を介した node の情報と変更内容の受け渡しを示す。visitor の完了後に変更が適用される。必要なら visitor の戻り値で node を交換することもできる。
この plugin API は remark と rehype の plugin API と同一ではない。既存 plugin を利用したい場合の unified の選択を 52 枚目へつなげる。

### 出典と確認資料（発表では話さない）

- [Sätteri の package 一覧](https://github.com/bruits/satteri#packages)
- [Plugin API](https://satteri.bruits.org/docs/plugin-api/)
- [Node-API](https://nodejs.org/api/n-api.html)
- [Oxc の raw transfer と遅延デシリアライズの記事](https://oxc.rs/blog/2025-10-09-oxlint-js-plugins.html#raw-transfer)
- [Oxc PR #9516 の実装説明](https://github.com/oxc-project/oxc/pull/9516)
- [Oxc の eager な復元の実装](https://github.com/oxc-project/oxc/blob/cef20b5794e2f832949459f0efb8a17465c4c609/napi/parser/src-js/raw-transfer/eager.js)
-->

---
layout: default
class: chapter-four ch4-config
---

## plugin の互換性から Processor を選ぶ

<ul class="ch4-list">
  <li>remark と rehype plugin を使うなら unified を選ぶ</li>
  <li>Sätteri への移行では、plugin の API も確認する</li>
</ul>



<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Astro Docs と Markdown Processors</Ref>

<!--
予定時間 23:03 から 23:28（25 秒）。発話 122 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

プラグインの互換性も、Processor を選ぶ条件です。Sätteri の API は remark と rehype の API と異なります。既存のプラグインを使い続けたい場合は、unified を選べます。速度と、必要な拡張機能の両方を確認します。

### 確認メモ（発表では話さない）

Astro v7 以降の Processor 選択の説明。個別の remarkPlugins と rehypePlugins の設定は画面で省略する。

### 出典と確認資料（発表では話さない）

- [Astro Docs と Markdown Processors](https://docs.astro.build/en/guides/markdown-content/#markdown-processors)
-->

---
layout: center
class: chapter-four ch4-recap
---

<Overview
  era="rust"
  :roles="{
    compiler: 'Astro syntax と変換を実装し、Oxc と Lightning CSS を利用',
    editor: 'AST と位置情報から、検査と整形と診断と補完を提供',
    content: 'Astro への統合と、解析と変換と plugin の実行を分担',
  }"
/>

<!--
予定時間 23:28 から 23:38（10 秒）。発話 61 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Astro が統合を担当し、解析と変換の基盤を利用する。Compiler と Content の両方で、保守の分担を選んでいます。

### 確認メモ（発表では話さない）

第 4 章の冒頭と同じ Rust の全体図を使用する。
-->

---
layout: default
class: body-center
---

## この章の結論

<div class="mt-10 text-xl leading-relaxed">
  <ul>
    <li>Rust への移行では、<b>Compiler の設計と保守範囲</b> も見直している</li>
    <li>汎用的な解析と変換には、<b>Oxc などの基盤</b> を利用する</li>
    <li>Astro は、<b>Astro syntax と変換と統合</b> を担当する</li>
    <li>用途に応じて、<b>Rust と JavaScript の役割</b> を分ける</li>
    <li>Astro Compiler と Markdown と MDX の Processor も、<br />それぞれの要件に合った構成を選ぶ</li>
  </ul>
</div>

<!--
予定時間 23:38 から 23:53（15 秒）。発話 81 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

今回の変更では、実装言語とともに設計と保守範囲を見直しています。汎用的な機能は基盤を利用し、Astro の構文と変換と統合を、自分たちの仕事として明確にしています。
-->

---
layout: statement
class: flex flex-col justify-center h-full
---

# Go で動いていたものを、<br />なぜ、Rust に書き直すのか？

<!--
予定時間 23:53 から 23:58（5 秒）。発話 27 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

Go で動いていたものを、なぜ、Rust に書き直すのか。

### 確認メモ（発表では話さない）

4 枚目と同じ問い。
-->

---
layout: default
class: body-center
---

## 最初の問いへの答え

<div class="grid grid-cols-2 gap-x-10 gap-y-8 mt-8 text-xl leading-relaxed">
  <div class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-sm uppercase tracking-widest text-black">当時の判断</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>高速な変換と、複数環境での実行</div>
      <div>Go と WASM が要件に合っていた</div>
    </div>
  </div>
  <div class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-sm uppercase tracking-widest text-black">発見した問題</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>Source の親子関係と位置情報への要求</div>
      <div>HTML correction による予想しにくい挙動</div>
      <div>独自実装の保守コスト</div>
    </div>
  </div>
  <div class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-sm uppercase tracking-widest text-black">前提の変化</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>Rust 基盤の成熟</div>
      <div>再利用できる範囲の拡大</div>
      <div>Astro syntax の整理</div>
    </div>
  </div>
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">
    <div class="text-sm uppercase tracking-widest text-black">新しい判断</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>保持する情報と変換する段階の明確化</div>
      <div>保守範囲を絞る</div>
      <div>改善し続けられる設計へ</div>
    </div>
  </div>
</div>

<!--
予定時間 23:58 から 24:20（22 秒）。発話 128 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

当時は、Go と WASM がビルドの要求に合っていました。その後、編集支援で必要な情報と、実装を保守する難しさが分かりました。
その間に、Rust の解析と変換の基盤が育ちました。利用できる部品が変わったから、情報の持ち方と、自分たちの実装範囲を選び直せたのです。

### 確認メモ（発表では話さない）

Go の採用が失敗だった、Rust なら必ず高速になるという一般論にはしない。
-->

---
layout: center
class: text-center
---

<div class="text-5xl font-700 leading-[1.5]" style="color: #7611A6">
  基盤を再利用し、<br />
  <span>自分たちの実装範囲を絞り、</span><br />
  <span>保守し続けられる設計にするため。</span>
</div>

<!--
予定時間 24:20 から 24:30（10 秒）。発話 48 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

基盤を再利用し、自分たちの実装範囲を絞り、保守し続けられる設計にするため。これが今日の答えです。
-->

---
layout: center
class: text-center
---

## ありがとうございました

<div class="mt-8 text-xl ">Vue Fes 楽しんでね。</div>

<!--
予定時間 24:55 から 25:00（5 秒）。発話 28 文字。予定配分であり、実測ではない。

### 進行案内（発表では話さない）

ページ内のクリックなし。発話後に次へ進む。

### 発話

ありがとうございました。Vue Fes、楽しんでください。
-->
