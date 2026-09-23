---
theme: ./theme-light
author: jp-knj
title: Astro と Rust で考えるフロントエンドツールチェーンの今
info: |
  動いていた Go Compiler を、Astro はなぜ Rust で書き直したのか。
  当時の判断と発見した問題と前提の変化と新しい判断の4章で、歴史を読み解く。
duration: 40min
mdc: true
transition: fade
colorSchema: light
themeConfig:
  primary: "#bc52ee"
layout: center-vertical
class: text-center
---

<div class="text-2xl text-black font-400">Astro Compiler</div>

<h1 class="!text-6xl !font-700 mt-4 leading-tight">
  動いていたものを、<br />なぜ書き直すのか
</h1>

<div class="text-xl text-black mt-8">
  Go と WASM から Rust へ、5年ぶんの前提の変化
</div>

<!--
こんにちは。今日は、動いていたものをなぜ書き直すのかを、Astro Compiler を題材に話します。2021年に Go と WASM で書かれた Compiler が、2026年に Rust で書き直されました。その判断の中身を、4つの章に分けて追いかけます。
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
      <li>Vue Fes 2025 が、コミュニティを始めるきっかけ</li>
    </ul>
  </div>
</div>

<Ref href="https://x.com/astrodotbuild/status/1982483654858441181">Astro 公式による Astro Japan Community の紹介</Ref>

<!--
自己紹介です。Astro のメンテナをしていて、Astro Japan Community の運営もしています。コミュニティを始めるきっかけは Vue Fes 2025 でした。あとで出てきますが、Markdown と MDX まわりで Astro 本体への提案もしています。
-->

---
layout: statement
class: flex flex-col justify-center h-full
---

# Go で動いていたものを、<br />なぜ、Rust に書き直すのか？

<!--
今日の問いは、動いていた Go Compiler を、Astro はなぜ Rust で書き直したのかです。速さに加えて、何が問題で、何が変わって、どう責務を分け直したのかを確認します。
-->

---
layout: default
class: body-center
---

## 話すこと

<div class="grid grid-cols-1 gap-4 mt-10">
  <div>
    <div class="text-3xl font-600 mt-1">1. 当時の判断</div>
    <div class="text-lg mt-2">なぜ最初に Go と WASM を選んだのか</div>
  </div>
  <div>
    <div class="text-3xl font-600 mt-1">2. 発見した問題</div>
    <div class="text-lg mt-2">使い続けるなかで何が見えたのか</div>
  </div>
  <div>
    <div class="text-3xl font-600 mt-1">3. 前提の変化</div>
    <div class="text-lg mt-2">2026年までに周囲はどう変わったのか</div>
  </div>
  <div>
    <div class="text-3xl font-600 mt-1">4. 新しい判断</div>
    <div class="text-lg mt-2">その結果、責務をどう分け直したのか</div>
  </div>
</div>

<!--
構成は4つです。当時の判断、発見した問題、前提の変化、新しい判断。この順で、判断の材料がどう入れ替わったのかを追います。
-->

---
layout: section
---

# 1. 当時の判断
## なぜ最初に Go と WASM を選んだのか

<!--
まず第1章。2021年に何を選んだのか、そしてそれはどういう条件下での選択だったのかを確認します。
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
これが出発点です。最初の Astro は、.astro を Svelte Compiler の fork で読んで、Snowpack が Build と配信を担い、Browser が表示する。この4つでした。ここに出ている Svelte Compiler と Snowpack は、このあと Go Compiler と Vite に入れ替わります。その入れ替えがこの章の話です。そしてこの図には、この講演で何度も戻ってきます。章が進むごとに、登場人物と矢印が増えていきます。
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
2021年は、Rome が Rust への書き直しを発表し、Parcel 2 と Next.js 12 が Rust 製 Compiler を採用した年です。同時に、Vite 2 は Go 製の esbuild を使い、Turborepo も Go でした。Rust の採用が進むなかでも、Go を選ぶことは珍しい判断ではありませんでした。
-->

---
layout: default
class: go-era-slide go-era-build
---

<div class="go-era-heading">
  <h2>Astro v1</h2>
  <span class="go-era-year">2022年</span>
</div>

<div class="go-era-summary">Build のための Compiler だった</div>

<Overview
  visible="source,compiler,build,browser"
  subs="html5-parser,esbuild-css"
  :labels="{ compiler: 'Go Compiler', build: 'Vite' }"
  :icons="{ compiler: 'go' }"
  :subnotes="{ build: 'esbuild' }"
/>

<div class="go-era-reason">
  <div class="text-2xl font-600 text-primary">深く考えすぎずに選んだ</div>
  <div class="text-xl mt-2">esbuild が Go だった。Go は学びやすかった。</div>
</div>

<Ref href="https://natemoo.re/posts/hello-from-the-other-side/">Nate Moore: Hello from the other side</Ref>

<!--
Astro v0.21 で、Svelte Compiler の fork から Go Compiler に移行し、Build は Vite が担うようになりました。この図は2022年の Astro v1 を示しています。JavaScript からは WASM を介して Compiler を呼び出します。Build を目的とした Compiler は、.astro を TypeScript を含むコードへ変換し、Astro の Vite plugin が esbuild を使って JavaScript に変換します。
Go を選んだ理由は、実装した Nate Moore 本人がこう書いています。esbuild が Go で書かれていたこと、Go が学びやすかったこと。深く考えすぎずに選んだ、と。
Go Compiler の中では、HTML5 Parser 由来の実装を Astro syntax 向けに拡張しています。CSS には、2022年3月に導入した esbuild 由来の CSS Parser と Printer を使い、CSS の解析とスコープ化を行います。Vite の部分に示した esbuild は TypeScript 変換用で、Compiler 内の CSS 用とは担当が異なります。HTML5 Parser をベースにしたことが、第2章の話につながります。

