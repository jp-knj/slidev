---
theme: ./theme-light
author: jp-knj
title: Astro と Rust で考えるフロントエンドツールチェーンの今
info: |
  動いていた Go Compiler を、Astro はなぜ Rust で書き直したのか。
  当時の判断と発見した問題と前提の変化と新しい判断をたどり、補章で MDX と Sätteri を紹介する。
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
予定時刻：00:00 から 00:09（9 秒）
発話 62 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

今日は Astro Compiler を題材に、動いていたツールチェーンを、なぜ書き直すのか、という話をわたしの視点でお話します。
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
予定時刻：00:09 から 00:19（10 秒）
発話 55 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

自己紹介です。Astro のメンテナとして活動していて、Astro Japan Community も運営しています。

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
      <p class="thread-meta"><a href="https://x.com/pilcrowonpaper" target="_blank" rel="noreferrer"><b>pilcrow</b> @pilcrowonpaper</a></p>
      <p class="thread-text">Why isn’t anyone from @astrodotbuild here at @vuefes :(</p>
    </div>
  </li>
  <li class="thread-post thread-continues">
    <span class="thread-avatar avatar-astro" aria-hidden="true"></span>
    <div>
      <p class="thread-meta"><a href="https://x.com/astrodotbuild" target="_blank" rel="noreferrer"><b>Astro</b> @astrodotbuild</a></p>
      <p class="thread-text">@jp_knj was there!</p>
    </div>
  </li>
  <li class="thread-post thread-continues">
    <span class="thread-avatar avatar-pilcrow" aria-hidden="true"></span>
    <div>
      <p class="thread-meta"><a href="https://x.com/pilcrowonpaper" target="_blank" rel="noreferrer"><b>pilcrow</b> @pilcrowonpaper</a></p>
      <p class="thread-text">We need more people!</p>
    </div>
  </li>
  <li class="thread-post">
    <span class="thread-avatar avatar-astro" aria-hidden="true"></span>
    <div>
      <p class="thread-meta"><a href="https://x.com/astrodotbuild" target="_blank" rel="noreferrer"><b>Astro</b> @astrodotbuild</a></p>
      <p class="thread-text">Who is organizing Astro meetups in Japan?</p>
    </div>
  </li>
</ol>

<!--
予定時刻：00:19 から 00:48（29 秒）
発話 171 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

実は、Astro Japan Community を立ち上げたきっかけが、去年の Vue Fes だったんですね。Astro の認証まわりにも貢献した方。学生で。Lucia を開発した pilcrow ですね。Vue Fes に Astro の人はいないのか、と投稿したんです。そこから、コアメンバーも交えて、日本の Meetup は誰がやるんだろう、という話になりました。

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
予定時刻：00:48 から 01:04（16 秒）
発話 95 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

そこで僕が手を挙げて、コミュニティを立ち上げ、Meetup も開催しました。そのきっかけになった Vue Fes に、今年は登壇者として参加しています。Astro のコアメンバーも登壇してくれました。

### 確認メモ（発表では話さない）

投稿の日時と出典と画像の撮影方法は images/community/README.md を参照する。


### 出典と確認資料（発表では話さない）

- [PLAID の開催告知](https://x.com/PLAID_Tech/status/1991667457032089615)
-->

---
layout: statement
class: flex flex-col justify-center h-full intro-question
---

# Go で動いていたものを、<br />なぜ、Rust に書き直すのか？

<a class="intro-question-video" href="https://www.youtube.com/live/wZ3OZh9IP54?t=7644" target="_blank" rel="noreferrer" aria-label="Vue Amsterdam での Matt Kane の発表動画を開く">
  <figure class="intro-question-screenshot">
    <img src="./images/talks/vue-amsterdam-edited.png" alt="Vue Amsterdam の発表スライド。Rust とツールのロゴが並ぶ。" />
    <figcaption>Vue Amsterdam の発表動画</figcaption>
  </figure>
</a>

<!--
予定時刻：01:04 から 01:16（12 秒）
発話 86 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

Matt は Vue Amsterdam で、Astro Compiler を Rust で書き直した話をしていました。
今日は、なぜ Go から Rust へ書き直すのか、その背景を掘り下げます。
-->

---
layout: default
class: body-center
---

## 話すこと

<div class="grid grid-cols-1 gap-4 mt-10">
  <div>
    <div class="text-3xl font-600 mt-1" style="color: var(--astro-heading)">1. 当時の判断</div>
    <div class="text-lg mt-2">なぜ最初に Go を選んだのか</div>
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
予定時刻：01:16 から 01:30（14 秒）
発話 100 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

当時、なぜ Go を選んだのか。使い続けて、どんな問題が分かったのか。その間に、利用できる技術はどう変わったのか。最後に、どんな判断で書き直すのか。この４つの視点で歴史を紐解いていこうかなと思っています。
-->

---
layout: section
---

# 1. 当時の判断
## なぜ最初に Go を選んだのか

<!--
予定時刻：01:30 から 01:35（5 秒）
発話 22 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

まず、Astro が Go を選んだときの話です。
-->

---
layout: default
class: ch1-start
---

## Astro 0.x の出発点

<div class="flex flex-col gap-8">
  <div class="text-2xl">Compiler とビルド基盤は、別の役割を持つ</div>
  <Overview
    visible="source,compiler,build,browser"
    :labels="{ compiler: 'Svelte Compiler', build: 'Snowpack' }"
    :icons="{ compiler: 'svelte', build: 'snowpack' }"
    :subnotes="{ compiler: 'fork を拡張', build: 'ビルドと配信' }"
  />
  <div class="text-2xl">Astro の構文を変換し、ビルド基盤へ渡す</div>
</div>

<Ref href="https://www.youtube.com/watch?v=bmWQqAKLgT4&amp;t=460s">VITE: The Documentary（Snowpack の話は 7:40 から）</Ref>

<!--
予定時刻：01:35 から 01:56（21 秒）
発話 144 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

まず、Compiler とビルド基盤の役割を分けて見ます。初期の Astro は Svelte Compiler の fork で構文を変換し、Snowpack でビルドと開発中の配信を行っていました。この Compiler を書き直すとき、どんな言語を選べたんでしょうか。背景は下の動画でも紹介されています。

### 確認メモ（発表では話さない）

Svelte の fork は Compiler の実装。Snowpack はビルドを担当する。
配信は開発サーバーからブラウザへのファイル配信を指す。Snowpack の開発中の動作を説明し、本番環境でのサイト公開やホスティングとは区別する。
CultRepo の VITE: The Documentary は確認資料。動画の概要欄で、7 分 40 秒から Snowpack との比較、20 分 21 秒から Astro の Vite 採用を扱うことを確認した。このページの下端に、7 分 40 秒から再生するリンクを表示する。Vite の採用経緯は 10 ページのトークスクリプトで話す。

### 話す場合の補足（任意）

Astro のビルド基盤は、Snowpack から Vite へ移行しました。Vite の改善や Rollup のプラグインを、Astro でも利用できるようになるからです。

### 補足の確認事項（発表では話さない）

Snowpack と Vite は、図の Build の役割を担う基盤。Astro 0.21 では、ビルド基盤を Snowpack から Vite へ移行した。同時期に行った、Svelte Compiler の fork から Go Compiler への移行とは担当が異なる。
Vite の採用理由として、当時の記事は保守と資料の充実、性能、エラーメッセージ、コミュニティと Rollup のプラグインを挙げている。改善を複数のフレームワークで共有できることも説明している。
この補足は、利用できる基盤を選び直すという講演の主題につながる。本編の時間に合わせて省略できる。任意の補足は発話文字数に含めていない。


### 出典と確認資料（発表では話さない）

- [Snowpack から Vite への移行の説明](https://astro.build/blog/astro-021-preview/)
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

## 2021 年、Go と Rust が選ばれていた

<div class="mt-12 relative">

  <!-- 軸。ドットの中心（上から 50px）に合わせて引く -->
  <div class="absolute left-0 right-0 top-[50px] h-[2px] bg-[#D9D3E2]"></div>

  <div class="relative flex items-start">
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Feb</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-vitejs class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Vite 2.0</div>
      <div class="text-xl mt-1 h-7 leading-7">esbuild を利用</div>
      <img src="./images/logos/gopher-cutout.png" alt="Go" class="h-16 mt-3" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Sep</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-rome-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Rome</div>
      <div class="mt-1 h-7" aria-hidden="true"></div>
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-11 mt-6" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Oct</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-parcel-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Parcel 2</div>
      <div class="mt-1 h-7" aria-hidden="true"></div>
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-11 mt-6" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Oct</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-nextjs-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Next.js 12</div>
      <div class="mt-1 h-7" aria-hidden="true"></div>
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-11 mt-6" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-primary font-700 h-11 leading-none">Nov</div>
      <div class="w-5 h-5 rounded-full bg-[#BC52EE] -mt-[3px]"></div>
      <logos-astro-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug text-primary font-600">Astro 0.21</div>
      <div class="mt-1 h-7" aria-hidden="true"></div>
      <img src="./images/logos/gopher-cutout.png" alt="Go" class="h-16 mt-3" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-black h-11 leading-none">Dec</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-turborepo-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Turborepo</div>
      <div class="mt-1 h-7" aria-hidden="true"></div>
      <img src="./images/logos/gopher-cutout.png" alt="Go" class="h-16 mt-3" />
    </div>
  </div>
</div>

<!--
予定時刻：01:56 から 02:10（14 秒）
発話 83 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

2021 年には Rust を採用するツールが増えていました。一方、Vite が使う esbuild や当時の Turborepo は Go です。Go も実績のある選択肢だったんですね。

### 確認メモ（発表では話さない）

Vite 自体を Go で実装したという説明ではない。製品の採用時期は既存の参照資料に基づく。
-->

---
layout: default
class: go-era-slide go-era-build
---

<div class="go-era-heading">
  <h2>Astro v1 の構成</h2>
  <span class="go-era-year">2022 年</span>
</div>

<div class="go-era-body">
  <div class="go-era-summary">Compiler は Go、ビルド基盤は Vite</div>

  <Overview
    visible="source,compiler,build,browser"
    era="go"
    :subnotes="{ build: 'Rollup\nesbuild' }"
  />

  <div class="go-era-reason">
    <div class="text-2xl font-600 text-primary">Nate Moore が挙げた Go の選定理由</div>
    <div class="text-xl mt-2">esbuild が Go だった。Go は学びやすかった。</div>
  </div>
</div>

<Ref>
  <a class="block w-fit" href="https://natemoo.re/posts/hello-from-the-other-side/" target="_blank" rel="noreferrer">Nate Moore: Hello from the other side</a>
  <a class="block w-fit mt-1" href="https://www.youtube.com/watch?v=bmWQqAKLgT4&amp;t=1221s" target="_blank" rel="noreferrer">VITE: The Documentary（Astro の Vite 採用は 20:21 から）</a>
</Ref>

<!--
予定時刻：02:10 から 03:00（50 秒）
発話 283 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

Astro は 2021 年の 0.21 で Go Compiler と Vite に移行し、v1 でもこの構成を使いました。Compiler が Astro の構文を変換し、Vite がビルドを担当します。Vite の改善や Rollup のプラグインを利用できることも、採用理由の一つでした。
Nate Moore は、esbuild が Go だったことと、学びやすさを理由に挙げています。
実装では HTML5 Parser の fork と、esbuild 由来の CSS Parser を利用していました。僕は、参考になる実装を利用できた点にも納得しています。ここからは、この Compiler を使い続けて分かった問題です。

### 確認メモ（発表では話さない）

Go の経験者だったという理由へ変更しない。Compiler 内の esbuild は CSS の解析と生成、Vite の部分の esbuild は TypeScript の変換を担当する。HTML5 Parser 由来の実装を Astro Template Syntax に対応させた。原文は "esbuild was written in Go and it was easy to learn. We didn't overthink it." で、深い技術的判断として語らない。`internal/parser.go` と `internal/token.go` は `golang.org/x/net/html` の fork（Copyright The Go Authors）。JavaScript は `tdewolff/parse` による走査（`internal/js_scanner`）だけで、完全な JS Parser はない。


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
予定時刻：03:00 から 03:06（6 秒）
発話 31 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

まず構文の挙動、次に編集ツールが必要とする情報を見ていきます。
-->

---
layout: default
class: syntax-overview body-center
clicks: 6
---

## 属性の優先順位と JSX の期待

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
  <div v-if="$clicks === 2"><span class="text-primary font-600">JavaScript expression</span><br />Astro の書き方って、JSX っぽいですよね。</div>
  <div v-if="$clicks === 3"><span class="text-primary font-600">Q. </span>この <code>title</code> は、どちらの値になる？</div>
  <div v-if="$clicks === 3" class="mt-4"><code>first</code> か、<code>second</code> か</div>
  <div v-if="$clicks === 4"><span class="text-primary font-600">A. </span><code>first</code></div>
  <Overlay v-if="$clicks >= 5" aria-label="Astro Template Syntax への問いと答え">
    <template #title>
      <span v-if="$clicks === 5">JSX なら second。なぜ first になった？</span>
      <span v-else>HTML の規則で扱ったため</span>
    </template>
    <p v-if="$clicks >= 6">
      Astro が同じ属性を二つ出力した。<br />
      ブラウザは HTML の規則で先の <code>title="first"</code> を採用した。
    </p>
    <template v-if="$clicks >= 6" #reference>
      <a href="https://html.spec.whatwg.org/multipage/parsing.html#attribute-name-state" target="_blank" rel="noopener noreferrer">HTML Standard：同じ名前の属性は後のものを取り除く</a>
    </template>
  </Overlay>
</div>

<Ref v-if="$clicks < 3" href="https://docs.astro.build/en/reference/astro-syntax/">Astro Template Syntax</Ref>
<Ref v-if="$clicks === 4" href="https://github.com/withastro/astro/issues/5558#issuecomment-1343799494">astro#5558 の説明</Ref>

<!--
予定時刻：03:06 から 04:16（70 秒）
発話 402 文字。時間は予定であり、実測ではない。
進行：6 回のクリックを発話に合わせる。

### 発話

[初期表示]
まず Astro の書き方です。三本線で囲まれた部分が Component script です。JavaScript と TypeScript を書けて、ビルド時やサーバーで実行します。
[クリック 1]
その下が Template です。HTML を基礎に、表示する内容を書きます。
[クリック 2]
波かっこの中で JavaScript expression を評価します。ここでは、名前と価格を表示しています。Astro の書き方って、JSX っぽいですよね。
[クリック 3]
li の title に first を指定して、その後に title が second の props を展開します。JSX のつもりなら second ですよね。Astro では、first だと思う人。second だと思う人。
[クリック 4]
2022 年の報告では、first になりました。
[クリック 5]
なぜ、後の指定が優先されなかったんでしょうか。
[クリック 6]
当時の Astro は、title 属性を二つ含む HTML を生成していました。ブラウザは重複した属性の先のものを採用します。

### 確認メモ（発表では話さない）

2022 年の報告を説明する。現在の Astro の挙動ではない。報告の class 属性を title に簡略化した例。HTML の重複属性と、JSX で後の指定を優先する props の合成を区別する。発話では JavaScript expression に統一する。Astro AST の expression node は波かっこを含む領域を指すため、その中の JavaScript expression と区別する。


### 出典と確認資料（発表では話さない）

- [astro#5558 の説明](https://github.com/withastro/astro/issues/5558#issuecomment-1343799494)
- [Astro Template Syntax](https://docs.astro.build/en/reference/astro-syntax/)
- [HTML Standard の attribute name state](https://html.spec.whatwg.org/multipage/parsing.html#attribute-name-state)
-->

---
layout: default
class: body-center
clicks: 2
---

## 改行は空白になるのか

```astro
<span>Astro</span>
<span>1200</span>
```

<!-- クイズと答えの表示領域を固定し、空白の説明は Overlay で表示する -->
<div class="mt-4 h-[96px] flex flex-col items-center justify-center text-center text-2xl">
  <div v-if="$clicks === 0"><span class="text-primary font-600">Q. </span>このコードは、どちらの表示になる？</div>
  <div v-if="$clicks === 0" class="mt-4"><code>Astro 1200</code> か、<code>Astro1200</code> か</div>
  <div v-if="$clicks === 1"><span class="text-primary font-600">A. </span><code>Astro 1200</code></div>
  <Overlay v-if="$clicks >= 2" aria-label="Astro Template Syntax の空白の扱い">
    <template #title>
      ブラウザが空白にする
    </template>
    <p>
      要素間の改行を HTML に保持した。<br />
      ブラウザがその改行を空白として表示し、<code>Astro 1200</code> になった。
    </p>
    <template #reference>
      <a href="https://github.com/withastro/astro/issues/6011" target="_blank" rel="noopener noreferrer">astro#6011: 要素間の空白テキスト node</a>
      <a href="https://blog.dwac.dev/posts/html-whitespace/" target="_blank" rel="noopener noreferrer" class="ml-8">HTML Whitespace is Broken</a>
    </template>
  </Overlay>
</div>

<!--
予定時刻：04:16 から 04:46（30 秒）
発話 101 文字。時間は予定であり、実測ではない。
進行：2 回のクリックを発話に合わせる。

### 発話

[初期表示]
二つの span を改行して並べます。JSX なら Astro1200 と続けて表示されますよね。
[クリック 1]
2023 年の報告では、空白が入りました。
[クリック 2]
Astro が改行を HTML に保持し、ブラウザが空白として表示していました。

### 確認メモ（発表では話さない）

2023 年の報告。既定の CSS の空白規則を前提とする。この空白の話は HTML correction と別の論点。関連ページで Astro v7 の設定の変更へ戻る。


### 出典と確認資料（発表では話さない）

- [astro#6011: 要素間の空白テキスト node](https://github.com/withastro/astro/issues/6011)
- [参照資料 2](https://blog.dwac.dev/posts/html-whitespace/)
-->

---
layout: default
class: table-comparison body-center code-example-compact
clicks: 3
---

## 表の外の h2 が移動した

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

<Overlay v-if="$clicks >= 2" aria-label="HTML の規則と Compiler の担当範囲">
  <template #title>
    <span v-if="$clicks === 2">HTML の規則による補正とは別の不具合</span>
    <span v-else>Compiler が HTML の補正まで担うべきか</span>
  </template>
  <div v-if="$clicks === 2">
    <p><code>expression</code> の後に、タグの親子関係を間違えた。</p>
    <p>Go Compiler は HTML5 Parser を拡張し、<br />ビルド時にもタグの補完と入れ子の補正を担っていた。</p>
  </div>
  <div v-else>
    <p>HTML に似た構文を採用することと、<br />ブラウザと同じ補正を行うことを分けて考える。</p>
    <p>属性と空白の規則は、別の論点として決める。</p>
  </div>
  <template #reference>
    <a href="https://github.com/withastro/compiler/issues/870" target="_blank" rel="noopener noreferrer">compiler#870 の不具合報告</a>
    <a href="https://html.spec.whatwg.org/multipage/parsing.html#tree-construction" target="_blank" rel="noopener noreferrer" class="ml-8">HTML Standard のパース規則</a>
  </template>
</Overlay>

</div>

<Ref v-if="$clicks < 2" href="https://github.com/withastro/compiler/issues/870">compiler#870</Ref>

<!--
予定時刻：04:46 から 05:36（50 秒）
発話 292 文字。時間は予定であり、実測ではない。
進行：3 回のクリックを発話に合わせる。

### 発話

[初期表示]
次は表の中に expression を含む例です。h2 は table の後に書いてあります。
[クリック 1]
ところが、生成した HTML では h2 が表の中に入っています。
[クリック 2]
これは、expression の後にタグの親子関係を間違えた不具合です。HTML の規則による補正ではありません。
Go Compiler は HTML5 Parser を拡張していて、ビルド時にもタグの補完と入れ子の補正を担っていました。
[クリック 3]
僕は、HTML に似た構文を採用することと、ブラウザと同じ補正を Compiler が行うことを、分けて考えたいんですね。属性と空白の規則とは別に、Compiler が HTML の補正まで担うべきか。この問いを後半で確認します。

### 確認メモ（発表では話さない）

compiler#870 と修正 PR #925。この例で h2 が table に入った直接の理由は、波かっこの領域の終了時にパースの状態を戻せなかった不具合。修正は resetInsertionMode() でパースの状態を選び直すもの。Compiler が生成した誤った HTML と、Browser がそれを補正して作る DOM は区別する。このスライドは前者を示す。

補足としてのみ紹介する。HTML Standard の Take a deep breath は、sarcasm という名前の終了タグについての一文。sarcasm は皮肉という意味で、文面はジョークとして理解できる。その後は他の終了タグと同じ規則に従う。表の不具合の原因を説明する文ではない。原文の画像と出典は images/html-spec/README.md を参照する。


### 出典と確認資料（発表では話さない）

- [JavaScript expression を含む表のパースを修正した PR #925](https://github.com/withastro/compiler/pull/925)
- [compiler#870](https://github.com/withastro/compiler/issues/870)
- [HTML Standard：Tree construction](https://html.spec.whatwg.org/multipage/parsing.html#tree-construction)
- [HTML Standard：The "in body" insertion mode](https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody)
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
  :subnotes="{ editor: 'Linter と LSP と Formatter' }"
/>

<!--
予定時刻：05:36 から 05:56（20 秒）
発話 130 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

ここからは編集ツールの話です。実行するコードが作れても、それだけでは書いている間のサポートはできません。
Linter と Formatter と Language Tool は、Go Compiler の結果を使っていました。それぞれ、どんな準備が必要だったかを見ていきます。
-->

---
layout: default
class: ch2-detail
clicks: 1
---

## Linter が検査を始めるまで

<div v-if="$clicks === 0">
<div class="ch2-cols">
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
</div>
<div class="ch2-summary">JavaScript expression の識別子と演算子が必要</div>
</div>
<div v-else>
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
<div class="ch2-summary">Espree でパースし、変数名と演算子を AST の項目として取得する</div>
</div>

<!--
予定時刻：05:56 から 06:46（50 秒）
発話 300 文字。時間は予定であり、実測ではない。
進行：1 回のクリックを発話に合わせる。

### 発話

[初期表示]
Linter で検査するには、変数名と演算子を node としてたどりたいんですね。ところが左の結果では、price と amount の掛け算は TextNode の文字列です。Astro のタグは分かっても、その中の JavaScript expression の AST はありません。
[クリック 1]
そこで、元の Astro を JavaScript と JSX に変換し、Espree でもう一度パースします。右のように Identifier と BinaryExpression が取得できます。ESTree は、この AST の形式を定める仕様です。
ここでようやく検査を始められます。ただ、変換したコードは元の Astro と位置が違うので、その対応も必要です。

### 確認メモ（発表では話さない）

ESTree は JavaScript の AST の形式を定める仕様。JavaScript 言語の仕様である ECMAScript と区別する。Go Compiler の Astro AST 全体が文字列という意味ではない。この JavaScript expression が TextNode.value の文字列であり、JavaScript の node を提供しない点を説明する。実装言語が Go であることの制約とは説明しない。
Compiler 2.12.2 の parse(source, { position: true }) の抜粋。Astro AST の expression node は子に Markup の node を含められるため、JavaScript expression 全体が常に一つの文字列という意味ではない。入力の行と末尾の LF は元の検証例に基づく。


### 出典と確認資料（発表では話さない）

- [Compiler 2.12.2 と AST](https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#parse-astro-and-return-an-ast)
- [ESTree の AST の定義](https://github.com/estree/estree/blob/master/es5.md)


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
予定時刻：06:46 から 07:11（25 秒）
発話 181 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

位置についても、二つの仕事がありました。上段は、生成したコードの位置を、元の Astro の位置に対応させる話です。
下段は、Compiler が返す位置情報そのものの不具合です。これは Linter の Adapter で修正していました。
変換後のコードを扱う仕事と、Compiler の不具合への対応は別なんですね。Linter が検査を始める前にも、こうした手間がありました。

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
class: ch2-detail ch2-formatter-failure
clicks: 2
---

## コードの再生成で、整形が止まった

<FormatterFailureExample :step="$clicks" />

<!--
予定時刻：07:11 から 07:51（40 秒）
発話 219 文字。時間は予定であり、実測ではない。
進行：2 回のクリックを発話に合わせる。

### 発話

[初期表示]
Formatter でも、Babel に渡すコードを作り直していました。この例の子には TextNode と p 要素と空の Fragment があります。TextNode.value はすでに文字列です。
[クリック 1]
プラグインはタグをコードの文字列に戻し、TextNode.value と連結します。そのとき空の Fragment が不正なタグになってしまいました。
[クリック 2]
Babel が構文エラーを返し、整形が止まります。元のコードは扱えていたのに、整形の準備で失敗したんですね。

### 確認メモ（発表では話さない）

prettier-plugin-astro の空の Fragment に関する報告を簡略化し、Compiler 2.12.2 と prettier-plugin-astro 0.14.1 と Prettier 3.6.2 で再現した。現在の実装の挙動を示すものではない。
入力は {true ? <p>OK</p> : <></>}。Compiler の transform() は成功し、parse() は空の fragment node を返す。条件演算子を含む JavaScript expression 全体は AST として返らない。
expression の子は TextNode.value の true ? 、p 要素の node、TextNode.value の : 、空の Fragment の node という順序。TextNode.value はすでに文字列で、serialize() はその値をそのまま使う。タグの node をコードの文字列に戻し、連結して expression 全体のコードにする。
プラグインの printRaw() は Astro AST の expression node の子を Compiler package の serialize() で文字列にする。serialize() の初期設定 selfClose は true で、子が空の fragment を < /> にする。文字列化の実装は Compiler package の JavaScript の補助機能である。Go Parser が Fragment を解析できなかったという説明はしない。
再生成された true ? <p>OK</p> : < /> を astroExpressionParser が JSX Fragment と波かっこで囲み、Babel に渡すと構文エラーになる。整形前の元の入力を Babel で解析できることも確認する。
以前の JSX で囲む理由は補足にする。オブジェクトリテラルを文と区別するために <>{expression}</> の形式を使い、閉じ波かっこの前の改行で行コメントとの混同を避ける。


### 出典と確認資料（発表では話さない）

- [空の Fragment を含む JavaScript expression の整形エラー](https://github.com/withastro/prettier-plugin-astro/issues/444)
- [JavaScript expression を文字列にするプラグインの実装](https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/printer/embed.ts)
- [Compiler の serialize()](https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/packages/compiler/src/node/utils.ts)
- ローカルの再現: validation/chapter2/formatter-fragment.mjs。
-->

---
layout: default
class: ch2-detail chapter-four ch2-formatter-requirements
---

## Formatter が担当する仕事に集中する

<div class="ch4-responsibilities">
  <section>
    <h3>Compiler から受け取る</h3>
    <ul class="ch4-list"><li>タグとコメントを含む AST</li><li>元のコードの正確な位置</li><li>AST を得るためのコード再生成を減らす</li></ul>
  </section>
  <section>
    <h3>Prettier で整形する</h3>
    <ul class="ch4-list"><li>AST を Prettier が扱う形に変換</li><li>Doc に文字と改行候補と字下げを記録</li><li>行幅に合わせて文字列を生成</li></ul>
  </section>
</div>

<Ref href="https://prettier.io/docs/plugins#the-printing-process">Prettier の整形工程</Ref>

<!--
予定時刻：07:51 から 08:16（25 秒）
発話 144 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

欲しかったのは、タグやコメント、元の位置も含むパース結果です。AST を得るためにコードを作り直す工程を減らしたいんですね。
その後、Prettier は AST から Doc を作ります。Doc は文字と改行候補と字下げの指示です。行幅に合わせて整形する仕事は、引き続き Formatter が担当します。

### 確認メモ（発表では話さない）

このページは第 2 章の要求を整理する。Rust Compiler が再パースをすべて廃止したという説明はしない。Astro の node を含む AST は、Prettier の AST とそのまま同じとは限らず、対応する Printer や変換が必要になる。
旧ページの group と softline と indent の詳説は本編では扱わない。group は改行を判断するまとまり、softline は 1 行なら空文字で改行時には改行、indent は字下げを表す。JavaScript expression を解析して AST を取得する工程と、AST から Doc を作る工程は区別する。
前の Fragment の例では、Astro AST に Fragment は保持されていた。必要なのは、タグの認識に加えて JavaScript expression 全体の AST を提供し、整形ツールが文字列の再生成と再解析を引き受ける範囲を減らすこと。


### 出典と確認資料（発表では話さない）

- [新 Compiler と Prettier plugin の検討](https://github.com/withastro/roadmap/discussions/1306)
- [Prettier の整形工程](https://prettier.io/docs/plugins#the-printing-process)
- [Doc の定義と命令](https://github.com/prettier/prettier/blob/main/commands.md)


### 確認メモ（発表では話さない）

prettier-plugin-astro 0.14.1 と Prettier 3.6.2 の例。Babel が解析し、Prettier の Printer が Doc を作る。再解析と整形指示への変換は別の工程。


### 出典と確認資料（発表では話さない）

- [Prettier の Parser と Printer](https://prettier.io/docs/plugins)
- [Prettier の整形方式](https://prettier.io/docs/technical-details)
- [prettier-plugin-astro 0.14.1 と JavaScript expression の整形](https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/printer/embed.ts)
-->

---
layout: default
class: ch2-detail ch2-language-overview
---

## Go Compiler と Language Tool の分担

<LanguageToolOverview />

<Ref><a href="https://code.visualstudio.com/api/language-extensions/language-server-extension-guide">LSP と Language Server</a> と <a href="https://volarjs.dev/core-concepts/embedded-languages/">Volar と位置対応</a> と <a href="https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/index.ts">従来の Astro の実装</a></Ref>

<!--
予定時刻：08:16 から 08:56（40 秒）
発話 251 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

これが Language Tool の全体像です。Go Compiler が TSX と Source map を返し、Astro の言語対応が HTML も作ります。Volar は、これらのコードと元の Astro の位置の対応を管理します。
HTML の属性補完は HTML Language Service、TSX の型の検査は TypeScript が担当します。結果を元の Astro の位置へ対応させ、エディタに返します。
既存の言語の機能を使えるのが、この設計の利点です。そのために、型の情報を保つコードと、正確な位置の対応が必要になります。

### 出典と確認資料（発表では話さない）

- [Biome を使う実装とテスト](https://github.com/withastro/compiler-rs/pull/34/files)
-->

---
layout: default
class: ch2-detail ch2-tsx-evolution
---

## TSX 変換で抱えていた課題

<div class="tsx-challenges">
  <section>
    <h3>型の情報を正しく渡す</h3>
    <p><code>as: Tag</code> を取り違え、使っている <code>Props</code> が未使用と診断された。</p>
  </section>
  <section>
    <h3>診断を元の位置へ戻す</h3>
    <p>CRLF で Source map の位置がずれ、診断を正しい場所へ戻せなかった。</p>
  </section>
  <section>
    <h3>書きかけのコードも扱う</h3>
    <p>独自の Scanner で JavaScript の構文を判別していた。<br />構文への対応に加え、入力途中の扱いも保守する必要があった。</p>
  </section>
</div>

<Ref><a href="https://github.com/withastro/compiler/issues/927">Props の事例</a> と <a href="https://github.com/withastro/compiler/issues/714">CRLF の事例</a> と <a href="https://github.com/withastro/compiler-rs/pull/34">TSX 変換の見直し</a></Ref>

<!--
予定時刻：08:56 から 09:31（35 秒）
発話 209 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

[初期表示]
Go Compiler の TSX 変換にも課題がありました。
as という prop を取り違え、使っている Props が未使用と診断される事例がありました。CRLF では、Source map が誤った位置を示しました。
JavaScript の構文は独自の Scanner で判別していたので、構文への対応や書きかけの入力を扱う負担もありました。
ビルドできるコードを作るだけでなく、型の情報と元の位置を保って、編集を支える必要があったんですね。

### 確認メモ（発表では話さない）

Props と CRLF は、従来の Go Compiler に報告された事例。現在も同じ不具合があるという説明はしない。
独自の Scanner による構文の判別は実装上の負担として扱う。すべての不完全なコードで TSX 生成が失敗したという説明はしない。


### 出典と確認資料（発表では話さない）

- [Props の不具合](https://github.com/withastro/compiler/issues/927)
- [CRLF の位置対応の不具合](https://github.com/withastro/compiler/issues/714)
- [TSX 変換の見直し](https://github.com/withastro/compiler-rs/pull/34)
-->

---
layout: default
class: ch2-detail chapter-four
---

## ツールの前準備を Compiler から見直す

<div class="ch4-responsibilities">
  <section>
    <h3>Compiler に求めること</h3>
    <ul class="ch4-list"><li>パース結果と正確な位置を提供する</li><li>TSX への変換でも情報を保つ</li></ul>
  </section>
  <section>
    <h3>ツールが担当すること</h3>
    <ul class="ch4-list"><li>規則に基づく検査と整形</li><li>型の診断と補完</li></ul>
  </section>
</div>
<p class="ch2-summary">独自実装の保守も含め、Compiler の設計を見直したい</p>

<Ref href="https://github.com/withastro/roadmap/issues/1356">Compiler の保守範囲を見直す公開提案</Ref>

<!--
予定時刻：09:31 から 10:00（29 秒）
発話 160 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

検査や整形の前に、コードを作り直したり、位置の不具合に対応したりしていました。僕は、この準備を Compiler から見直す必要があると思っています。
公開提案でも、Compiler を理解して修正できる人が少なく、保守が難しくなっていたと説明されています。機能を増やすとともに、改善を続けられる実装を考える段階だったんですね。

### 確認メモ（発表では話さない）

第 2 章では、ツールが必要とする情報、Compiler の情報不足と不具合、ツールが担当する変換を区別する。Virtual Code と位置対応と Doc の生成を、それ自体が Go Compiler の不具合であるとは説明しない。
未定義の参照の詳説は本編から省略し、補足にする。関連ページは再解析のためのコード生成の途中の不具合、関連ページは Compiler と Formatter の分担に改稿した。JSX で囲む理由と Doc の命令の詳説は確認メモに移した。LSP と Volar の分担は本編で説明する。
AST があればスコープ解析や型検査が不要という意味ではない。Compiler が生成したコードの位置対応は Compiler が、Adapter が独自に生成したコードの位置対応は Adapter が管理する。

保守の難しさと既存の基盤を利用する方針は、2026 年の公開提案に基づく。TSX 生成は同じ提案の対象外とされ、Language Tool の改善がすべて完了したとは説明しない。


### 出典と確認資料（発表では話さない）

- [新しい Compiler の提案と Prettier の AST に関する議論](https://github.com/withastro/roadmap/discussions/1306)
- [保守範囲と既存の基盤の利用を示した正式提案](https://github.com/withastro/roadmap/issues/1356)
-->

---
layout: section
---

# 3. 前提の変化
## Astro が再利用できる基盤はどう変わったのか

<!--
予定時刻：10:00 から 10:05（5 秒）
発話 27 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

その間に、再利用できる基盤はどう変わったのでしょうか。
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
    <p>JavaScript と TypeScript の<br />パースと変換</p>
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
予定時刻：10:05 から 10:40（35 秒）
発話 174 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

Rust で作られたフロントエンドのツールが増えました。ここで注目したいのは、ツールの中のライブラリを、自分たちの実装にも組み込めることです。
Parser や変換の機能を最初から作る代わりに、既存の実装を利用する選択肢が増えました。Go に Parser がないという話ではなく、Astro が再利用したい機能と、保守できる実装の組み合わせが変わったんですね。

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
class: ch3-detail chapter-three
---

## Oxc を既存の Parser として利用する

<div class="rebuild-oxc-example">

```js
import { parseSync } from "oxc-parser";

const { program } = parseSync(
  "example.js",
  "price * amount",
);
```

<p class="text-2xl mt-6">第 2 章で確認した変数名と演算子を取得できる。</p>
<p class="text-2xl mt-4">Astro Template Syntax への対応は、Astro が実装する。</p>
</div>

<Ref href="https://oxc.rs/docs/guide/usage/parser.html">Oxc Parser</Ref>

<!--
予定時刻：10:40 から 11:40（60 秒）
発話 346 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

先ほどの掛け算を、今度は Oxc の Parser に渡します。第 2 章で確認した変数名と演算子を、この呼び出しから取得できます。木の中身の説明は同じなので、ここでは呼び出す部分に注目してください。
この例は npm package から呼んでいます。Astro Compiler の内部では、Oxc の Rust crate を利用します。ここが、実装言語を選び直す理由につながります。欲しい機能を、自分たちの Compiler の中で利用できるんですね。
ただし、JavaScript が分かる Parser を入れるだけでは、Astro Template Syntax には対応できません。Astro のタグや Component script を扱う部分は、自分たちで実装して保守します。もう一つ、編集に必要な情報を保持する設計例を見ます。

### 確認メモ（発表では話さない）

ここは oxc-parser の JavaScript API の例。Astro Compiler の内部では Astro Template Syntax に対応させた Oxc の Rust crate を利用する。実装言語と、npm パッケージと、ネイティブコードや WASM という配布方法は別の判断。


### 出典と確認資料（発表では話さない）

- [Oxc Parser](https://oxc.rs/docs/guide/usage/parser.html)
- [参照資料 2](https://vite.dev/blog/announcing-vite8)
- [参照資料 3](https://napi.rs/docs/introduction/simple-package)
- [参照資料 4](https://napi.rs/blog/announce-v2)
-->

---
layout: default
class: ch3-detail chapter-three ch3-cst-comparison
---

## AST と Lossless CST が保持する情報

<FormattingInformation :stage="2" />

<!--
予定時刻：11:40 から 12:15（35 秒）
発話 206 文字。時間は予定であり、実測ではない。
進行：クリックなし。上のコードから、左と右の順に比較する。

### 発話

編集では、元のコードの情報をどこまで保持するかも大切です。同じコードで比べます。
左は Prettier と Babel の例です。変数名や演算子の AST とコメントを受け取り、空白の確認には元のコードも参照します。
右は Biome の Lossless CST です。構文に加えて、空白二文字、コメント、末尾の改行も木の中に保持します。
既存の設計と、これから参考にできる設計の比較です。Astro の採用予定を示すものではありません。

### 確認メモ（発表では話さない）

左の AST は BinaryExpression の抜粋。comments はコメントを取得できることを示す模式図で、Prettier と Babel のデータ全体ではない。AST が常にコメントを持たないという説明はしない。
右は Biome の Lossless CST の模式図。空白とコメントと改行は token に付随する情報として保持される。末尾の改行を含め、図は実際のダンプを簡略化している。
元の文字を保持する性質と、不完全なコードをパースするエラー回復は別の性質。
既存の設計と今後参考にできる設計を比較する。Astro Compiler が Biome や Lossless CST を採用する予定を示すものではない。

### 出典と確認資料（発表では話さない）

- [Prettier の整形工程](https://prettier.io/docs/plugins#the-printing-process)
- [Biome の Parser と CST](https://biomejs.dev/internals/architecture/#parser-and-cst)
-->

---
layout: default
class: ch3-detail chapter-three ch3-cst-example
---

## Biome の Lossless CST で書式を保つ

<FormattingInformation :stage="3" />

<Ref href="https://biomejs.dev/internals/architecture/#parser-and-cst">Biome の Parser と CST</Ref>

<style>
/* Keep this single-page example about a local edit, with room above the reference. */
:global(.ch3-cst-example .data-edit-caption) { display: none; }
:global(.ch3-cst-example .data-edit-intent) { margin-bottom: 12px; }
:global(.ch3-cst-example .data-takeaway) { margin-top: 16px; }
</style>

<!--
予定時刻：12:15 から 12:45（30 秒）
発話 178 文字。時間は予定であり、実測ではない。
進行：クリックなし。変更前と変更後を順に示す。

### 発話

では、この一か所の price を unitPrice に変えるとします。名前の部分を変更し、ほかの情報を引き継げば、空白二文字もコメントも末尾の改行も、そのままです。
AST と元のコードの位置を使っても実現できます。Lossless CST では、構文と元の文字を、一つの木で扱えるんですね。
必要な情報から基盤を選ぶ、という視点で、次は Astro の判断を見ていきます。

### 確認メモ（発表では話さない）

一か所の名前を変更する模式例。宣言と参照をまとめて改名するには、名前の参照関係を調べる機能も必要。
Lossless CST の文字の保持と、Parser のエラー回復は別の性質。Astro Compiler が Biome や Lossless CST を採用したという説明にはしない。
Biome の BatchMutation::replace_token は、元の token に付随する空白とコメントを新しい token に引き継ぐ。

### 出典と確認資料（発表では話さない）

- [Biome の Parser と CST](https://biomejs.dev/internals/architecture/#parser-and-cst)
- [biome_rowan の token の変更](https://github.com/biomejs/biome/blob/main/crates/biome_rowan/src/ast/batch.rs)

### 詳細な比較資料（発表では話さない）

本編では比較図と名前を変更する例を扱う。以下は以前の詳説の記録。

次は、元のコードの情報をどこまで持つかです。Biome は JavaScript の構文に加えて、空白とコメントも保持します。
整形に加えて、一部の文字だけを変更する編集支援でも、この情報が役立ちます。その一例が Lossless CST です。ここで紹介するのは Biome の設計で、Astro が導入したという説明ではありません。


### 確認メモ（発表では話さない）

上段は Go Compiler と Astro の Prettier plugin の課題の振り返り。下段は JavaScript を扱う Biome の設計例。入力言語と目的が異なるため、性能や対応範囲の直接比較にはしない。空の Fragment の再生成の不具合は、コードの再生成で整形が止まったページを参照する。
Biome は Rust で実装された別のツール。Prettier の内部に Biome があるという意味ではない。Astro が Biome や Lossless CST を採用したとは説明しない。Rust Compiler を基盤にした Astro の Prettier plugin は、第 4 章で説明する。


### 出典と確認資料（発表では話さない）

- [Prettier の整形工程](https://prettier.io/docs/plugins#the-printing-process)
- [Biome の設計資料](https://biomejs.dev/internals/architecture/)

同じコードを左右で比べます。Babel の AST には変数名と演算子があり、コメントも取得できます。空白を判断するときは、元のコードも参照します。
右の Biome の Lossless CST は、空白が二文字だったこと、コメント、末尾の改行まで、構文の木に保持します。名前や演算子に加えて、その周囲の文字も取得できるんですね。次の例では、その情報を使って名前だけを変えます。


### 確認メモ（発表では話さない）

図の AST は BinaryExpression の抜粋で、Prettier の全データを表さない。Prettier は言語とプラグインにより Parser が異なり、ここでは Babel の例を扱う。コメントを持つ AST もあり、コメントの保持だけで CST と分類しない。
Biome では空白とコメントなどを trivia として token に付随させる。token は名前や記号など、コードを分けた単位。CST が常に lossless とは限らない。元の文字を保持することと、不完全な入力からパースを続けるエラー回復は別の性質。


### 出典と確認資料（発表では話さない）

- [Prettier の整形工程](https://prettier.io/docs/plugins#the-printing-process)
- [Biome の Parser と CST](https://biomejs.dev/internals/architecture/#parser-and-cst)

一か所の price を unitPrice に変えたいとします。名前の部分を変更し、ほかの情報を引き継げば、空白二文字もコメントも末尾の改行もそのままです。
直したい場所だけを変え、ほかの書式を保つ。編集支援で、こういう情報を基盤から使えるのが嬉しいんですね。整形で空白を決め直す話とは分けて考えます。


### 確認メモ（発表では話さない）

一か所の token の変更を示す模式例。biome_rowan の BatchMutation::replace_token は replace_element を呼び、元の token の leading trivia と trailing trivia を新しい token に引き継ぐ。commit で反映する。宣言と参照をまとめて改名するには、名前の参照関係を調べる機能も必要。
元の書式を保つ修正は、AST と元のコードの範囲を使うツールでも実装できる。Lossless CST だけが可能にする機能とは説明しない。利点は、構文と元の文字を一つの木で保持し、編集 API で扱えること。


### 出典と確認資料（発表では話さない）

- [Biome の Parser と CST](https://biomejs.dev/internals/architecture/#parser-and-cst)
- [biome_rowan の token の変更](https://github.com/biomejs/biome/blob/main/crates/biome_rowan/src/ast/batch.rs)
-->

---
layout: section
---

# 4. 新しい判断
## Astro は何を実装し、何を基盤に任せるのか

<!--
予定時刻：12:45 から 12:50（5 秒）
発話 27 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

ここから、Compiler の新しい設計を見ていきます。
-->

---
layout: default
class: chapter-four ch4-compiler
---

## Astro が選んだ基盤と保守する実装

<div class="ch4-diagram ch4-compiler-diagram">
  <svg class="ch4-lines" viewBox="0 0 868 398" aria-hidden="true">
    <defs><marker id="ch4-compiler-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1,1 L9,5 L1,9" /></marker></defs>
    <path d="M175,68 V145" /><path d="M675,68 V145" />
    <path d="M350,191 H479" />
    <path d="M600,236 V269 H404 V301" /><path d="M745,236 V301" />
  </svg>
  <div class="ch4-node ch4-api"><strong>Astro の公開 API と Node-API bindings</strong><span>parse() と transform()</span></div>
  <div class="ch4-node ch4-parser"><strong>Oxc Parser と AST</strong><span>Astro Template Syntax への対応</span></div>
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
予定時刻：12:50 から 14:30（100 秒）
発話 461 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

この図では、既存の基盤を使う部分と、Astro が実装する部分を分けています。上の parse はパース結果を返す API、transform はビルドで実行するコードへ変換する API です。
パースには、Astro Template Syntax に対応させた Oxc を使います。JavaScript の Parser と AST を利用しながら、Astro の構文に対応させた部分は自分たちで保守します。
次に、実行するコードを作るのが中央の Astro Codegen です。TypeScript の変換と JavaScript の出力では、Oxc の Transformer と Codegen を利用します。Astro としてどんなコードを生成するかは、Astro の担当です。
CSS のパースと出力には Lightning CSS を使います。ただ、スタイルをどのコンポーネントに限定するかという規則は、Astro が実装します。
僕が大切だと思うのは、この保守範囲です。構文に対応するすべてを自分たちだけで実装するより、既存の機能を使いながら、Astro が決める部分に取り組めます。

### 確認メモ（発表では話さない）

parse() は AST と位置情報を返す。transform() は解析の後に Astro Codegen を呼ぶ。Oxc の Astro 拡張も保守範囲に含む。CSS のスコープ規則まで Lightning CSS に任せる説明はしない。実装言語、Node-API や WASM という配布方法、AST の設計は別の判断。


### 出典と確認資料（発表では話さない）

- [astro_napi](https://github.com/withastro/compiler-rs/blob/main/crates/astro_napi/src/lib.rs)
- [Astro Codegen](https://github.com/withastro/compiler-rs/tree/main/crates/astro_codegen/src/printer)
- [CSS scoping](https://github.com/withastro/compiler-rs/blob/main/crates/astro_codegen/src/css_scoping.rs)
- [Cargo.toml](https://github.com/withastro/compiler-rs/blob/main/Cargo.toml)
- [Compiler の実装と依存関係](https://github.com/withastro/compiler-rs/tree/main/crates)


### 確認メモ（発表では話さない）

このページは全体の案内に絞る。Go と Rust の比較、Astro Template Syntax の規則と空白の扱い、Compiler 内部の担当の順に説明する。


### 出典と確認資料（発表では話さない）

- [Astro の構文解析と AST](https://github.com/withastro/compiler-rs/blob/main/crates/astro_napi/src/lib.rs)
- [CSS の解析と生成](https://github.com/withastro/compiler-rs/blob/main/crates/astro_codegen/src/css_scoping.rs)
-->

---
layout: default
class: chapter-four ch4-comparison
clicks: 1
---

## Go と Rust のツールチェーン

<div class="ch4-state">
  <p>{{ $clicks === 0 ? 'Build 時の変換で HTML correction' : 'Compiler は HTML correction を行わない' }}</p>
</div>
<Overview
  compiler-frame
  :era="$clicks === 0 ? 'go' : 'rust'"
  :labels="{ build: 'Vite', compiler: $clicks === 0 ? 'Go Compiler' : 'Rust Compiler' }"
  :icons="{ compiler: $clicks === 0 ? 'go' : 'rust' }"
  :subnotes="{ build: '' }"
/>

<Ref href="https://github.com/withastro/roadmap/issues/1356">新 Compiler の方針と RFC #1356</Ref>

<!--
予定時刻：14:30 から 15:35（65 秒）
発話 315 文字。時間は予定であり、実測ではない。
進行：1 回のクリックを発話に合わせる。

### 発話

[初期表示]
では、第 2 章の問いに戻ります。Compiler が HTML の補正まで担うべきか、という話でした。Go Compiler では、HTML5 Parser に基づく補正をビルド時にも行っていました。
[クリック 1]
公開提案では、Rust Compiler は HTML correction を行わず、書かれた親子関係を保つ方針が示されています。出力された HTML から DOM を作るときには、引き続きブラウザが HTML の規則を適用します。
ここは、Compiler が何を変えるかの判断です。書いたタグの関係を保つことと、閉じ忘れたタグを許容することは別で、構文エラーの検査は必要です。
僕は、言語を Rust に変える機会に、ビルドで担う仕事そのものを見直した点に注目しています。

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

## Astro Template Syntax の規則と空白の扱い

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

<Ref><a href="https://github.com/withastro/compiler/blob/04170031ce2f30d1882fe480e87998197e0016aa/SYNTAX_SPEC.md">Astro Template Syntax の仕様ドラフト</a> と <a href="https://docs.astro.build/en/guides/upgrade-to/v7/#new-default-whitespace-handling-compresshtml-jsx">v7 の空白規則</a> と <a href="https://docs.astro.build/en/reference/configuration-reference/#compresshtml">compressHTML の設定</a></Ref>

<!--
予定時刻：15:35 から 16:35（60 秒）
発話 334 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

属性と空白の話も確認します。これらは HTML correction とは別に、Astro Template Syntax の規則として考える内容です。
2026 年 2 月の仕様ドラフトでは、構文の共通基準が文書化されています。Compiler とツールが同じ書き方を扱うために、参照できる規則があることも大切です。
空白については、Astro v7 で compressHTML の既定値が jsx になり、JSX の規則で扱います。前半の二つの span は Astro1200 と続けて表示されます。以前の扱いも設定で選べます。
Rust という言語だけで空白の扱いが決まるわけではありません。どの規則を採用するかは Astro の判断です。僕は、実装とともに、この規則も明確にすることが必要だったと考えています。

### 確認メモ（発表では話さない）

仕様は 2026 年 2 月 3 日付の Draft。Component Script と Component Template は以前からの呼称。構文の呼称がこの時点で初めて定義されたとは説明しない。
compressHTML は既存の設定。Astro v7 では既定値が true から 'jsx' に変更された。関連ページの二つの span を改行して並べる例では、'jsx' は Astro1200、従来の true は Astro 1200。既定の CSS の空白規則を前提とする。false は空白を保持する。
仕様ドラフトは位置情報の精度やエラー回復を保証しない。元の文字を保持する Lossless CST と、出力する HTML の空白をどう扱うかは別の判断。


### 出典と確認資料（発表では話さない）

- [Astro v7 の空白規則](https://docs.astro.build/en/guides/upgrade-to/v7/#new-default-whitespace-handling-compresshtml-jsx)
- [compressHTML の設定](https://docs.astro.build/en/reference/configuration-reference/#compresshtml)
- [Astro Template Syntax の仕様ドラフト](https://github.com/withastro/compiler/blob/04170031ce2f30d1882fe480e87998197e0016aa/SYNTAX_SPEC.md)
-->

---
layout: default
class: chapter-four ch4-tools
---

## パース結果を共有し、ツールが機能を作る

<div class="ch4-responsibilities">
  <section><h3>Rust Compiler の公開 API</h3><ul class="ch4-list"><li>parse() で AST と位置情報を返す</li><li>transform() でビルドのコードを作る</li></ul></section>
  <section><h3>受け取った後の担当</h3><ul class="ch4-list"><li>Linter は規則に基づいて検査する</li><li>Formatter は改行と字下げを決める</li><li>Language Tool の TSX 生成は別の要件</li></ul></section>
</div>

<Ref><a href="https://github.com/withastro/compiler-rs">Rust Compiler の公開 API</a> と <a href="https://github.com/withastro/roadmap/issues/1356">RFC の対象範囲</a></Ref>

<!--
予定時刻：16:35 から 17:45（70 秒）
発話 355 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

第 2 章では、ツールが検査や整形を始めるまでの準備が問題でした。新しい API からパース結果と位置情報を受け取れることで、その準備を変えられます。
ただ、何を警告するか、どこで改行するかまで Compiler が決めるわけではありません。規則の検査は Linter、整形は Formatter が担当します。ツールが期待するデータへの調整も必要です。
また、AST を返す API と、Language Tool が必要とする TSX の生成は別です。公開提案でも TSX の生成は対象外とされています。ここで、言語ツールの問題がすべて解消したとは言えません。
僕は今後、TSX の生成についても既存の基盤を使う設計が進むと期待しています。ただ、それは今の成果と分けて話したいところです。現在の再利用の具体例が、次の Prettier plugin です。

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
予定時刻：17:45 から 18:45（60 秒）
発話 372 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

Rust Compiler を使う Prettier plugin は公開されています。第 2 章では、文字列化の途中で Fragment が不正なタグになり、整形が止まる例を見ました。
新しいプラグインは Compiler の parse を呼び、受け取った AST を Prettier が扱う形に調整します。コメントの扱いなど、プラグインが担当する仕事もあります。その上で Prettier の機能を使って整形します。
Oxfmt でも、このプラグインと Rust Compiler を使う計画があります。資料を確認した 2026 年 10 月 1 日時点では、Astro 対応はまだ提供されていません。
僕は、自分たちの Compiler が別のツールからも利用されることに意味があると思っています。パースした情報の受け渡しを決めると、Compiler と Formatter が、それぞれの機能を改善できます。

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
layout: section
---

# MDX と Sätteri
## Rust と JavaScript の分担を、別の場所でも試した

<!--
予定時刻：18:45 から 18:50（5 秒）
発話 27 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

最後に、同じ分担の考え方を、僕が MDX で試した話です。
-->

---
layout: default
class: mdx-contribution-page
clicks: 1
---

## MDX の試作とライブラリへの貢献

<div v-if="$clicks === 0" class="mdx-contribution-map">
  <div class="mdx-contribution-trials">
    <section>
      <h3>Astro への提案</h3>
      <p>2025 年 7 月に Rust Compiler の統合を提案</p>
      <p>2025 年 8 月に AST Bridge を提案</p>
      <p class="mdx-contribution-detail">remark と rehype plugin の互換性が課題</p>
    </section>
    <section>
      <h3>MDX のコミュニティでの経験</h3>
      <p>Remco のサポートを受けて貢献</p>
      <p>不完全な import と export の編集支援を改善</p>
      <p class="mdx-contribution-detail">試作から、人との交流が続いた</p>
    </section>
  </div>

</div>

<div v-if="$clicks >= 1" class="mt-8 grid grid-cols-2 gap-8">
  <section>
    <h3 class="!text-2xl !mb-4">Remco の告知投稿</h3>
    <a href="https://bsky.app/profile/remcohaszing.nl/post/3mu5jnocvbk2r" target="_blank" rel="noopener noreferrer">
      <img src="./images/mdx/remco-mdx-release.png" alt="Remco による MDX の言語ツールのリリース告知" class="w-full" />
    </a>
    <p class="!text-xl !leading-7">MDX の言語ツールのリリースを告知。</p>
  </section>
  <section class="flex flex-col justify-center gap-5">
    <h3 class="!text-3xl !normal-case !my-0">Thanks, Remco!</h3>
    <p class="!text-2xl !leading-8 !my-0">親切に教えてくれて、<br />貢献をサポートしてくれました。</p>
    <a href="https://bsky.app/profile/remcohaszing.nl" class="text-xl underline">@remcohaszing.nl</a>
  </section>
</div>

<Ref><a href="https://github.com/withastro/astro/pull/14080">Compiler の統合提案</a> と <a href="https://github.com/withastro/astro/pull/14181">AST Bridge の提案</a></Ref>

<!--
予定時刻：18:50 から 19:50（60 秒）
発話 345 文字。時間は予定であり、実測ではない。
進行：1 回のクリックを発話に合わせる。

### 発話

[初期表示]
ここからは Astro Compiler とは別の試作です。僕は、Markdown と MDX にも高速な実装を使いたいと思い、2025 年 7 月に Rust の MDX Compiler の統合、8 月に AST Bridge を提案しました。既存の remark と rehype のプラグインとの互換性が課題でした。
採用の見通しは立ちませんでしたが、MDX のコミュニティとの交流は続きました。
[クリック 1]
Remco にサポートしてもらいながら、不完全な import と export で補完や診断が止まる問題を改善しました。親切に教えてくれた Remco に感謝しています。
冒頭の Astro Japan Community もそうですが、人と話し、助けてもらうことで、自分が取り組めることが増えました。僕にとって OSS の面白さは、こういう経験にもあります。

### 確認メモ（発表では話さない）

配布方法の補足。NAPI-RS は Rust の関数の公開と TypeScript の型定義を支援する。ネイティブコードでは OS と CPU ごとのビルドと検証が必要。僕の提案では、配布と保守の負担を減らすため wasm-bindgen を選んだ。

最初の統合提案は 2025 年 7 月 16 日、AST Bridge の提案は 2025 年 8 月 3 日（日本時間）。PR の作成日であり、試作を開始した日とは限らない。提案と試作を並行して進めた時期もある。
動機とボトルネックについてのやり取りは、本人がこの会話で共有した経験。相手と対象工程と計測範囲は未特定。一般的なベンチマーク事実や特定人物の発言として提示しない。6999 ページ、10 秒、半減などの数値は使わない。Astro の PR #14080 と PR #14181 は未マージで終了。拒否されたとは断定しない。AST Bridge と、xmdx の生成コードと付随情報を返す仕組みは別。


### 出典と確認資料（発表では話さない）

- [Remco Haszing の Bluesky](https://bsky.app/profile/remcohaszing.nl)
- [Astro PR #14080](https://github.com/withastro/astro/pull/14080)
- [PR #14181 での提案と助言](https://github.com/withastro/astro/pull/14181#issuecomment-3311059055)
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
予定時刻：19:50 から 20:55（65 秒）
発話 359 文字。時間は予定であり、実測ではない。
進行：2 回のクリックを発話に合わせる。

### 発話

[初期表示]
自作した xmdx は、Astro integration として導入します。これは Astro に機能を追加するプラグインです。Vite plugin を登録して、ビルド中に MDX を変換します。
[クリック 1]
変換には Rust の mdxjs-rs を使い、Node-API bindings で JavaScript から呼びます。Rust が変換を担当し、JavaScript が Astro に組み込みます。本文に加えて、frontmatter と見出し情報も返す必要がありました。
[クリック 2]
Starlight に組み込み、当時の公式ドキュメントで確認しました。僕が試した環境では、ビルド全体が半分以下になりました。
ただ、ベンチマークには苦労しました。変換だけの時間と、ビルド全体の時間は別です。速度に加え、どんな情報を返し、どんな条件で使えるかまで考える必要があったんですね。

### 確認メモ（発表では話さない）

ベンチマークの詳説は補足として保存する。
ただ、そこで悩んだのがベンチマークです。Vite のフックはファイルごとに動き、非同期の実行時間も重なります。フックの時間を合計しても、ビルド全体の時間にはならないんですね。
変換単体は、同じファイル群をビルドの外で直接変換して比べます。ファイルの取得と初期化は計測から分けます。
CPU プロファイルでは、負荷が集中する場所をサンプリングから推定します。変換全体の時間を測ることとは分けます。
ビルド全体は hyperfine で繰り返し測り、平均とばらつきを比べます。キャッシュとプラグイン、コードの色付けをそろえ、本文や見出しの結果も確かめます。
速い数字を示すだけでなく、何を含めた比較なのかを説明する。僕は、ここまで準備するのが難しかったんですね。

参照する試作は Astro 5 と Vite 6 と Rollup の組み合わせ。本番ビルドと開発時の依存関係の事前バンドルを混同しない。Rust の MDX コード生成には mdxjs-rs を利用。frontmatter と見出し情報は xmdx が取得する。実装の関数名は発話しない。

計測の難しさは発表者が練習で話した経験に基づく。変換単体と CPU プロファイルとビルド全体は、計測範囲を分けて説明する。Node.js の CPU プロファイルはサンプリングであり、関数の self time を合計して変換全体の正確な CPU 時間としない。Rust の内部を調べるには別の計測も必要になる。hyperfine では同じ機能と環境とキャッシュの条件をそろえ、繰り返した結果を比較する。計測手順の説明を、当時その手順をすべて実施したという主張に変えない。今回、新しいベンチマークは実行していない。


### 出典と確認資料（発表では話さない）

- [参照資料 1](https://github.com/jp-knj/xmdx/tree/7a89fdb17140e2b710e40d52d26338d978bc5c13)
- [Vite のプラグインの実行時間とプロファイル](https://vite.dev/guide/performance.html#audit-configured-vite-plugins)
- [Node.js の CPU プロファイルのサンプリング間隔](https://nodejs.org/api/cli.html#--cpu-prof-interval)
- [hyperfine の繰り返し計測とキャッシュの条件](https://github.com/sharkdp/hyperfine#usage)
-->

---
layout: default
class: body-center
---

## Astro と Content Processor の分担

<div class="grid grid-cols-2 gap-10 mt-10 text-2xl leading-relaxed">
  <section><h3>Astro</h3><p>Processor を選ぶ入口</p><p>Collections とビルドへの統合</p></section>
  <section><h3>Processor</h3><p>Markdown と MDX のパースと変換</p><p>plugin の実行</p></section>
</div>
<div class="mt-8 text-xl leading-relaxed"><p>remark と rehype plugin を使うなら unified</p><p>Sätteri への移行では plugin の API も確認する</p></div>

<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Astro の Markdown Processors</Ref>

<!--
予定時刻：20:55 から 21:20（25 秒）
発話 172 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

実際に導入するときは、Astro が Collections とビルドへの統合を担当し、Processor が Markdown と MDX の変換とプラグインの実行を担当します。
既存の remark と rehype を使うなら unified、Sätteri に移るならプラグインの API を確認します。高速化だけでなく、今のサイトの機能を続けられるかも判断の条件です。

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

<div class="satteri-growth-body">
  <div class="satteri-growth-context">計算負荷の高い部分は Rust。柔軟な plugin は JavaScript。</div>
  <img class="satteri-download-screenshot" src="./images/satteri-npmx-2026-10-02.jpg" alt="npmx の satteri の週ごとのダウンロード推移。2026 年 6 月以降に増加し、直近は週 400 万回を超えている。" />
</div>

<Ref><a href="https://npmx.dev/package-stats/satteri/v/0.10.5?end=2026-09-30&start=2025-10-02#trends">npmx のグラフ</a> と <a href="https://bsky.app/profile/erika.florist/post/3mj2tfwryw226">Erika の Sätteri 紹介</a></Ref>

<!--
予定時刻：21:20 から 21:45（25 秒）
発話 146 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

Erika の Sätteri も、計算負荷の高い部分を Rust に、柔軟なプラグインを JavaScript に分けています。僕の試作が採用されたという話ではありません。同じ課題に取り組む人と交流し、実装が進むのが嬉しかったんですね。
ここでも、言語の間で何を渡すかと、誰が何を保守するかを決めています。

### 確認メモ（発表では話さない）

Erika の紹介は 2026 年 4 月 9 日。npmx のグラフは 2026 年 10 月 2 日に撮影した。
発表者も関心を持っていた課題に、別の実装で取り組む人がいた嬉しさを話す。以前の xmdx の提案の採否と、Sätteri の開発を混同しない。


### 出典と確認資料（発表では話さない）

- [Erika の投稿と Sätteri](https://bsky.app/profile/erika.florist/post/3mj2tfwryw226)
-->

---
layout: statement
class: flex flex-col justify-center h-full intro-question
---

# Go で動いていたものを、<br />なぜ、Rust に書き直すのか？

<a class="intro-question-video" href="https://www.youtube.com/live/wZ3OZh9IP54?t=7644" target="_blank" rel="noreferrer" aria-label="Vue Amsterdam での Matt Kane の発表動画を開く">
  <figure class="intro-question-screenshot">
    <img src="./images/talks/vue-amsterdam-edited.png" alt="Vue Amsterdam の発表スライド。Rust とツールのロゴが並ぶ。" />
    <figcaption>Vue Amsterdam の発表動画</figcaption>
  </figure>
</a>

<!--
予定時刻：21:45 から 21:50（5 秒）
発話 42 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

では、最初の問いに戻ります。なぜ、動いていた Compiler を書き直すのでしょうか。

### 確認メモ（発表では話さない）

関連ページと同じ問い。
-->

---
layout: default
class: body-center
---

## 最初の問いへの答え

<div class="answer-recap-grid">
  <section>
    <h3>当時の判断</h3>
    <ul>
      <li>当時の要件に合った実装</li>
      <li>Go を選んでビルドを支えた</li>
    </ul>
  </section>
  <section>
    <h3>発見した問題</h3>
    <ul>
      <li>Source の親子関係と位置情報への要求</li>
      <li>HTML correction を担う範囲</li>
      <li>独自実装の保守コスト</li>
    </ul>
  </section>
  <section>
    <h3>前提の変化</h3>
    <ul>
      <li>再利用したい Rust の基盤</li>
      <li>再利用できる範囲の拡大</li>
      <li>Astro Template Syntax の整理</li>
    </ul>
  </section>
  <section>
    <h3>新しい判断</h3>
    <ul>
      <li>保持する情報と変換する段階の明確化</li>
      <li>保守範囲を絞る</li>
      <li>改善し続けられる設計へ</li>
    </ul>
  </section>
</div>

<!--
予定時刻：21:50 から 22:50（60 秒）
発話 312 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

当時の Go Compiler は、Astro のビルドを支えていました。使い続けるなかで分かったのは、実行するコードに加えて、編集を支える情報も必要だということです。HTML の補正をどこまで担うか、独自の実装をどう保守するかも、考え直す段階になりました。
その間に、再利用したい基盤が Rust にそろってきました。だから、実装言語の変更とともに、Compiler が渡す情報と、Astro が保守する範囲を見直せる。僕は、そこに今回の書き直しの意味があると思っています。
補章の MDX でも、言語の分担と既存のプラグインとの関係を考えました。技術だけでなく、その実装を作り、教え、改善してくれる人たちとの関係も、続けていきたいと思っています。

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
予定時刻：22:50 から 23:05（15 秒）
発話 50 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

基盤を再利用し、自分たちの実装範囲を絞り、保守し続けられる設計にするため。これが、僕なりの答えです。
-->

---
layout: center
class: text-center
---

## ありがとうございました

<div class="mt-8 text-xl ">Vue Fes 楽しんでね。</div>

<!--
予定時刻：23:05 から 23:35（30 秒）
発話 111 文字。時間は予定であり、実測ではない。
進行：クリックなし。発話後に次へ進む。

### 発話

Astro と MDX の開発で助けてくれた皆さん、そして、きっかけをくれた Vue Fes に感謝しています。受け取った知識や助けを、僕も次の人へ渡していきたいと思っています。
ありがとうございました。Vue Fes、楽しんでください。
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