実装の出典: [esbuild の CSS Parser の導入](https://github.com/withastro/compiler/pull/329)、[Astro v1 の Vite plugin](https://github.com/withastro/astro/blob/astro%401.0.0/packages/astro/src/vite-plugin-astro/index.ts)、[Go Compiler と Vite を採用した Astro v0.21](https://astro.build/blog/astro-021-release/)。

次の章では、Compiler が Editor のツールでも使われるようになり、どのような問題が分かったのかを確認します。
-->

---
layout: section
---

# 2. 発見した問題
## 使い続けるなかで何が見えたのか

<!--
第2章です。Go と WASM の Compiler を使い続けるなかで、何が見えてきたのか。ここからは具体的なコードと AST を見ていきます。なお、これから出す AST の例は、説明に必要な部分だけを抜き出したものです。実際には位置情報などのフィールドが付きます。
-->

---
layout: default
class: go-era-slide go-era-tools
---

<div class="go-era-heading">
  <h2>Astro v2〜v5</h2>
  <span class="go-era-year">2023〜2025年</span>
</div>

<div class="go-era-summary">Editor のツールと Content の経路が増えた</div>

<Overview
  subs="html5-parser,esbuild-css"
  :labels="{ compiler: 'Go Compiler', build: 'Vite' }"
  :icons="{ compiler: 'go' }"
  :subnotes="{ build: 'esbuild' }"
/>

<!--
この図は、2023年から2025年の Astro v2〜v5 で利用していた経路をまとめたものです。Editor のツール、つまり ESLint や Language Server や Formatter も Go Compiler を利用していました。Compiler の中の HTML5 Parser と CSS 用の esbuild、Vite の部分の TypeScript 変換用の esbuild は、8枚目と同じ役割です。
時代の表記は、この章で扱う期間を示しています。Editor のツールや Markdown と MDX がすべて v2 で初めて登場したという意味ではありません。MDX は v1 ですでに利用でき、v2 では Content Collections が導入されました。Markdown と MDX は Content Processor から Build へ渡す別の経路です。
この章では、HTML の親子関係と埋め込まれた JavaScript を確認します。Content の経路は、第3章の後半で説明します。

出典: [Astro v1 の MDX 対応](https://astro.build/blog/astro-1/)、[Astro v2 の Content Collections](https://astro.build/blog/astro-2/)、[Astro v5 の TypeScript 変換](https://github.com/withastro/astro/blob/astro%405.0.0/packages/astro/src/vite-plugin-astro/compile.ts)。
-->

---
layout: default
class: syntax-overview body-center
clicks: 4
---

<h2>{{ $clicks >= 4 ? 'Astro syntax がおかしいのか？' : 'Astro syntax' }}</h2>

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
  <div v-if="$clicks === 0"><span class="text-primary font-600">Component script</span><br /><code>---</code> で囲む。Build 時とサーバーで実行する JavaScript と TypeScript</div>
  <div v-if="$clicks === 1"><span class="text-primary font-600">Template</span><br />HTML を基礎に、expression（JavaScript の式）や<br />コンポーネントを書ける</div>
  <div v-if="$clicks === 2"><span class="text-primary font-600">JavaScript expression</span><br />波かっこの中の式を評価し、結果をその場所に表示する</div>
  <div v-if="$clicks === 3"><span class="text-primary font-600">Q. </span>この <code>title</code> は、どちらの値になる？</div>
  <div v-if="$clicks === 3" class="mt-4"><code>first</code> か、<code>second</code> か</div>
  <Overlay v-if="$clicks >= 4" aria-label="属性の値の答え">
    <template #title>ブラウザのルールやからや！</template>
    <div><strong><code>first</code></strong> <span class="text-xl">2022年の報告に基づく例</span></div>
    <p>後から書いた <code>{...props}</code> が優先され、<code>second</code> になると予想した。</p>
    <p>当時の Astro は同名の属性を出力した。<br />Browser は先にある <code>title="first"</code> を採用した。</p>
    <template #reference>
      <a href="https://github.com/withastro/astro/issues/5558#issuecomment-1343799494" target="_blank" rel="noopener noreferrer">astro#5558 の説明</a>
    </template>
  </Overlay>
</div>

<Ref v-if="$clicks < 3" href="https://docs.astro.build/en/reference/astro-syntax/">Astro syntax</Ref>

<!--
Astro syntax をおさらいします。初めに三本線で囲まれた Component script を示します。1クリック目で Template、2クリック目で波かっこに埋め込んだ JavaScript expression を示します。
products.map(...) は、商品を表す配列 products から li 要素の一覧を作る式です。li の中にある product.name と product.price も式で、商品の名前と価格を参照します。波かっこの中の式を評価し、その結果をその場所に表示します。
3クリック目では同じ例に属性を加え、title がどちらの値になるかを問いかけます。4クリック目で報告者の期待と当時の結果を示します。報告の論点に絞った例です。HTML の重複属性では先の値を採用し、JSX での props 合成では後の指定を優先します。Astro syntax は HTML を基礎にした構文で、JSX に似ていても同じ規則とは限りません。この違いが利用者の期待との不一致になりました。
2022年の元の報告にある class 属性を、ここでは title に簡略化しています。現在の Astro の挙動を示す例ではありません。
-->

---
layout: default
class: body-center
clicks: 1
---

## Astro syntax がおかしいのか？

```astro
<span>Astro</span>
<span>1200</span>
```

<!-- 問いの表示領域を固定し、答えは Overlay で表示する -->
<div class="mt-4 h-[96px] flex items-center justify-center text-center text-2xl">
  <div v-if="$clicks === 0">この表示はどうなる？</div>
  <Overlay v-if="$clicks >= 1" aria-label="改行の表示の答え">
    <template #title>ブラウザのルールやからや！</template>
    <div>期待した表示：<code>Astro1200</code><br />実際の表示：<code>Astro 1200</code></div>
    <p>Astro が保持した要素間の改行を、ブラウザが空白として表示する。</p>
  </Overlay>
</div>

<Ref>
  <a href="https://github.com/withastro/astro/issues/6011">astro#6011: 要素間の空白テキスト node</a>
  <a v-if="$clicks >= 1" href="https://blog.dwac.dev/posts/html-whitespace/" class="ml-8">HTML Whitespace is Broken</a>
</Ref>

<!--
2023年の報告です。要素を改行して並べると、要素間に空白だけのテキスト node ができます。Astro は .astro の改行を出力にも保持します。Browser の空白の扱いが表示に影響するため、JSX での表示と比べると違いがあります。次は、Compiler の HTML Parser を確認します。
-->

---
layout: default
class: table-comparison body-center code-example-compact
clicks: 2
---

## Astro syntax がおかしいのか？

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

<Overlay v-if="$clicks >= 2" aria-label="生成された HTML の問題">
  <template #title>それは Compiler の不具合や！</template>
  <p>Compiler の変換で、<b>表の後の見出しが表の中に入った</b>。</p>
  <p>ブラウザの HTML の規則ではなく、Compiler が生成する HTML の問題。</p>
</Overlay>

</div>

<Ref href="https://github.com/withastro/compiler/issues/870">compiler#870</Ref>

<!--
最初は書いた Astro を確認します。1回目のクリックで、報告された生成 HTML を右に表示します。2回目で問題を整理します。
compiler#870 の報告当時、Build で使うコードへの変換で table の後の h2 が table の中に入る不具合がありました。この結果を HTML 仕様どおりとは説明しません。Compiler が生成する HTML と、Browser がその HTML から作る DOM は区別します。
DOM は、Browser が表示のために作る HTML の木です。HTML5 の補正は、HTML の規則に従って要素の移動や追加を行うことです。補正後の親子関係だけを見ても、書かれた入れ子は分かりません。たとえば p の中に div を書くと、div の開始で p が閉じられます。補正後の木からは、元の入れ子を診断できません。
ここまでの例から、Astro syntax に必要な規則を振り返ります。
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
    <h3>HTML5 Parser 固有のふるまい</h3>
    <ul><li>タグの補完や入れ子の補正まで、Astro で採用する必要があるか</li></ul>
  </div>
</div>
<div class="ch2-next-question">HTML5 Parser は必要なのか？</div>

<!--
11枚目の属性と12枚目の空白と13枚目の不具合を振り返ります。HTML に似た構文を解析することと、Browser と同じ HTML correction を採用することは別の判断です。
改行を含む空白の表示は、HTML correction とは別の論点です。Astro syntax でどの規則を採用するかという問いであり、空白の仕様が変更済みだという説明ではありません。
table の後の h2 が table の中に入った例は、Compiler の不具合です。HTML5 の正しい挙動として説明しません。Rust への移行だけで、これらの課題をすべて解決できるという説明もしません。
次は、Go Compiler の情報をツールがどう利用していたかを確認します。
-->

---
layout: default
class: ch2-detail
---

## `parse()` と `convertToTSX()` を使うツールの役割

<div class="ch2-api-map" aria-label="Go Compiler の API からツールへの分岐">
  <div class="ch2-api-node ch2-api-parse"><strong><code>parse()</code></strong><span>Astro AST と位置情報</span></div>
  <svg class="ch2-api-fork" viewBox="0 0 60 220" preserveAspectRatio="none" aria-hidden="true"><path d="M0 110 H25 V55 H55 M25 110 V165 H55 M47 50 L55 55 L47 60 M47 160 L55 165 L47 170" /></svg>
  <div class="ch2-api-consumer"><strong>Linter</strong><span>expression を再解析し、宣言と参照を検査する</span></div>
  <div class="ch2-api-consumer"><strong>Formatter</strong><span>expression を再解析し、空白と改行を整える</span></div>
  <div class="ch2-api-node"><strong><code>convertToTSX()</code></strong><span>Virtual TSX と Source map</span></div>
  <svg class="ch2-api-arrow" viewBox="0 0 60 110" preserveAspectRatio="none" aria-hidden="true"><path d="M0 55 H55 M47 50 L55 55 L47 60" /></svg>
  <div class="ch2-api-consumer"><strong>Language Tool の型解析</strong><span>TypeScript の補完と診断を<br />.astro へ対応させる</span></div>
</div>

<Ref href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/cmd/astro-wasm/astro-wasm.go#L251-L284">Go Compiler の parse() と convertToTSX()</Ref>

<!--
architecture/docs/drafts/astro-go-compiler-internals-and-consumers.md の API と用途の対応表を参照しています。資料は Compiler 3.0.0、続く実測例は Compiler 2.12.2です。
parse は Astro AST と位置情報を返し、astro-eslint-parser と prettier-plugin-astro が利用します。Linter は宣言と参照を検査し、Formatter は空白と改行を決めます。expression の再解析については後の具体例で確認します。
convertToTSX は TypeScript が解析できるコードと Source map を返します。この図の Language Tool は型解析の経路です。HTML 属性の補完は別に Virtual HTML を使います。
Go Compiler の二つの解析モードも区別します。Tokenizer と Parser の実装は共通です。transform() は Literal mode を指定せず、parse() と convertToTSX() は ParseOptionEnableLiteral(true) を指定します。Literal mode は HTML correction を抑え、書かれた入れ子を保持します。API は個別に Parser を呼び、返す形式を選びます。一度の解析結果を三つの API で共有する図ではありません。
transform() は Build で使う実行コードを生成します。parse() と convertToTSX() は Editor でも使われます。この違いは2.12.2と、資料の3.0.0の固定コミット 8870738a46baf6e639b1fab61e9e443b5e5df8f0 で確認しています。
-->

---
layout: default
class: ch2-detail ch2-nesting-slide
clicks: 3
---

## expression の AST と正確な位置を<br />ツールへ提供できていたか？

<div class="ch2-nesting-cols">
<div class="ch2-source-regions" aria-label="Astro の言語領域">
<pre><span class="ch2-region-script">---
const products =
  await getProducts();
&#45;&#45;&#45;</span>
<span class="ch2-region-template">&lt;ul&gt;</span>
<span :class="{ 'ch2-region-expression': $clicks >= 1 }">  {products.map((product) =&gt; (</span>
<span :class="{ 'ch2-region-markup': $clicks >= 2 }">    &lt;li&gt;<span :class="{ 'ch2-region-inner': $clicks >= 3 }">{product.name}</span>&lt;/li&gt;</span>
<span :class="{ 'ch2-region-expression': $clicks >= 1 }">  ))}</span>
<span class="ch2-region-template">&lt;/ul&gt;</span></pre>
</div>
<div class="ch2-tree" aria-label="Component script と Template は同じ階層">
  <div class="ch2-tree-root flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro</div>
  <div class="ch2-tree-children">
    <div class="ch2-tree-node ch2-region-script">Component script</div>
    <div class="ch2-tree-node"><span class="ch2-region-template">Template</span>
      <div class="ch2-tree-children">
        <div class="ch2-tree-node" :class="{ 'ch2-region-expression': $clicks >= 1 }">JavaScript expression
          <div class="ch2-tree-children">
            <div class="ch2-tree-node" :class="{ 'ch2-region-markup': $clicks >= 2 }">Markup
              <div class="ch2-tree-children">
                <div class="ch2-tree-node" :class="{ 'ch2-region-inner': $clicks >= 3 }">JavaScript expression</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</div>
<div class="ch2-note">Astro syntax には、expression の中の Markup と、Markup の中の expression がある</div>

<!--
左は11枚目の products.map を簡略化した例です。Component script と Template は同じ階層です。Template の expression に Markup があり、その Markup に再び expression があります。
三回のクリックで Template 直下の expression、li の Markup、product.name の expression を順に強調します。コードと図の色が対応します。
右は .astro に含まれる言語領域の図であり、Go Compiler が返す AST の node 名を示す図ではありません。Go Compiler は Astro AST を返し、expression の子に element を含めることができ、Markup の入れ子を保持します。AST には、JavaScript expression の変数名と演算子を表す AST node がありません。次の例で AST を確認します。
-->

---
layout: default
class: ch2-detail
---

## Compiler が返す expression

<div class="ch2-cols">
<div>
<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro</div>

```astro
---
const price = 10;
const amount = 3;
---

<p>{price * amount}</p>
```

</div>
<div>
<div class="ch2-label">Go Compiler の AST</div>

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
<div class="ch2-summary">変数名と演算子を、個別の AST node としてたどれない</div>

<Ref href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#parse-astro-and-return-an-ast">Compiler 2.12.2 と AST</Ref>

<!--
左のコードは5行目に空行があり、末尾は LF です。price と amount はともに宣言されています。
右は parse(source, { position: true }) の返却値から、expression とその子を抜粋したものです。Astro AST は expression の範囲を表し、TextNode.value に price * amount という文字列を持ちます。変数名を表す Identifier や、掛け算を表す BinaryExpression は、この AST にはありません。
この枚では、expression の中身が文字列であることだけを伝えます。Compiler 2.12.2で検証しています。
-->

---
layout: default
class: ch2-detail
clicks: 2
---

## コードから変数名と演算子を取得する

<div class="ch2-cols ch2-expression-cols">
<div>
<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro</div>

```astro
---
const price = 10;
const amount = 3;
---

<p>{price * amount}</p>
```

</div>
<div v-click="1" class="ch2-expression-stages">
<div v-if="$clicks < 2">
<div class="ch2-label">Linter 独自の Virtual TSX</div>

```tsx
const price = 10;
const amount = 3;
<>
  <p>{price * amount}</p>
</>;
```

<div class="ch2-note">Espree で JavaScript として解析する</div>
</div>
<div v-else>
<div class="ch2-label">Espree で解析した AST</div>
<div class="ch2-expression-ast" role="img" aria-label="price * amount 全体は BinaryExpression。operator は掛け算の*。left は price の Identifier、right は amount の Identifier。">
  <div class="ch2-expression-root">
    <strong><code>BinaryExpression</code></strong>
    <div><code>price * amount</code> 全体</div>
    <div>二つの値の間に演算子がある expression</div>
    <div class="ch2-expression-operator"><code>operator: "*"</code> 掛け算</div>
  </div>
  <svg class="ch2-expression-branches" viewBox="0 0 400 36" preserveAspectRatio="none" aria-hidden="true"><path d="M200 0 V16 M100 36 V16 H300 V36" /></svg>
  <div class="ch2-expression-operands">
    <div><div class="ch2-label"><code>left</code></div><strong><code>Identifier</code></strong><div><code>name: "price"</code></div><div>左辺の変数名</div></div>
    <div><div class="ch2-label"><code>right</code></div><strong><code>Identifier</code></strong><div><code>name: "amount"</code></div><div>右辺の変数名</div></div>
  </div>
</div>
</div>
</div>
</div>
<div v-if="$clicks < 2" class="ch2-summary"><code>astro-eslint-parser</code> が JavaScript Parser へ渡すコードを作る</div>
<div v-else class="ch2-summary">変数名と演算子を AST の項目として取得できる</div>

<!--
Go Compiler の AST では、price * amount の中身は文字列でした。変数名や演算子を個別に扱うには、JavaScript として解析する必要があります。

クリック1で Virtual TSX を表示します。astro-eslint-parser が、右の Virtual TSX を作ります。これは JavaScript Parser へ渡すためのコードです。この例では、Espree という Parser で解析します。

クリック2で右列を AST 図へ切り替えます。price * amount 全体が BinaryExpression になっています。二つの値の間に演算子がある expression を表す node です。
その operator が掛け算の*です。left には price、right には amount を表す Identifier があります。Identifier は、ここでは参照している変数名を表します。
これでツールは、変数名と演算子を AST の項目として取得できます。

補足。Compiler の convertToTSX() とは別の変換です。この例は JavaScript と JSX だけで表せるため、検証では Espree を使います。Component script の区切りを外し、Template を Fragment で囲みます。実装は区切りを除いた位置にセミコロンを挿入するなどの調整も行います。スライドに掲載した抜粋では、そのセミコロンと一部の空行を省き、Fragment 内を字下げしています。図は expression の部分を抜粋し、位置などの項目を省略しています。

参照: [astro-eslint-parser 1.2.2と processTemplate](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/process-template.ts)
-->

---
layout: default
class: ch2-detail code-example-dense ch2-position-slide
---

## 不正確な位置を返した理由

<div class="ch2-label">expression の位置にも HTML タグ用の計算を適用していた</div>
<pre class="ch2-ruler">十の位  44444555555555566666666
一の位  56789012345678901234567
文字    &lt;p&gt;{price * amount}&lt;/p&gt;</pre>

<div class="ch2-ranges leading-[28px]">
  <div class="!grid-cols-[245px_245px_1fr]"><span class="ch2-label">Compiler が返す位置</span><code class="!text-[20px]">start: 47, end: 80</code><span>内部名の長さも終端に加算</span></div>
  <div class="!grid-cols-[245px_245px_1fr]"><span class="ch2-label">補正後の expression</span><code class="!text-[20px]">[48, 64)</code><span><code>{price * amount}</code></span></div>
  <div class="!grid-cols-[245px_245px_1fr]"><span class="ch2-label">.astro での変数名</span><code class="!text-[20px]">[49, 54)</code><span><code>price</code> の5文字</span></div>
</div>
<div class="ch2-summary">1. <code>fixLocations</code> で Astro expression の範囲を補正する<br />2. <code>restore</code> で Virtual TSX の AST の位置を .astro へ戻す</div>
<div class="ch2-note">Range は0始まりで終端を含まない</div>

<Ref href="https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/astro-parser/parse.ts">astro-eslint-parser 1.2.2 と fixLocations</Ref>

<!--
前の枚では、変数名と演算子を AST として取得する流れを示しました。Editor で名前に下線を引くには、.astro の何文字目なのかも必要です。ここでは、その流れに含まれる二つの位置調整を確認します。

一つ目は、Astro expression の範囲の補正です。Compiler 2.12.2 の内部では expression も ElementNode で表します。AST の位置情報を作る positionAt は、expression にも HTML タグ用の計算を適用していました。
開始位置は 48 - 1 = 47、終端位置は 63 + 16 + 1 = 80 になります。16 は内部の n.Data に入る文字列 astro:expression の文字数です。HTML タグ名の長さを使う計算に、この内部名の長さが使われています。
この不具合は Virtual TSX の作成前に、Compiler が Astro AST を返す時点で発生します。astro-eslint-parser の fixLocations は .astro の波かっこを確認します。開始の波かっこは48、閉じ波かっこは63にあるので、終端を含まない範囲 [48, 64) に補正します。

二つ目は、Virtual TSX で解析した AST の位置を、.astro の位置へ戻す工程です。これは Compiler が返す範囲の補正とは別です。前の枚の右に示したコードは変換後のコードなので、その位置をそのまま Editor へ渡せません。restore で .astro へ対応させると、掛け算に使われている price は [49, 54) の範囲になります。JavaScript の識別子を解析するのは JavaScript Parser です。次の枚では、誤記した変数名への診断を示します。

補足。定規は6行目の文字オフセットで、前のコードの空行と末尾の LF を含めて数えた値です。Compiler の README も、一部の位置が不正確であることを明記しています。
この例は ASCII なので、UTF-8 の byte と UTF-16 の文字オフセットの値が一致します。一般の日本語を含む入力で両者が一致するとは限りません。ESLint の行と列は1始まりで、price は6行目の5列目から10列目に相当します。終端は含みません。

参照: [Compiler 2.12.2 の positionAt](https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/internal/printer/print-to-json.go#L134-L175)
参照: [astro-eslint-parser 1.2.2 と fixLocations](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/astro-parser/parse.ts)
-->

---
layout: default
class: ch2-detail code-example-dense
---

## ESLint が未定義の参照を検査する

<div class="ch2-cols ch2-scope">
<div>
<div class="ch2-label">ここで変数名を誤記する</div>

```astro
---
const price = 10;
const amount = 3;
---

<p>{pirce * amount}</p>
<!-- pirceは診断を示すための誤記 -->
```

</div>
<div>
<div class="ch2-label">宣言と参照を照合する</div>
<div class="ch2-lint-matches"><div><code>price</code><span>宣言あり</span></div><div><code>amount</code><span>参照先の宣言あり</span></div><div><code>pirce</code><span>参照先の宣言なし</span></div></div>
<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro への診断</div>
<pre class="ch2-lint-diagnostic">&lt;p&gt;{<span>pirce</span> * amount}&lt;/p&gt;</pre>
<div class="ch2-note"><code>no-undef</code><br /><code>'pirce' is not defined.</code></div>
</div>
</div>
<div class="ch2-summary">未定義の参照を検出し、元の5文字に波線を表示する</div>

<Ref href="https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/index.ts">parseForESLint と位置の復元</Ref>

<!--
この枚で初めて pirce という誤記を示します。Parser が用意したスコープ情報では、price と amount には宣言があります。amount の参照はその宣言に対応します。pirce の参照には対応する宣言がなく、globalScope.through に含まれます。
parseForESLint は、Virtual TSX を解析して AST とスコープ情報を用意した後、restore で AST の位置を .astro へ戻します。Astro 固有の node や visitorKeys も整えた返却値を ESLint へ渡します。ESLint の no-undef は、このスコープ情報から未定義の参照を検査します。意図した綴りを推測して修正するルールではありません。
診断 JSON の抜粋は { "ruleId": "no-undef", "message": "'pirce' is not defined.", "line": 6, "column": 5, "endLine": 6, "endColumn": 10 } です。ESLint 9.36.0で確認した値で、Range では[49, 54)です。波線はこの範囲を示した図です。
-->

---
layout: default
class: ch2-detail code-example-compact
clicks: 2
---

## Formatter が expression を解析する

<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />整形前の .astro</div>

```astro
<ul>
{products.map(product=><li>
{product.name}:{product.price}</li>)}
</ul>
```

<div v-if="$clicks === 1" class="ch2-format-stage">
<div class="ch2-label">1. Astro AST と .astro から抽出した expression</div>

```jsx
products.map(product=><li>
{product.name}:{product.price}</li>)
```

</div>
<div v-if="$clicks >= 2" class="ch2-format-stage">
<div class="ch2-label">2. JSX で囲んだ Babel 入力</div>

```jsx
<>{products.map(product=><li>
{product.name}:{product.price}</li>)
}</>
```

</div>
<div class="ch2-bottom-note"><code>parse()</code> で .astro 全体を、<code>babel-ts</code> で expression の中身を解析する</div>

<Ref href="https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/index.ts">prettier-plugin-astro 0.14.1と astroExpressionParser</Ref>

<!--
ここからは Formatter による整形の例です。変数名の誤記はなく、products.map の空白と改行をそろえたい場面です。
クリック1で Astro AST と .astro から取り出した expression を示します。クリック2では同じ expression を JSX Fragment と波かっこで囲んだ Babel 入力に切り替えます。astroExpressionParser.preprocess は、この末尾の改行を含むコードを作ります。babel-ts を基にした Parser が解析し、Fragment 内部の expression の AST を返します。
この入力と整形結果は prettier-plugin-astro 0.14.1と Prettier 3.6.2で確認しています。整形設定は printWidth 80、tabWidth 2、endOfLine lf です。
-->

---
layout: default
class: ch2-detail code-example-dense ch2-doc-slide
---

## Doc から整形後の .astro を作る

<div class="ch2-cols ch2-doc">
<div>
<div class="ch2-label">Astro Printer の Doc</div>

```js
 group([
   "{",
   indent([
     softline,
     expressionDoc
   ]),
   softline,
   "}"
 ])
```

<div class="ch2-note"><code>group</code> は改行する範囲<br /><code>softline</code> は改行候補<br /><code>indent</code> は字下げ</div>
</div>
<div>
<div class="ch2-label">Prettier による実際の整形結果</div>

```astro
<ul>
  {
    products.map((product) => (
      <li>
        {product.name}:{product.price}
      </li>
    ))
  }
</ul>
```

<div class="ch2-note">行幅80、インデント2、LF<br />二つの expression の間に空白は追加しない</div>
</div>
</div>

<Ref href="https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/printer/embed.ts">Astro Printer と Doc</Ref>

<!--
Doc は、文字列と改行候補と字下げの指示を組み合わせたデータです。Astro Printer は、Babel が解析した expression の整形の指示を表す Doc を受け取り、Astro の波かっこやタグの Doc と組み合わせます。左は expression を囲む Doc の抜粋で、実装の lineSuffixBoundary を省いています。expressionDoc はこの説明で使う名前です。
group は、まとまりを1行で表示するか改行するかを選ぶ単位です。softline は1行に収まれば空文字、改行を選べば改行になります。indent は改行後の字下げを表します。Prettier がこれらを行幅などの設定に従って文字列にします。
右は前の入力の実出力です。product.name と product.price の間にはコロンだけがあり、空白を追加しません。
-->

---
layout: default
class: ch2-detail code-example-dense
clicks: 2
---

## 補完と型検査のために Virtual Code を作る

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
<div v-if="$clicks === 1">
<div class="ch2-label">Virtual HTML</div>

```html
<a href="/products">
  {product.nmae}
</a>
```

<div class="ch2-note">HTML Language Service<br />属性補完: <code>target</code> と <code>title</code></div>
<div class="ch2-result">Component script を空白化し、<br />文字オフセットを保持する</div>
</div>
<div v-if="$clicks >= 2">
<div class="ch2-label"><code>convertToTSX()</code> の出力</div>

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

<div class="ch2-note">TypeScript が型を検査する Virtual TSX<br />TypeScript: <code>nmae</code> は型にない</div>
</div>
</div>
</div>

<Ref href="https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/index.ts">language-tools b4bcb4f と AstroVirtualCode</Ref>

<!--
Language Tool は、Editor に補完や診断を提供します。この例では product.name を宣言し、Template で product.nmae と誤記しています。
クリック1で Virtual HTML を示します。Component script を区切りごと同じ長さの空白へ変えます。抜粋では先頭の空白を省いています。HTML Language Service は、a タグの href 属性の直前で target や title を補完候補として返します。
空白化は改行も変えるため、保持するのは UTF-16 の文字オフセットです。.astro と Virtual HTML の行番号が一致する、という意味ではありません。
クリック2で表示を切り替え、Compiler の convertToTSX が作る Virtual TSX の抜粋を示します。Component script の宣言も同じ TSX に含まれます。抜粋では先頭の pragma と一部の空行と末尾の関数を省いています。TypeScript は product の型を調べ、nmae というプロパティがないことを診断します。次の枚で診断位置を確認します。
参照実装は language-tools b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05 です。HTML の前変換は packages/language-server/src/core/parseHTML.ts、TSX と位置対応は同じディレクトリの astro2tsx.ts にあります。
-->

---
layout: default
class: ch2-detail
---

## TypeScript の診断位置を戻す

<div class="ch2-cols">
<div>
<div class="ch2-label">Virtual TSX</div>

```tsx
  {product.nmae}
```

<div class="ch2-range-value">[129, 133)</div>
<div class="ch2-note">TypeScript 診断 <code>TS2339</code><br />型にあるのは <code>name</code> と <code>price</code></div>
</div>
<div>
<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro</div>

```astro
  {product.nmae}
```

<div class="ch2-range-value">[95, 99)</div>
<div class="ch2-note">8行目の12列目から16列目<br />元のプロパティ名に波線を表示する</div>
</div>
</div>
<div class="ch2-mapping"><strong>Source map と Volar の mapping</strong><span>TSX の範囲を .astro の範囲へ対応させる</span></div>
<div class="ch2-result ch2-editor-result">
<div><div class="ch2-label">Editor に表示する診断</div><div class="ch2-note">LSP の行と列は0始まり</div></div>
<div>
<code>start: { line: 7, character: 11 }</code><br />
<code>end: { line: 7, character: 15 }</code>
</div>
</div>

<Ref href="https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/astro2tsx.ts">convertToTSX と位置対応</Ref>

<!--
前の .astro 全文から、Compiler 2.12.2で生成した TSX を TypeScript 5.9.3へ渡した結果です。型にない nmae に対する診断 TS2339 は、TSX 上の[129, 133)を指します。Compiler の Source map で対応する位置を調べると、.astro では[95, 99)です。抜粋の表示位置から数えた値ではありません。
language-tools は Source map を Volar の mapping へ変換します。Volar がこの対応を利用し、診断範囲を .astro へ戻します。一定の差分34を常に引く方法ではなく、この範囲について対応が確認できたという意味です。
下は Editor へ渡す診断の range の抜粋です。LSP は行と列が0始まりなので、8行目の12列目を line 7と character 11で表します。終端は含みません。
-->

---
layout: default
class: ch2-detail ch2-flow-slide
clicks: 3
---

## .astro からツールのアウトプットまで

<div class="ch2-flow" aria-label=".astro から三つのツールへのフロー">
  <div class="ch2-flow-head ch2-flow-data">中間データ</div><div class="ch2-flow-head ch2-flow-tool">ツール</div><div class="ch2-flow-head ch2-flow-output">アウトプット</div>
  <div class="ch2-flow-source flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" /><code>.astro</code></div>
  <div v-click="1" class="ch2-flow-row ch2-flow-lint">
    <svg class="ch2-flow-branch" viewBox="0 0 42 180" preserveAspectRatio="none" aria-hidden="true"><path d="M0 180 H14 V60 H40 M33 54 L40 60 L33 66" /></svg>
    <div class="ch2-flow-data"><strong>AST とスコープ情報</strong><span>astro-eslint-parser が<br />独自の TSX を<br />JavaScript で解析</span></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-one" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-tool"><strong>ESLint</strong></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-two" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-output">未定義変数の診断</div>
  </div>
  <div v-click="2" class="ch2-flow-row ch2-flow-format">
    <svg class="ch2-flow-branch" viewBox="0 0 42 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 60 H40 M33 54 L40 60 L33 66" /></svg>
    <div class="ch2-flow-data"><strong>整形の指示</strong><span>Babel で<br />expression を解析し、<br />Astro Printer が作成</span></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-one" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-tool"><strong>Prettier</strong></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-two" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-output flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />整形後の .astro</div>
  </div>
  <div v-click="3" class="ch2-flow-row ch2-flow-language">
    <svg class="ch2-flow-branch" viewBox="0 0 42 180" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0 H14 V120 H40 M33 114 L40 120 L33 126" /></svg>
    <div class="ch2-flow-data"><strong>Virtual HTML と TSX</strong><span>HTML は Language Tool、<br />TSX は convertToTSX()</span></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-one" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-tool"><strong>HTML Language<br />Service と TypeScript</strong></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-two" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-output">属性補完と<br />型の診断</div>
  </div>
</div>

<!--
共通の .astro から、中間データとツールとアウトプットへ進むフローです。クリック1で Linter、2で Formatter、3で Language Tool の経路を示します。
Linter は astro-eslint-parser が独自に Virtual TSX を作り、JavaScript Parser から AST とスコープ情報を取得します。位置を元に戻してから ESLint が検査します。
Formatter は expression を Babel 入力へ変換し、Astro Printer が Doc を組み立て、Prettier が文字列にします。Doc は Prettier が整形するために必要な形式です。Doc への変換自体を Compiler の不具合とは説明しません。
Language Tool は自分で生成する Virtual HTML と、Compiler の convertToTSX() が生成する Virtual TSX を使い分けます。HTML Language Service は属性を補完し、TypeScript は型を検査します。結果は .astro と対応させます。
Compiler がすべての中間データを作るわけではありません。二つの Virtual TSX は生成元と用途が異なります。
-->

---
layout: default
class: ch2-detail
---

## `parse()` と `convertToTSX()` を使う難しさ

<div class="ch2-cols ch2-api-recap">
  <div><div class="ch2-label"><code>parse()</code></div><h3 class="!normal-case !tracking-normal">expression の AST と位置の不足</h3><ul><li>変数名と演算子の AST node がない</li><li>位置情報が不正確な箇所がある</li><li>ツールごとに expression を再解析する</li></ul></div>
  <div><div class="ch2-label"><code>convertToTSX()</code></div><h3>型検査を支える変換と位置対応</h3><ul><li>生成コードを TypeScript で解析する</li><li>.astro との位置対応が必要</li><li>補完と型検査を支える変換も保守する</li></ul></div>
</div>
<div class="ch2-summary">情報の不足や不正確さと、<br />用途別の変換に伴う負担を区別する</div>

<!--
parse() の AST では expression の中身が文字列なので、Linter と Formatter は expression を再解析します。一部の位置情報は補正が必要です。これは、正確な AST を受け取った後でツールが受け取る形式へ変換する負担とは区別します。
convertToTSX() は TypeScript の型解析を利用するためのコードを生成します。TypeScript による解析と .astro への位置対応と補完と型検査を支える変換の保守が必要です。すべてを HTML5 由来の欠陥とは説明しません。Rust へ移行して expression の AST を提供できても、TypeScript の型解析やツール固有の形式への変換が不要になるとは限りません。
Source contract は、この発表で Compiler へ求める保証を整理するための呼び名です。書かれた HTML の親子関係と expression の AST と正確な位置情報と生成コードとの位置対応を含みます。Go Compiler がこれらをすべて提供していた、という実装の説明ではありません。
Compiler は Source の親子関係と expression の中身と位置を保証する。Adapter はツールに必要な形式へ変換し、.astro と対応させる。Ecosystem tool は検査と整形と型解析を担う。この分担で考えると、用途別の変換と、Compiler の情報不足に対する再解析や位置の再計算を区別できます。
Compiler が生成したコードとの位置対応は Compiler に求めます。Adapter が独自に変換したコードとの対応は Adapter が管理します。
-->

---
layout: statement
---

<h1 class="!text-5xl !leading-relaxed !m-0">Astro が使える基盤は、<br />2021年からどう変わったのか？</h1>

<!--
第3章では、Go Compiler を選んだ2021年から、Astro が利用できる基盤がどう変わったかを確認します。
-->

---
layout: section
class: ch3-section chapter-three
clicks: 1
---

# 3. 前提の変化
<h2 v-click="1">Astro が再利用できる基盤はどう変わったのか</h2>

<!--
第2章では、expression の AST と位置情報がツールに必要なことを確認した。ここからは、その要求に使える基盤と資料を確認する。
-->

---
layout: default
class: ch3-detail chapter-three ch3-tools
---

## Rust 製のフロントエンドツールが増えた

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
Rust 製のツールは、JavaScript と TypeScript の解析と変換から、CSS、バンドル、タスク実行まで広がった。
SWC は2021年にも利用されていた。Oxc や Rolldown、Rspack、Turbopack など、その後に登場したツールもある。Biome は Rome を引き継いだプロジェクトである。Turborepo は Go から Rust へ移行し、2023年の1.11で移行を完了した。
製品の主な役割を一つずつ示した。Astro がこれらをすべて採用しているという意味ではない。完成したツールを利用する場合と、解析や変換のライブラリを組み込む場合がある。次は Oxc を例に、JavaScript の expression から AST を取得する。
参照：https://nextjs.org/blog/next-12
参照：https://biomejs.dev/blog/announcing-biome/
参照：https://turborepo.dev/blog/turbo-1-11-0
-->

---
layout: default
class: ch3-detail chapter-three code-example-dense
clicks: 1
---

## Oxc で expression の AST を取得する

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
<div v-click="1">
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
<div class="ch3-summary">Rust 製 Parser を npm package から利用できる</div>

<Ref href="https://oxc.rs/docs/guide/usage/parser.html">Oxc Parser</Ref>

<!--
price * amount という JavaScript expression を解析する。右は program.body[0].expression の抜粋で、位置などのフィールドを省いている。Identifier の name で price と amount を、BinaryExpression の operator で掛け算を確認できる。
このコードは npm package の利用例である。Astro Compiler での Rust crate の利用と Astro syntax への対応は第4章で説明する。

補足：利用できるツールと機能
SWC は JavaScript と TypeScript の変換基盤、Biome は検査と整形のツール、Oxc は解析と変換のツール群、Rolldown は Bundler である。Parser には Oxc と SWC、Transformer には SWC と esbuild、Resolver には Oxc と Vite、Bundler には Rollup と Rolldown、Minifier には esbuild と Oxc、Linter には Biome と ESLint、Formatter には Biome と Prettier という選択肢がある。完成したツールとして利用する方法と、ライブラリとして組み込む方法を区別する。
Vite 2では開発時の事前バンドルを esbuild、本番バンドルを Rollup が担っていた。Vite 8は Rolldown を採用した。Astro syntax の変換と汎用的な Build 基盤を分けて考える例である。
参照：https://vite.dev/blog/announcing-vite8

補足：napi-rs と配布方法
Node-API はネイティブ実装を Node.js から利用する API で、napi-rs は Rust の関数を公開する bindings と型定義を生成する。たとえば #[napi] を付けた multiply(p: u32, q: u32) が p * q を返す Rust 関数なら、JavaScript から multiply(1200, 3) を呼び、3600を受け取れる。生成された index.js が OS と CPU に合う実装をロードする。これは呼び出し方の例であり、Astro の実装を示すものではない。
ネイティブバイナリは OS と CPU に対応する実行形式、WASM は対応する実行環境で動かすバイナリ形式、Rust crate は Rust の実装へ組み込むライブラリである。実装言語と配布方法を分けて選ぶ。Node-API と WASM は2021年にも存在し、napi-rs も bindings と型定義の生成を提供していた。
参照：https://napi.rs/docs/introduction/simple-package
参照：https://napi.rs/blog/announce-v2
-->

---
layout: default
class: ch3-detail chapter-three
---

## Biome から学ぶ編集中のコードの解析

<div class="ch3-cols">
<div>
<div class="ch3-label">空白と改行とコメントも保持する</div>

```js
const price = 1200; // 税込

price * amount;
```

</div>
<div>
<div class="ch3-label">編集中の入力も解析する</div>

```js
while {}
```

<p>括弧と条件の expression が<br />欠けても、本文のブロックを<br />解析できる</p>
</div>
</div>
<div class="ch3-note">Lossless CST：元の Source を再現できるよう、<br />空白と改行とコメントも含めた木</div>

<Ref href="https://biomejs.dev/internals/architecture/">Biome Architecture</Ref>

<!--
Source の保持とエラーからの回復は別々の設計課題である。Biome は rowan の fork を基に、空白と改行とコメントも保持する CST を実装している。情報を付加した AST も選択肢になる。
while {} は Biome の設計資料の例である。括弧と条件の expression を欠落として記録し、本文のブロックを解析できる。一方、function} のような入力では正しく解釈できない部分を Bogus node で表す。回復できる範囲は入力とエラーの位置に依存する。
これは Biome の設計例であり、Astro が Biome や Lossless CST を採用したという説明ではない。現在の Astro 実装の回復範囲とも区別する。
-->

---
layout: default
class: ch3-detail chapter-three
---

## Astro syntax の規則を明文化する

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
  <div><strong>expression</strong><span><code>{name}</code></span></div>
  <div><strong>複数のルート要素</strong><span><code>h1</code> と <code>p</code> を並べた Template</span></div>
</div>
</div>

<Ref href="https://github.com/withastro/compiler/blob/04170031ce2f30d1882fe480e87998197e0016aa/SYNTAX_SPEC.md">Astro syntax 仕様ドラフト（Draft、2026年2月）</Ref>

<!--
2026年2月3日付の Draft を参照する。Component script、HTML の属性名、expression、複数ルートの規則を確認できる。右の expression ラベルは波かっこを含む Astro expression の領域に対応し、その中の name が JavaScript expression である。
このページでは構文規則を紹介する。位置情報の精度と編集中の入力への対応は、ツールの要求と合わせて別途設計する。仕様ドラフトが、それらの実装を保証しているという説明ではない。
-->

---
layout: default
class: ch3-detail chapter-three mdx-proposals
clicks: 3
---

## MDX への提案と xmdx の試作

<div class="mdx-lead">Content にも、速度と plugin の柔軟さが必要だった</div>
<div class="mdx-proposal-grid">
  <div class="mdx-evidence">
    <div v-if="$clicks === 0" class="mdx-evidence-pair">
      <img src="/images/mdx/markdown-rs-184-clean.png" alt="markdown-rs への GFM の表の再生成の提案。投稿者 jp-knj" />
      <img src="/images/mdx/markdown-rs-185-clean.png" alt="markdown-rs への WASM bindings の提案。投稿者 jp-knj" />
    </div>
    <img v-if="$clicks === 1" src="/images/mdx/mdxjs-rs-71-clean.png" alt="mdxjs-rs への npm 配布と native bindings の提案。投稿者 jp-knj" />
    <div v-if="$clicks === 2" class="mdx-evidence-pair">
      <img src="/images/mdx/astro-14080-clean.png" alt="Astro への Rust 製 MDX Compiler の試作の提案。投稿者 jp-knj" />
      <img src="/images/mdx/astro-14181-clean.png" alt="Astro への AST Bridge の試作の提案。投稿者 jp-knj" />
    </div>
    <img v-if="$clicks === 3" class="mdx-repo-image" src="/images/mdx/xmdx-clean.png" alt="jp-knj の xmdx リポジトリ" />
  </div>
  <div class="mdx-efforts">
    <section :class="{ 'mdx-current': $clicks < 2 }">
      <h3>Rust ライブラリへの提案</h3>
      <p>markdown-rs に GFM の表の再生成と<br />WASM bindings を提案。<br />mdxjs-rs に npm 配布と<br />native bindings を提案</p>
    </section>
    <section :class="{ 'mdx-current': $clicks === 2 }">
      <h3>Astro への提案</h3>
      <p>Rust 製 MDX Compiler の統合と、<br />既存 plugin と連携する<br />AST Bridge を試作</p>
    </section>
    <section :class="{ 'mdx-current': $clicks === 3 }">
      <h3>xmdx の制作</h3>
      <p>Rust 製 Markdown と MDX の package。<br />Astro と Starlight に組み込み、<br />Astro Docs で検証</p>
    </section>
  </div>
</div>

<!--
Content にも、速度と plugin の柔軟さが必要だった。取り組みを提案先と試作で分けて紹介する。
初期表示は markdown-rs への二つの提案。GFM の表を AST から Markdown へ再生成する機能と WASM bindings を提案した。
クリック 1 は mdxjs-rs への提案。npm 配布と native bindings の提案であり、PR ではない。
クリック 2 は Astro への二つの提案。AST Bridge は mdast と hast を既存の remark と rehype plugin に渡し、加工した AST を Rust へ戻す案だった。
クリック 3 は xmdx。Rust 製 Markdown と MDX の package と Astro integration を試作し、当時の Astro Docs で変換と表示と Build を検証した。出典と確認時の状態は画像の管理資料を参照する。
mdxjs-rs の Issue と Astro への試作 PR と xmdx の実装は、別の成果として説明する。速度の比較値は掲載しない。
-->

---
layout: default
class: ch3-detail chapter-three mdx-integration
clicks: 2
---

## xmdx を Astro に組み込む

<div class="mdx-overview" aria-label="Markdown と MDX を xmdx で変換し、Astro と Starlight のサイトで利用する">
  <div class="mdx-inputs"><span>Markdown</span><span>MDX</span></div>
  <div class="mdx-flow-arrow" aria-hidden="true"></div>
  <div class="mdx-overview-engine"><strong>xmdx</strong><span>Rust 製の解析と変換</span></div>
  <div class="mdx-flow-arrow" aria-hidden="true"></div>
  <div class="mdx-sites"><strong>Astro と Starlight</strong><span>サイトで利用</span></div>
</div>

<h3 class="mdx-detail-label">MDX の変換経路</h3>
<div class="mdx-pipeline">
  <section v-click="1" class="mdx-rust">
    <h3>Rust</h3>
    <p>mdxjs-rs による<br />コード生成</p>
    <p>frontmatter と<br />見出し情報の取得</p>
  </section>
  <section v-click="2" class="mdx-transfer">
    <h3>Node-API</h3>
    <div class="mdx-flow-arrow" aria-hidden="true"></div>
    <p>生成コード<br />frontmatter<br />見出し情報</p>
  </section>
  <section v-click="2" class="mdx-js">
    <h3>JavaScript</h3>
    <p>Astro 用 module への変換</p>
    <p>component の対応<br />コードの色付け</p>
  </section>
</div>
<div class="mdx-wasm-note">WASM 版も用意。図は Node-API を使う MDX の経路</div>

<!--
上段は常時表示する。Markdown と MDX を xmdx で変換し、Astro と Starlight のサイトに組み込む全体図である。下段は MDX の変換経路に限定する。
クリック 1 では Rust の担当範囲を説明する。crates/core/src/mdx_compiler.rs の compile_mdx は frontmatter と見出し情報を取得し、mdxjs-rs を使ってコードを生成する。frontmatter の取得は xmdx が担当する。
クリック 2 では Node-API を経由する情報と JavaScript の担当範囲を説明する。compileMdxBatch の結果にある code と frontmatterJson と headings を受け取り、wrapMdxModule で Astro 用 module に変換する。その後、component の対応とコードの色付けを含む transformPipeline を実行し、transformJsx で JSX を変換する。色付けには Shiki と Expressive Code の経路がある。
参照した実装は画像の管理資料に記録する。互換性のない入力には既存の MDX 実装を利用する fallback もある。前ページの AST Bridge は Astro への別の提案であり、この図の受け渡しは生成コードと付随情報である。
-->

---
layout: default
class: ch3-detail chapter-three
---

## 第3章の結論

<table class="ch3-recap">
<thead><tr><th>第2章からの課題</th><th>第3章で確認したこと</th></tr></thead>
<tbody>
<tr><td>expression の AST</td><td>Oxc の Parser を利用できる</td></tr>
<tr><td>元の Source と編集中の入力</td><td>Biome の設計を参考にできる</td></tr>
<tr><td>Astro syntax</td><td>仕様ドラフトで規則を確認できる</td></tr>
</tbody>
</table>
<div class="ch3-summary">Astro 固有の実装と、<br />既存の基盤に任せる範囲を選び直せる</div>

<!--
expression の AST には Oxc の Parser、元の Source の保持と編集中の入力には Biome の設計例、Astro syntax には仕様ドラフトという基盤と資料を確認した。Markdown と MDX での試作も、plugin の互換性と配布方法という利用条件を検証する経験になった。
Astro 固有の実装と、既存の基盤に任せる範囲を選び直せる。第4章では位置情報も含めて Astro Compiler の担当範囲を確認する。
-->

---
layout: section
class: ch3-section
---

# 4. 新しい判断
<h2>Astro は何を実装し、<br />何を既存の基盤に任せるのか</h2>

<!--
ここから、Astro 自身の実装と既存基盤の担当範囲を説明する。次の全体図で、Compiler と Editor と Build と Content の担当範囲を確認する。
-->

---
layout: center
---

<Overview
  subs="parser,oxc,astro-syntax"
  :roles="{
    editor: 'Source の情報を、診断や補完につなげる',
    build: '変換されたコードをまとめ、実行や配信につなげる',
    content: 'Markdown と MDX の解析と変換',
  }"
/>

<!--
先に結論の図を出します。領域が何を担当するか。Astro Compiler は Astro syntax と変換、そしてその中の汎用的な解析には Oxc を使う。Build は変換されたコードをまとめて実行や配信につなげる。Editor のツールは Source の情報を診断や補完につなげる。Content Processor は Markdown と MDX の解析と変換。Browser は出力された HTML を解釈して DOM を構築する。
-->

---
layout: default
class: body-center
---

## 判断の軸

<div class="grid grid-cols-2 gap-x-10 gap-y-6 mt-12 text-2xl">
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">どの Source 情報を保持するか</div>
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">どの段階で補正や変換を行うか</div>
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">汎用的な解析と変換を、どの基盤に任せるか</div>
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">Astro が、どの機能を実装して保守するか</div>
</div>

<!--
判断の軸は4つです。どの Source 情報を保持するか。どの段階で補正や変換を行うか。汎用的な解析と変換をどの基盤に任せるか。そして Astro がどの機能を実装して保守するか。この4つで、HTML、JavaScript、Markdown と MDX の3つの具体例を確認します。
-->

---
layout: default
class: body-center
---

## Rust Compiler と verbatim parsing

```html
<p>before<div>inside</div>after</p>
```

<div class="mt-5 text-xl text-primary"><code>div</code> を <code>p</code> の子として保持し、位置情報を提供する</div>

<Ref href="https://github.com/withastro/roadmap/issues/1356">Rust Compiler と RFC #1356</Ref>

<!--
第2章の入力です。Go Compiler の Editor が使う API にも literal parsing はありました。Rust Compiler では Build を含め HTML correction を行わない方針です。書かれた入れ子を保持しても、その HTML が妥当になるわけではありません。DOM の構築は Browser が担当します。
-->

---
layout: default
class: body-center
---

## Compiler が受け入れないものもある

<div class="mt-10 text-2xl leading-relaxed">
  <p>Rust Compiler では、<b>HTML correction を行わない</b>方針が明示されている</p>
  <p class="">一方、閉じ忘れたタグなどの構文エラーは拒否する</p>
  <p class="text-primary">どんな入力でも受け入れる、という意味ではない</p>
</div>

<Ref href="https://github.com/withastro/roadmap/issues/1356">withastro/roadmap#1356: 新 Compiler の正式提案</Ref>

<!--
補足です。Rust Compiler では HTML correction を行わない方針が明示されています。ただし、閉じ忘れたタグなどの構文エラーは拒否します。何でも受け入れるという意味ではありません。
-->

---
layout: default
class: body-center
---

## Compiler の AST と、Browser の DOM を分ける

<div class="grid grid-cols-2 gap-8 mt-8 text-xl">
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Compiler 内部の AST</div>
    <ul class="mt-3 text-lg">
      <li>Source の構文を表すデータ</li>
      <li>解析や変換、ツールとの連携に使う</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Browser が構築する DOM</div>
    <ul class="mt-3 text-lg">
      <li>出力 HTML から作る<br />node の親子関係</li>
      <li>表示や JavaScript からの操作に使う</li>
    </ul>
  </div>
</div>

<div class="mt-8 text-xl leading-relaxed">
  <p class="">同じ入れ子の HTML を Browser へ渡せば、Browser では HTML の規則に従って補正が起きる</p>
  <p class="text-primary">HTML correction の方針は、Go か Rust かとは別の設計判断</p>
</div>

<!--
ここで分け直したのは3つの段階です。Source を理解する段階、コードを生成する段階、そして HTML から DOM を構築する段階。同じ入れ子の HTML を Browser へ渡せば、Browser では HTML の規則に従って補正が起きます。それでいい。大事なのは、HTML correction の方針は Go か Rust かとは別の設計判断だということです。言語を変えたから補正をやめたのではなく、責務を分け直した結果です。
-->

---
layout: default
class: body-center
---

## JavaScript AST と Go Compiler の表現

```json
{
  "type": "text",
  "value": "price * quantity"
}
```

<div class="mt-5 text-xl text-primary">ExpressionNode の子の抜粋。識別子を扱うには追加の解析が必要</div>

<Ref href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#parse-astro-and-return-an-ast">Go Compiler 2.12.2と TextNode</Ref>

<!--
第2章で確認した Go Compiler の表現です。expression の Source を取り出せます。次のページでは Rust Compiler の parse API が提供する expression の AST を確認します。
-->

---
layout: default
class: body-center
---

## JavaScript AST と Rust Compiler の表現

```json {4,5}
{
  "type": "BinaryExpression",
  "operator": "*",
  "left": { "type": "Identifier",
            "name": "price" }
}
```

<div class="mt-5 text-xl text-primary">左辺のみ抜粋。右辺と周囲の Astro AST と位置情報は省略</div>

<Ref href="https://github.com/withastro/compiler-rs">Rust Compiler と ESTree 互換 AST</Ref>

<!--
Rust Compiler の parse API は ESTree 互換の AST を返します。実際の BinaryExpression には right もあり、quantity を表す Identifier です。このページでは左辺に注目しています。AST で識別子を区別できても、参照先や型の判定は意味解析の仕事です。
-->

---
layout: default
class: body-center
---

## ツールから見た変化と Editor の役割

<div class="grid grid-cols-2 gap-8 mt-8 text-lg">
  <div class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
    <h3 class="opacity-100 !text-base">ツールから見た変化</h3>
    <ul class="mt-2">
      <li>expression の左辺と右辺をたどれる</li>
      <li>演算子と識別子を個別に扱える</li>
      <li>JavaScript AST を扱うツールと連携しやすくなる</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <h3 class="opacity-100 !text-base">Editor が引き続き担当すること</h3>
    <ul class="mt-2">
      <li>変数の宣言と使用箇所を対応させる</li>
      <li>型情報を調べる</li>
      <li>Astro syntax と位置情報を扱う</li>
      <li>不完全な入力を扱う</li>
    </ul>
  </div>
</div>

<div class="mt-8 text-xl text-primary">AST の提供は、診断や補完を作るための基盤になる</div>

<!--
ツールから見た変化です。expression の左辺と右辺をたどれる。演算子と識別子を個別に扱える。JavaScript の AST を扱う既存のツールで利用しやすくなる。ただし、これで Editor の仕事がなくなるわけではありません。変数の宣言と使用箇所の対応、型情報、Astro syntax と位置情報、不完全な入力。これらは引き続き Editor の仕事です。AST の提供は、診断や補完を作るための基盤になる、ということです。
-->

---
layout: default
class: body-center
---

## Oxc との責務分担

<div class="grid grid-cols-2 gap-8 mt-8 text-xl">
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Oxc へ任せる部分</div>
    <ul class="mt-3 text-lg">
      <li>JavaScript と TypeScript の解析</li>
      <li>expression と識別子の AST</li>
      <li>汎用的な変換とコード生成</li>
    </ul>
  </div>
  <div class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
    <div class="text-2xl font-600">Astro が持つ部分</div>
    <ul class="mt-3 text-lg">
      <li>Astro syntax</li>
      <li>Template と JavaScript の混在</li>
      <li>実行に必要な変換</li>
      <li>.astro との対応</li>
    </ul>
  </div>
</div>

<div class="mt-10 text-2xl">
  Rust Compiler は、<b>Astro の要件に合わせて拡張した Oxc</b> を利用する
</div>

<Ref href="https://github.com/withastro/compiler-rs/blob/main/Cargo.toml">compiler-rs: Cargo.toml</Ref>

<!--
Oxc との責務分担です。Oxc に任せるのは、JavaScript と TypeScript の解析、expression や識別子を表す AST、汎用的な変換やコード生成の基盤。Astro が持つのは、Astro syntax、Template と JavaScript が混在する部分、Astro の実行に必要な変換、そして .astro との対応。Rust Compiler は Astro の要件に合わせて拡張した Oxc を使っています。汎用部分を再利用しながら、必要な変更を加える。自分たちで実装して保守する範囲を絞るという判断です。
-->

---
layout: center
---

<Overview
  highlight="compiler,editor,browser,parser,oxc,astro-syntax"
  subs="parser,oxc,astro-syntax"
  :annotate="{
    'compiler->editor': '書かれた親子関係と位置情報、埋め込まれた JavaScript の AST',
    browser: '出力 HTML から DOM を構築',
  }"
/>

<div class="text-center text-2xl text-primary mt-2">Compiler を less clever にする</div>

<!--
Compiler は Editor に、書かれた親子関係と位置情報、埋め込まれた JavaScript の AST を提供します。Compiler 内部では Oxc が汎用的な解析を担い、Astro が Astro syntax と変換を担当します。Browser は出力 HTML から DOM を構築します。Compiler を less clever にするとは、暗黙に補正する範囲を減らし、解析と変換、Editor や Browser の担当範囲を明確にすることです。
-->

---
layout: default
class: mdx-source-post
---

## Rust Compiler を Prettier plugin で使う

<div class="mdx-post-author">Erika <span>@erika.florist</span><time>2026年8月20日</time></div>
<blockquote class="mdx-post-quote" lang="en">Astro prettier plugin, rewritten on top of our Rust compiler.</blockquote>
<div class="mdx-post-summary">Rust Compiler を基盤に書き直した<br />Astro の Prettier plugin を、<br />1.0 に向けた beta として公開</div>
<div class="mdx-post-takeaway">Compiler が提供する情報を、整形ツールが利用する</div>

<!--
Erika が 2026年8月20日に投稿した内容。引用は原文の一部で、日本語は投稿の要約である。投稿時点で、Rust Compiler を基盤に書き直した Astro の Prettier plugin の 1.0 に向けた beta を公開している。
Compiler が提供する AST と位置情報をツールが利用する具体例として紹介する。整形結果を作るのは Prettier plugin の担当である。
-->

---
layout: default
class: mdx-source-post
---

## Sätteri が選んだ Rust と JavaScript の分担

<div class="mdx-post-author">Erika <span>@erika.florist</span><time>2026年4月9日</time></div>
<blockquote class="mdx-post-quote" lang="en">The expensive stuff in Rust,<br />your flexible plugins in JavaScript.</blockquote>
<div class="mdx-post-summary">Markdown と MDX を変換する Sätteri を紹介。<br />計算負荷の高い部分は Rust、<br />柔軟な plugin は JavaScript が担当する</div>
<div class="mdx-post-takeaway">Content でも、速度と拡張のしやすさを両立する設計</div>

<!--
Erika が 2026年4月9日に Sätteri を紹介した投稿。引用は原文の一部で、日本語は投稿の要約である。前ページとは話題の順で並べており、投稿の時系列ではない。
第3章の Content に必要だった条件を踏まえ、ここから Sätteri が Rust と JavaScript の担当範囲をどう分けたかを説明する。
-->

---
layout: default
class: body-center
---

## Sätteri と JavaScript plugin の分担

<div class="grid grid-cols-2 gap-10 mt-10 text-xl">
  <div>
    <h3 class="opacity-100 !text-base">Sätteri</h3>
    <ul class="mt-3">
      <li>Rust が解析と変換を担う</li>
      <li>よく使う変換を標準機能として提供</li>
      <li>JavaScript で拡張できる</li>
    </ul>
  </div>
  <div>
    <h3 class="opacity-100 !text-base">plugin との境界</h3>
    <div class="grid grid-cols-[2rem_1fr] gap-x-3 gap-y-4 mt-3">
      <div class="text-primary">1</div><div>扱う node の種類を指定</div>
      <div class="text-primary">2</div><div>JavaScript で node を検査と変更</div>
      <div class="text-primary">3</div><div>必要な情報だけを受け渡す</div>
    </div>
  </div>
</div>

<Ref href="https://satteri.bruits.org/docs/plugins/">Sätteri: Plugin API</Ref>

<!--
Sätteri では、Rust が Markdown と MDX の解析と変換を担い、よく使う変換を標準機能として提供します。JavaScript では独自の変換を追加できます。plugin は扱う node の種類を指定し、その node を検査したり変更したりする関数を JavaScript で実行します。これが visitor です。たとえば見出しやリンクの node を指定し、必要な情報だけを Rust と JavaScript の間で受け渡します。
-->

---
layout: default
class: body-center
---

## Astro と Content Processor の分担

<div class="text-xl mb-6">Content Processor は Markdown と MDX を解析し、HTML や JavaScript へ変換する</div>

<div class="grid grid-cols-2 gap-8 text-xl">
  <div class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
    <div class="text-2xl font-600">Astro が担当すること</div>
    <ul class="mt-3 text-lg">
      <li>Processor を組み込む入口を用意する</li>
      <li>Content Collections と Build に統合</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Processor が担当すること</div>
    <ul class="mt-3 text-lg">
      <li>Markdown と MDX の構文</li>
      <li>Content 固有の変換</li>
      <li>拡張機能を実行する仕組み</li>
    </ul>
  </div>
</div>

<div class="mt-8 text-xl text-primary">Content Processor は Astro Compiler とは別に選ぶ</div>

<!--
第3章では、Rust 製 MDX Compiler の PoC と plugin 互換性の問題を確認しました。ここでは、Markdown と MDX の担当範囲を分けます。Astro は Processor を組み込む入口を用意し、Content Collections や Build に統合します。Processor は Markdown と MDX の構文、Content 固有の変換、拡張機能を実行する仕組みを担当します。Content Processor は Astro Compiler とは別に選びます。
-->

---
layout: default
class: body-center
---

## unified の設定と import

```js
import { defineConfig } from "astro/config";
import { unified }
  from "@astrojs/markdown-remark";

const contentProcessor = unified();
```

<div class="mt-5 text-xl text-primary">既存の remark と rehype plugin を使うための選択肢</div>

<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Astro Docs と Markdown Processors</Ref>

<!--
必要な package を導入したうえで、unified の Processor を作ります。次のページで Astro の設定に指定します。
-->

---
layout: default
class: body-center
---

## unified の設定と Processor を指定する

```js
export default defineConfig({
  markdown: {
    processor: contentProcessor,
  },
});
```

<div class="mt-5 text-xl text-primary">前ページの続き。Astro が選択した Processor へ本文を渡す</div>

<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Astro Docs と Markdown Processors</Ref>

<!--
Astro は Processor を呼び出し、Processor は Content を解析して変換します。既存 plugin を利用する経路を明示的に選べます。
-->

---
layout: default
class: body-center
---

## 実装言語と、配布方法を分けて考える

<div class="grid grid-cols-4 gap-5 mt-8 text-lg">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">実装言語</div>
    <div class="mt-2">どの言語で実装するか</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">配布と実行方法</div>
    <div class="mt-2">どう配布し、どの環境で実行するか</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">AST 設計</div>
    <div class="mt-2">構文の表し方と保持する情報</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">責務の所有</div>
    <div class="mt-2">どの project が実装して保守するか</div>
  </div>
</div>

<div class="mt-8 text-xl leading-relaxed">
  <p class="text-primary">これらは、それぞれ別の判断になる</p>
  <p class="">Node.js からは native bindings で呼び出す。<br />Browser 内で Compiler を動かす場合は WASM の経路を考える</p>
  <p class="text-lg">全体図の Browser は、生成されたサイトを表示する場所。Compiler 自体を Browser 内で実行する話とは区別する</p>
</div>

<Ref href="https://github.com/withastro/compiler-rs">Rust Compiler README と bindings の構成</Ref>

<!--
第1章の選択を、ここでは4つに分けます。実装言語、配布と実行方法、AST 設計、責務の所有です。Node.js からは native bindings で呼び出し、Browser 内で Compiler を動かす場合は WASM の経路を考えます。Rust Compiler にも WASM で動作する実装があり、提供する環境と API は実装ごとに確認する必要があります。全体図の Browser は生成されたサイトを表示する場所です。Compiler 自体を Browser 内で実行する場合とは区別します。
-->

---
layout: center
---

<Overview
  subs="parser,oxc,astro-syntax"
  :annotate="{
    compiler: 'parse() で AST を提供し、transform() で JavaScript へ変換する',
    editor: 'AST と位置情報から、診断と補完を提供する',
    content: 'frontmatter と見出し ID、コードの色付け、MDX component',
  }"
/>

<!--
Astro Compiler は Astro syntax を解析して親子関係と位置情報を保持し、parse() で AST を提供し、transform() で HTML を生成する JavaScript へ変換します。汎用的な解析には Oxc を使います。Editor は AST と位置情報を利用し、不完全な構文を扱いながら診断と補完を提供します。Build はモジュールを解決し、JavaScript と CSS をまとめます。Vite とその内部の Rolldown を使いますが、Compiler と Build の分担は Go Compiler の導入時から存在していました。Astro の Content は Processor を選ぶ入口を用意し、Content Collections と Build に統合します。Content Processor は Markdown と MDX の解析と変換、frontmatter、見出しの ID、コードの色付け、MDX component を担当し、汎用的な機能と plugin model を保守します。unified ecosystem は既存 plugin が必要な利用者の経路を担います。Rust Compiler の公開 API は parse() と transform() が中心です。Language Server に渡す TSX の出力は、実行コードを生成する Compiler とは別の要件として扱われています。
-->

---
layout: default
class: body-center
---

## 三つの具体例を、同じ全体図へ重ねる

<div class="grid grid-cols-3 gap-6 mt-10 text-lg">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-black">HTML</div>
    <div class="text-2xl font-600 mt-1">保持と補正</div>
    <ul class="mt-3">
      <li>書かれた親子関係を保持する</li>
      <li>Compiler の解析と Browser の DOM 構築を区別する</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-black">JavaScript</div>
    <div class="text-2xl font-600 mt-1">AST の提供と再利用</div>
    <ul class="mt-3">
      <li>expression の内部を AST として提供する</li>
      <li>汎用的な解析には Oxc を利用する</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-black">Markdown と MDX</div>
    <div class="text-2xl font-600 mt-1">互換性と所有</div>
    <ul class="mt-3">
      <li>plugin との互換性も要件に含める</li>
      <li>Astro との統合と、Content の解析と変換を分ける</li>
    </ul>
  </div>
</div>

<!--
3つの具体例を並べます。HTML では、書かれた親子関係を保持し、Compiler の解析と Browser の DOM 構築を区別します。JavaScript では expression の AST を提供し、汎用的な解析は Oxc に任せます。Markdown と MDX では plugin の互換性も要件に含め、Astro との統合と汎用的な Content の変換を分けます。
-->

---
layout: center
---

<Overview
  subs="parser,oxc,astro-syntax"
  contract="source,output,ecosystem"
/>

<!--
ここでの契約とは、連携する相手へ保証する情報や振る舞いを指します。Source contract は主に Compiler と Editor の間の契約です。書かれた親子関係と位置を保持し、埋め込まれた構文をツールが利用できる形で渡します。Output contract は Compiler と Build と Browser の間の契約です。実行や表示に使う成果物を生成し、Source の入れ子と表示時の DOM の親子関係を区別します。Ecosystem contract は Content Processor と plugin ecosystem の間の契約です。既存 plugin を利用できる経路を維持し、新しい plugin model への移行方法を用意します。
-->

---
layout: default
class: body-center
---

## この章の結論

<div class="mt-10 text-xl leading-relaxed">
  <ul>
    <li>Rust への移行では、<b>Compiler の設計と保守範囲</b> も見直している</li>
    <li>汎用的な解析と変換には、<b>既存の基盤</b> を利用する</li>
    <li>Astro は、<b>Astro syntax と変換と統合</b> を担当する</li>
    <li>用途に応じて、<b>Rust と JavaScript の役割</b> を分ける</li>
    <li>Astro Compiler と Markdown と MDX の Processor も、<br />それぞれの要件に合った構成を選ぶ</li>
  </ul>
</div>

<!--
Rust への移行では、Compiler の設計と保守範囲も見直しています。汎用的な解析と変換には既存の基盤を使い、Astro は Astro syntax と変換と統合を担当します。用途に応じて Rust と JavaScript の役割を分け、Astro Compiler と Markdown と MDX の Processor も、それぞれの要件に合った構成を選びます。
-->

---
layout: statement
class: flex flex-col justify-center h-full
---

# 動いていた Go Compiler を、<br /><span>Astro はなぜ Rust で<br />書き直したのか？</span>

<!--
最初の問いに戻ります。
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
当時は、高速な変換と複数環境での実行が必要で、Go と WASM がその要件に対応していました。使い続けるなかで、Source の親子関係と位置を扱う要求が明確になり、HTML correction による不具合や予想しにくい挙動、独自実装の保守の難しさが分かりました。その後、Rust の解析と変換基盤が育ち、汎用的な機能を再利用できる範囲が広がり、Astro syntax の整理も進みました。新しい判断は、保持する情報と変換する段階を明確にし、既存基盤を使って保守範囲を絞り、チームが継続して改善できる Compiler へ作り直すことです。Content での取り組みも、Markdown と MDX の解析と変換を通じて、同じ責務設計の問題を検証したものでした。
-->

---
layout: center
class: text-center
---

<div class="text-5xl font-700 leading-[1.5]" style="color: #7611A6">
  既存の基盤を再利用し、<br />
  <span>自分たちの実装範囲を絞り、</span><br />
  <span>保守し続けられる設計にするため。</span>
</div>

<!--
Rust の基盤を再利用し、Astro が実装して保守する範囲を絞って、継続して改善できる Compiler へ再設計するためです。
-->

---
layout: default
class: body-center takeaway-slide
---

## 持ち帰ってほしいこと

<div class="mt-8 text-2xl text-primary">技術選定は、その時点の要件と利用できる基盤に対する判断</div>

<div class="mt-8 text-xl">
  <h3 class="opacity-100 !text-base">技術を選び直すときに確認すること</h3>
  <ul class="mt-3">
    <li>当時、何を実現するために選んだのか</li>
    <li>利用が広がり、何が新しく必要になったのか</li>
    <li>今なら、どの機能を既存基盤に任せられるのか</li>
    <li>自分たちが実装して保守すべき範囲はどこか</li>
  </ul>
</div>

<div class="mt-8 text-xl leading-relaxed">
  <p>技術を選び直す機会に、<b>担当する責務も見直す</b></p>
  <p class="">PoC が merge されなくても、制約を明らかにし、コミュニティの次の判断につなげられる</p>
</div>

<!--
技術選定は、その時点の要件と利用できる基盤に対する判断です。選び直すときには、当時何を実現するために選んだのか、利用が広がって何が新しく必要になったのか、今ならどの機能を既存基盤に任せられるのか、自分たちが実装して保守すべき範囲はどこかを確認します。技術を選び直す機会に、担当する責務も見直します。PoC が merge されなくても、制約を明らかにして、コミュニティの次の判断につなげることはできます。
-->

---
layout: center
class: text-center
---

## ありがとうございました

<div class="mt-8 text-xl ">Astro Japan Community</div>

<img src="./images/qrcode_discord.com.png" class="h-60 mx-auto mt-6" alt="Discord QR Code" />

<!--
ありがとうございました。Astro Japan Community の Discord です。よかったら覗いてみてください。
-->
