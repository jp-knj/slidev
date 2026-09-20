---
theme: ./theme-light
author: jp-knj
title: なぜAstroはGoコンパイラをRustで書き直したのか
info: |
  動いていたGoコンパイラを、AstroはなぜRustで書き直したのか。
  当時の判断・発見した問題・前提の変化・新しい判断の4章で、技術選定を責務の設計として読み解く。
duration: 40min
mdc: true
transition: fade
colorSchema: light
themeConfig:
  primary: "#bc52ee"
layout: center-vertical
class: text-center
---

<div class="text-2xl text-[#6B7280] font-400">Astro Compiler</div>

<h1 class="!text-6xl !font-700 mt-4 leading-tight">
  動いていたものを、<br />なぜ書き直すのか
</h1>

<div class="text-xl text-[#6B7280] mt-8">
  GoとWASMからRustへ、5年ぶんの前提の変化
</div>

<!--
こんにちは。今日は「動いていたものを、なぜ書き直すのか」という話をします。題材は Astro のコンパイラです。2021年に Go と WASM で書かれたコンパイラが、2026年に Rust で書き直されました。その判断の中身を、4つの章に分けて追いかけます。
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

# Goを動いていたものを、<br />なぜ、Rustに書き直すのか？

<!--
今日の問いはこれ1つです。「動いていた Go コンパイラを、Astro はなぜ Rust で書き直したのか」。速いから、で終わらせずに、何が問題で、何が変わって、どう責務を分け直したのかを見ていきます。
-->

---
layout: default
class: body-center
---

## 四つの構成

<div class="grid grid-cols-2 gap-x-10 gap-y-6 mt-10">
  <div class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-3xl font-600 mt-1">当時の判断</div>
    <div class="text-lg opacity-60 mt-2">なぜ最初にGoとWASMを選んだのか</div>
  </div>
  <div class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-3xl font-600 mt-1">発見した問題</div>
    <div class="text-lg opacity-60 mt-2">使い続けるなかで何が見えたのか</div>
  </div>
  <div class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-3xl font-600 mt-1">前提の変化</div>
    <div class="text-lg opacity-60 mt-2">2026年までに周囲はどう変わったのか</div>
  </div>
  <div class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-3xl font-600 mt-1">新しい判断</div>
    <div class="text-lg opacity-60 mt-2">その結果、責務をどう分け直したのか</div>
  </div>
</div>

<!--
構成は4つです。当時の判断、発見した問題、前提の変化、新しい判断。この順で、判断の材料がどう入れ替わったのかを追います。
-->

---
layout: section
---

# 1. 当時の判断
## なぜ最初にGoとWASMを選んだのか

<!--
まず第1章。2021年に何を選んだのか、そしてそれはどういう条件下での選択だったのかを確認します。
-->

---
layout: center
---

<Overview visible="source,compiler,build,browser" :labels="{ build: 'Vite' }" />

<div class="text-center text-xl opacity-60 mt-2">2021年に必要だったのは、この一本道だった</div>

<!--
これが出発点の全体図です。.astro のソースを Astro Compiler が読んで、Build に渡して、最後にブラウザが表示する。この講演では、この図に何度も戻ってきます。章が進むごとに、登場人物と矢印が増えていきます。
-->

---
layout: default
class: body-center
---

## 2021年は、Rust一色ではなかった

<div class="mt-12 relative">

  <!-- 軸。ドットの中心（上から 50px）に合わせて引く -->
  <div class="absolute left-0 right-0 top-[50px] h-[2px] bg-[#D9D3E2]"></div>

  <div class="relative flex items-start">
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-[#717781] h-11 leading-none">Feb</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-vitejs class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Vite 2.0</div>
      <img src="./images/logos/gopher.svg" alt="Go" class="h-16 mt-6" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-[#717781] h-11 leading-none">Sep</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-rome-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Rome</div>
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-11 mt-9" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-[#717781] h-11 leading-none">Oct</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-parcel-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Parcel 2</div>
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-11 mt-9" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-[#717781] h-11 leading-none">Oct</div>
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
      <img src="./images/logos/gopher.svg" alt="Go" class="h-16 mt-6" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-[#717781] h-11 leading-none">Dec</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-turborepo-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Turborepo</div>
      <img src="./images/logos/gopher.svg" alt="Go" class="h-16 mt-6" />
    </div>
  </div>
</div>

<!--
2021年の状況を並べてみます。Rome が Rust への書き直しを発表し、Parcel 2 と Next.js 12 が Rust 製のコンパイラを採用した年です。でも同時に、Vite 2 は Go 製の esbuild を使っていたし、Turborepo も Go でした。つまり「Rust 一色」ではなかった。Go を選ぶことが特別に珍しい判断ではない時期だった、というのが押さえておきたい点です。
-->

---
layout: default
class: center-vertical
---

<Overview
  visible="source,compiler,build,browser"
  :labels="{ compiler: 'Go Compiler', build: 'Vite' }"
  :icons="{ compiler: 'go' }"
  dashed="compiler->build"
  :edgeLabels="{ 'compiler->build': 'WASM 境界' }"
/>

<div class="mt-10 flex justify-center gap-10 text-lg opacity-70">
  <div>Build のための Compiler だった</div>
  <div>主な入口は <code>transform</code> API</div>
</div>

<div class="mt-12 border-l-2 border-[#BC52EE] pl-5">
  <div class="text-2xl font-600 text-primary">深く考えすぎずに選んだ</div>
  <div class="text-xl opacity-70 mt-2">esbuild が Go だった。Go は学びやすかった。</div>
</div>

<Ref href="https://natemoo.re/posts/hello-from-the-other-side/">Nate Moore — Hello from the other side</Ref>

<!--
Astro のコンパイラは Svelte のコンパイラの fork から始まりました。そこに Go を置き、JavaScript との境界に WASM を置き、ビルドは Vite に任せた。重要なのは、当時これは「ビルドのためのコンパイラ」だったということです。主な入口は transform API ひとつ。ソースを受け取って、実行できる JavaScript を返す。それが仕事のすべてでした。
選んだ理由は本人がこう書いています。esbuild が Go で書かれていたこと、Go が学びやすかったこと。深く考えすぎずに選んだ、と。そして esbuild を参考に Go を学んで、HTML5 のパーサを Astro 向けに拡張した。ここで HTML5 パーサをベースにしたことが、第2章の話につながります。
-->

---
layout: default
class: body-center
---

## 分けて考える選択

<div class="grid grid-cols-3 gap-6 mt-10 text-xl">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">実装言語</div>
    <div class="text-2xl font-600 mt-2">Go か Rust か</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">配布と実行</div>
    <div class="text-2xl font-600 mt-2">ネイティブバイナリか WASM か</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">置き換える範囲</div>
    <div class="text-2xl font-600 mt-2">全体か、重い処理だけか</div>
  </div>
</div>

<div class="mt-10 text-xl opacity-70">
  そしてどの選択でも、JavaScript の境界には WASM や JSON 変換のコストが残る
</div>

<!--
ここで、ひとつの判断に見えるものが実は3つに分かれることを確認しておきます。実装言語をどうするか。それをどう配布して、どこで動かすか。そして、全体を置き換えるのか重い処理だけを置き換えるのか。この3つは独立に決められます。第4章でもう一度この軸に戻ってきます。あと、どの選択をしても、JavaScript との境界には WASM や JSON 変換のコストが残ります。
-->

---
layout: default
class: body-center
---

## この章の結論

<div class="mt-10 text-2xl leading-relaxed">
  <p>Go は、Compiler の実装要件に対応していた</p>
  <p>WASM は、配布と実行環境の要件に対応していた</p>
  <p class="mt-8 text-primary font-600">GoとWASMは、2021年のAstroに合った合理的な選択だった</p>
</div>

<div class="mt-8 text-xl opacity-60">
  この判断を失敗として扱うのではなく、当時の要件に対する選択として扱う
</div>

<!--
第1章の結論です。Go はコンパイラの実装要件に合っていたし、WASM は配布と実行環境の要件に合っていた。2021年の Astro にとって、これは合理的な選択でした。今日の話は「あれは失敗だった」という話ではありません。当時の要件に対する正しい選択が、要件が変わったことで見直された、という話です。
-->

---
layout: section
---

# 2. 発見した問題
## 使い続けるなかで何が見えたのか

<!--
第2章です。Go と WASM のコンパイラを使い続けるなかで、何が見えてきたのか。ここからは具体的なコードと AST を見ていきます。なお、これから出す AST の例は、説明に必要な部分だけを抜き出したものです。実際にはソース位置などのフィールドが付きます。
-->

---
layout: center
---

<Overview />

<div class="text-center text-xl opacity-60 mt-2">Editor のツールと Content の経路が増えた</div>

<!--
全体図に登場人物が増えました。Editor のツール、つまり ESLint や Language Server や Formatter が、同じコンパイラを使うようになった。それと Markdown / MDX の経路。Content の経路は図に残しますが、第3章の後半まで強調はしません。この章では2か所にズームします。HTML の構造と、埋め込まれた JavaScript です。
-->

---
layout: default
class: code-tall body-center
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
````

<!-- いま足された構文だけを1つ見せる。v-click は非表示でも場所を取るので $clicks で出し分ける -->
<div class="mt-4 text-center text-2xl">
  <div v-if="$clicks === 0"><span class="text-primary font-600">Component script</span><br /><code>---</code> で囲む。ビルド時とサーバーで実行する JS と TS</div>
  <div v-if="$clicks === 1"><span class="text-primary font-600">Template</span><br />HTML を基礎に、式やコンポーネントを書ける</div>
  <div v-if="$clicks >= 2"><span class="text-primary font-600">{ }</span><br />JavaScript 式の結果を、その場所に表示する</div>
</div>

<Ref href="https://docs.astro.build/en/reference/astro-syntax/">Astro Syntax — Astro Docs</Ref>

<!--
Astro の構文をおさらいします。三本線で囲まれた Component script と、その下の Template。Template は HTML を基礎にしていて、波かっこで JavaScript の式を埋め込めます。ここで大事なのは、JSX に似た構文であっても、同じ規則とは限らないということです。Astro は HTML を基礎にした構文です。この違いが、次の話につながります。
-->

---
layout: default
class: code-tall body-center
clicks: 1
---

## Astro Syntax で受けたフィードバック

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

<!-- 問いと答えを同じ帯に入れて、行数が変わっても位置が動かないようにする -->
<div class="mt-4 h-[96px] flex items-center justify-center text-center text-2xl">
  <div v-if="$clicks === 0">この <code>title</code> は、どちらの値になる？</div>
  <div v-else class="grid grid-cols-[auto_auto_auto] gap-x-5 gap-y-2 items-center text-left">
    <div>期待した値</div><div><code>second</code></div>
    <div>実際の値</div><div><code>first</code></div>
  </div>
</div>

<Ref href="https://github.com/withastro/astro/issues/5558#issuecomment-1343799494">astro#5558 — spread attributes と重複属性</Ref>

<!--
属性の話です。HTML では、同じ属性を2回書くとブラウザは先に書いたほうを採用します。先行優位です。一方 React と Babel の props 合成では、後から指定したものが上書きします。後行優位。同じように見える書き方で、規則が逆になっている。
-->

---
layout: default
class: code-tall body-center
clicks: 1
---

## Astro Syntax として改行の扱いがおかしい

```astro
<span>Astro</span>
<span>1200</span>
```

<!-- 問いと答えを同じ帯に入れて、行数が変わっても位置が動かないようにする -->
<div class="mt-4 h-[96px] flex items-center justify-center text-center text-2xl">
  <div v-if="$clicks === 0">この表示はどうなる？</div>
  <div v-else class="grid grid-cols-[auto_auto_auto] gap-x-5 gap-y-2 items-center text-left">
    <div>期待した表示</div><div><code>Astro1200</code></div>
    <div>実際の表示</div><div><code>Astro 1200</code></div>
  </div>
</div>

<Ref>
  <a href="https://github.com/withastro/astro/issues/6011">astro#6011 — 要素の間に空白だけのテキストノードが入る</a>
  <a v-if="$clicks >= 1" href="https://blog.dwac.dev/posts/html-whitespace/" class="ml-8">HTML Whitespace is Broken</a>
</Ref>

<!--
もうひとつの驚きです。2023年に報告された issue で、要素を1行ずつ改行して並べると、あいだに空白だけのテキストノードが入る。Next.js の出力と比べて違う、という指摘でした。返答は「Astro is not like JSX. 書いたソースの改行は、そのまま出力に残る」。3日でクローズされています。規則としてはそのとおりなんですが、この issue は2024年、2025年とコメントが付き続けました。同じ場所を踏む人が出続けたということです。書いた見た目と表示がずれるという意味では、さっきの属性の話と同じ形をしています。そして、この空白をどう扱うかを決めているのもコンパイラではなく、ブラウザの HTML 解析です。次は、その HTML の解析が何をしているのかを見ていきます。
-->

---
layout: default
class: code-compact body-center
clicks: 2
---

## Astro Syntax で受けたフィードバック

<div>

<div class="flex gap-8 w-full">
  <div class="min-w-0 code-split" :class="$clicks >= 1 ? 'w-[calc(50%-1rem)]' : 'w-full'">
    <div class="text-primary font-600 text-xl mb-1 flex items-center gap-2"><logos-astro-icon class="w-5 h-5" />書いた .astro</div>

```astro
<table>
  <tr><td>{'foo'}</td></tr>
</table>
<h2>Chats</h2>
```

  </div>
  <Transition name="reveal-right">
  <div class="min-w-0 w-[calc(50%-1rem)]" v-if="$clicks >= 1">
    <div class="text-primary font-600 text-xl mb-1 flex items-center gap-2"><logos-html-5 class="w-5 h-5" />解釈された HTML</div>

```html
<table>
  <tr><td>foo</td></tr>
  <h2>Chats</h2>
</table>
```

  </div>
  </Transition>
</div>

<Transition name="reveal-up">
<div class="mt-10 text-center" v-if="$clicks >= 2">
  <div class="text-2xl">これはバグではなく、<b>HTML の解析仕様に書かれた回復規則</b></div>
</div>
</Transition>

</div>

<Ref href="https://github.com/withastro/compiler/issues/870">compiler#870 — Astro misparses table HTML</Ref>

<!--
実際に報告された issue です。table を閉じたあとに h2 を書いている。素直に読めば、表の下に見出しが来るはずです。ところが出力された HTML では、h2 が table の中に入ってしまう。しかもブラウザがこの HTML を読むと、今度は h2 を table の外へ、それも表より上へ追い出します。書いたものと、コンパイラが作る構造と、ブラウザが作る構造が、三者三様にずれている。
ここで押さえておきたいのは、こういう組み替えがバグではないということです。HTML の解析仕様には、想定外のタグが来たときにどう直すかという回復規則が書かれていて、ブラウザもコンパイラもそれに従っています。たとえば p の中に div を書くと、div の開始時に p が閉じられ、最後の閉じ p に対応して空の p が生成される。書いたものと、できあがる構造が違う。HTML 補正が働く Go 版コンパイラでも、同様の構造変更が AST に起きていました。
余談ですが、その解析仕様には、閉じ sarcasm タグを受け取った場合の記述もあります。そこには実際に「Take a deep breath」、深呼吸をしろ、と書かれていて、その後は他の終了タグと同じ処理に進みます。……HTML の仕様書を読んでいたら、深呼吸を指示されました。
-->

---
layout: default
class: body-center
---

## HTMLを土台にした構文を、どう解析していたか

<div class="grid grid-cols-3 gap-8 mt-12 text-xl">
  <div>
    <div class="text-primary font-600 text-2xl">HTML First</div>
    <div class="opacity-70 text-lg mt-3">AstroはHTMLを土台にしている</div>
  </div>
  <div>
    <div class="text-primary font-600 text-2xl">JSX Like</div>
    <div class="opacity-70 text-lg mt-3">そこにJavaScript式やComponentを記述できる構文が加わる</div>
  </div>
  <div>
    <div class="text-primary font-600 text-2xl">HTML5 parserの挙動</div>
    <div class="opacity-70 text-lg mt-3">従来のGo Compilerでは、HTMLの解析規則に従って、書かれた構造を補正する場合があった</div>
  </div>
</div>

<Ref href="https://docs.astro.build/en/reference/astro-syntax/">Template expressions reference — Astro Docs</Ref>

<!--
ここまでの話を、設計思想、構文、解析方法の3つで振り返ります。まず HTML First。Astro は HTML を土台にしている。これは設計思想です。次に JSX Like。そこに JavaScript の式やコンポーネントを書ける構文が加わる。Astro の公式ドキュメントでも、構文を HTML の拡張として位置づけて、式の記述を JSX-like Expressions と呼んでいます。みっつめが HTML5 parser の挙動。これは前の2つとは別の話で、解析方法の話です。従来の Go Compiler では、HTML の解析規則に従って、書かれた構造を補正する場合がありました。HTML First であることと、コンパイラの内部で HTML5 の構造補正を行うことは、分けて考えてください。ここでは補正の中身には立ち入りません。置いておきたい問いはこれです。では、書いた構造は、どの段階で変わっていたのでしょうか。
-->

---
layout: default
class: body-center
---

## 同じCompilerを、Editorのツールも使い始めた

<div class="grid grid-cols-3 gap-6 mt-10 text-xl">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-2xl font-600">ESLint</div>
    <div class="opacity-60 mt-2 text-lg">問題のある構文を調べる</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-2xl font-600">Language Server</div>
    <div class="opacity-60 mt-2 text-lg">診断と補完を提供する</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-2xl font-600">Formatter</div>
    <div class="opacity-60 mt-2 text-lg">構造と空白とコメントを扱う</div>
  </div>
</div>

<div class="mt-10 text-xl">
  <p>どれも「ユーザーが何を書いたか」を知りたい</p>
  <p class="text-primary">出力を作るための情報とは、求めるものが違う</p>
</div>

<div class="mt-10 text-2xl text-primary">では、書いた構造は、どの段階で変わっていたのか？</div>

<!--
同じコンパイラをエディタでも使うようになって、必要な情報の違いが見えてきました。ESLint は問題のある構文を調べたい。Language Server は診断と補完を出したい。Formatter は構造だけでなく空白やコメントも扱いたい。どれも「ユーザーが何を書いたか」を知る必要がある。出力を作るための情報とは、求めるものが違います。この視点で、さっきの3つの現象を並べ直すと、実装の中に埋もれていた前提が見えてきます。
-->

---
layout: default
class: body-center
---

## 書いたものと、表示されるものを分ける

<Overview
  visible="source,compiler,build,browser"
  :labels="{ compiler: 'AST', build: 'code', browser: 'DOM' }"
  :subnotes="{
    source: '書いたソース',
    compiler: 'Compilerの内部',
    build: 'Compilerが生成',
    browser: 'Browserが構築',
  }"
  :icons="{ build: '' }"
  dashed="build->browser"
  :annotate="{
    'build->browser': 'コードを実行してHTMLを生成し、BrowserがHTMLを解析する',
  }"
/>

<div class="mt-6 text-2xl text-primary">いま話している構造は、この4つのどれなのか</div>

<!--
さっきまでと同じ全体図ですが、箱の中身が違います。登場人物ではなく、これ以降の説明で使う4つの表現を、同じ場所に置き直したものです。ユーザーが書いたソース、コンパイラ内部の AST、コンパイラが生成するコード、そしてブラウザが構築する DOM。ここでの目的は、全工程を詳しく解説することではありません。いま話している構造がこの4つのどれなのか、区別できるようにすることです。ひとつ補足しておくと、生成コードから直接 DOM になるわけではありません。旧コンパイラが出力するのは HTML そのものではなく、HTML を生成するモジュールです。それを実行して HTML ができ、ブラウザがその HTML を解析して DOM を作る。この段階の違いは、あとで効いてきます。
-->

---
layout: default
class: body-center
---

## 補正された木から、元の入れ子を診断できるか

<div class="grid grid-cols-2 gap-8 mt-4">
  <div class="min-w-0">
    <div class="text-lg opacity-60 mb-1">書いたソース</div>

```html
<p>before<div>inside</div>after</p>
```

  </div>
  <div class="min-w-0">
    <div class="text-lg opacity-60 mb-1">解析後の構造をHTMLで表すと</div>

```html
<p>before</p>
<div>inside</div>
after
<p></p>
```

  </div>
</div>

<div class="mt-6 text-xl">
  <p class="!my-0">旧 Go Compiler も、不正な入れ子をHTMLの解析規則に合わせて組み替えていた</p>
  <p class="!mt-3 !mb-0">Editorで「<code>p</code> の中に <code>div</code> を書いています」と診断したい。しかし補正後の木には、その親子関係がもうない</p>
  <p class="text-primary font-600 !mt-5 !mb-0">補正後の親子関係だけを見ても、書かれていた親子関係は分からない</p>
</div>

<Ref>
  <a href="https://html.spec.whatwg.org/multipage/parsing.html">HTML Standard — Parsing HTML documents</a>
  <a href="https://docs.astro.build/en/guides/upgrade-to/v7/" class="ml-8">Astro Docs — Upgrade to v7</a>
</Ref>

<!--
ここで初めて、HTML5 parser の具体的な挙動に入ります。さっきの table の例と同じ規則です。p の中に div を書くと、div の開始時点で p が閉じられます。最後の閉じ p に対応する開いた p がないので、空の p も生成されます。右がその結果です。ここで、ブラウザの挙動を説明して終わりにせず、コンパイラ内部の AST へ視点を戻してください。旧 Go Compiler にも、不正な入れ子を HTML の解析規則に合わせて組み替える処理がありました。Astro の v7 アップグレードガイドにも、以前のコンパイラは不正な HTML を黙って並べ替えたり組み替えたりしていた、と書かれています。さて、エディタで「p の中に div を書いています」と診断したい。ところが補正後の木には、その親子関係がもうありません。ここでの結論は「補正すると位置情報がすべて消える」ではありません。補正後の親子関係だけを見ても、書かれていた親子関係は分からない、ということです。元の関係を診断するには、補正前の構造か、それを確認できる別の情報が要ります。
-->

---
layout: default
class: code-compact body-center
---

## 保持したい構造は、HTMLの入れ子だけではない

<div class="text-lg opacity-60 mb-3">書かれた構造を保持したい。では、Astroで保持すべき構造は、HTMLの入れ子だけだろうか</div>

<div class="grid grid-cols-2 gap-8">
  <div class="min-w-0">

```astro {*|1,5|2,4|3|3}
<section>
  {visible && (
    <p>{price * quantity}</p>
  )}
</section>
```

  </div>
  <div class="min-w-0 text-lg">
    <div class="border-l-4 border-[#BC52EE] pl-4 py-2 transition-opacity duration-300" :class="$clicks >= 1 ? '' : 'opacity-25'">
      <div class="font-600 text-[#BC52EE]">Template</div>
      <div class="font-mono opacity-60">&lt;section&gt;</div>
      <div class="border-l-4 border-[#0B7BC1] pl-4 py-2 mt-2 transition-opacity duration-300" :class="$clicks >= 2 ? '' : 'opacity-25'">
        <div class="font-600 text-[#0B7BC1]">JavaScript式</div>
        <div class="font-mono opacity-60">{visible && (</div>
        <div class="border-l-4 border-[#A36B09] pl-4 py-2 mt-2 transition-opacity duration-300" :class="$clicks >= 3 ? '' : 'opacity-25'">
          <div class="font-600 text-[#A36B09]">markup</div>
          <div class="font-mono opacity-60">&lt;p&gt;</div>
          <div class="border-l-4 border-[#198755] pl-4 py-2 mt-2 transition-opacity duration-300" :class="$clicks >= 4 ? '' : 'opacity-25'">
            <div class="font-600 text-[#198755]">JavaScript式</div>
            <div class="font-mono opacity-60">{price * quantity}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="mt-5 text-lg text-primary">「どこからどこまでが、何の構文なのか」を区別する必要がある</div>

<Ref href="https://docs.astro.build/en/reference/astro-syntax/#dynamic-html">Dynamic HTML — Astro Docs</Ref>

<!--
前のスライドの続きです。書かれた構造を保持したい。では、Astro で保持すべき構造は、HTML の入れ子だけでしょうか。ここで JSX Like の話が戻ってきます。Astro では、テンプレートの中に JavaScript の式があり、その式の中にマークアップがあり、さらにその中に式を書けます。この例だと、section が Template、visible のかっこが JavaScript 式、p が式の中に書かれたマークアップ、そして price かける quantity がさらにその中に埋め込まれた式です。Template、JavaScript 式、markup、JavaScript 式、と4段重なっている。ここでまだ AST の細かい形式には入りません。伝えたいのは、どこからどこまでが何の構文なのかを区別する必要がある、という点だけです。
-->

---
layout: default
class: body-center
---

## Go版は、式を文字列のまま持っていた

```json
{
  "type": "text",
  "value": "price * quantity"
}
```

<div class="mt-6 text-2xl">ひとまとまりの文字列。code生成では、これをそのまま式として組み込める</div>

<Ref href="https://github.com/withastro/compiler">Go版Compiler</Ref>

<!--
Go 版の公開 AST です。式の中身が price かける quantity という1つの文字列として入っています。Go 版コンパイラの README にも、TextNode が HTML のテキストと JavaScript のソースの両方を表すと書かれています。
ひとまとまりの内容として扱っていて、コード生成ではこれをそのまま JavaScript の式として組み込める。出力を作るだけなら、これで十分でした。
-->

---
layout: default
class: body-center
---

## 式の内部まで分解すると、何が分かるか

```json
{
  "type": "BinaryExpression",
  "operator": "*",
  "left":  { "type": "Identifier", "name": "price" },
  "right": { "type": "Identifier", "name": "quantity" }
}
```

<div class="mt-8 text-2xl text-primary">左辺・演算子・右辺が、それぞれ別のnodeになる</div>

<Ref href="https://github.com/estree/estree">ESTree — JavaScript ASTの表し方を定めた共通仕様</Ref>

<!--
同じ式を JavaScript として解析したものです。ESTree という共通仕様の形式で、BinaryExpression があって、左に price、右に quantity という Identifier がある。左辺の price、演算子の掛ける、右辺の quantity を、それぞれ別の node として区別できます。
-->

---
layout: default
class: body-center
---

## 同じ式の、二つの持ち方

<div class="grid grid-cols-[10rem_1fr_1fr] gap-x-8 gap-y-6 mt-10 text-xl items-baseline">
  <div></div>
  <div class="text-2xl font-600">TextNode</div>
  <div class="text-2xl font-600 text-primary">AST</div>

  <div class="text-[#717781]">持ち方</div>
  <div>文字列ひとまとまり</div>
  <div class="text-primary">種類つきの木</div>

  <div class="text-[#717781]">できること</div>
  <div>そのまま式として出力へ組み込む</div>
  <div class="text-primary">識別子・演算子を個別に扱う</div>

  <div class="text-[#717781]">足りる用途</div>
  <div>code生成</div>
  <div class="text-primary">Editorの診断・補完</div>
</div>

<div class="mt-12 text-2xl text-primary font-600">出力に必要な情報と、ソース解析に必要な情報は違う</div>

<!--
二つを並べます。TextNode は文字列ひとまとまりで、そのまま式として出力へ組み込める。code 生成にはこれで足ります。AST は種類つきの木なので、識別子と演算子を個別に扱える。Editor の診断や補完にはこちらが要る。
言いたいのは、式をそのまま渡せることと、式の内部を個別に調べられることは違う、という点です。出力に必要な情報と、ソース解析に必要な情報は別だということが、ここではっきりします。
-->

---
layout: default
class: code-compact body-center
---

## pirceに波線を引くには、何が必要か

```astro {4}
---
const price = 1200;
const quantity = 3;
---
<p>{pirce * quantity}</p>
```

<div class="text-lg text-primary mt-3">Editorでは、<code>pirce</code> だけを識別して診断を表示したい</div>

<div class="grid grid-cols-2 gap-8 mt-5">
  <div>
    <h3 class="opacity-100 !text-base">3つの別の仕事に分かれる</h3>
    <div class="mt-2 grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-lg">
      <div class="font-600">構文解析</div><div class="opacity-70"><code>pirce</code> が識別子であること</div>
      <div class="font-600">定義との照合</div><div class="opacity-70">この場所から参照できる <code>pirce</code> の定義があるか</div>
      <div class="font-600">位置の対応</div><div class="opacity-70">診断対象が、元の <code>.astro</code> のどの範囲にあるか</div>
    </div>
  </div>
  <div>
    <h3 class="opacity-100 !text-base">ソース位置の意味を、1行の例で確認する</h3>

  <div class="font-mono text-xl mt-3">
    <div>&lt;p&gt;{price * quantity}&lt;/p&gt;</div>
    <div class="flex text-primary h-2">
      <span style="width:4ch"></span>
      <span style="width:5ch" class="border-t-3 border-current"></span>
      <span style="width:3ch"></span>
      <span style="width:8ch" class="border-t-3 border-current"></span>
    </div>
    <div class="flex text-primary mt-1">
      <span style="width:4ch"></span>
      <span style="width:5ch">4..9</span>
      <span style="width:3ch"></span>
      <span style="width:8ch">12..20</span>
    </div>
  </div>

  <div class="text-lg opacity-60 mt-3">オフセットが分かれば、元のソースを取り出せる</div>
  </div>
</div>

<!--
前のスライドと同じ式で、price を pirce と書き間違えてみます。エディタでは、pirce だけに波線を引きたい。ここで注意したいのは、ESTree 形式の AST にすれば、それだけで未定義変数を診断できるわけではない、ということです。仕事は3つに分かれます。ひとつめ、構文解析。pirce が識別子であることを知る。ふたつめ、定義との照合。この場所から参照できる pirce の定義があるかどうかを調べる。みっつめ、位置の対応。診断の対象が、元の .astro のどの範囲にあたるかを求める。右がその位置の意味です。開始と終了のオフセットが分かれば、元のソースの該当部分を取り出せる。実際の方法はツールごとに違って、JavaScript の AST を自前で組み立てるものもあれば、convertToTSX で生成した TSX とソース位置の対応を使うものもあります。この3つを別の仕事として見ておくと、あとで「誰がどこまで受け持つか」の話につながります。
-->

---
layout: default
class: code-compact body-center
---

<div class="text-sm uppercase tracking-widest text-[#717781]">合流</div>

## 完成したコードだけを扱えばよいわけではない

<div class="grid grid-cols-2 gap-x-8 gap-y-4 mt-4">
  <div class="min-w-0">
    <div class="text-primary font-600 text-lg">空白</div>

```html
<b>Hello</b> <b>world</b>
<b>Hello</b><b>world</b>
```

  <div class="opacity-70 text-lg">空白や改行を、どの範囲まで保持するか</div>
  </div>
  <div class="min-w-0">
    <div class="text-primary font-600 text-lg">コメント</div>

```astro
<!-- 合計金額を表示 -->
<p>{price * quantity}</p>
```

  <div class="opacity-70 text-lg">コメントの内容と位置を、どう保持するか</div>
  </div>
  <div class="min-w-0">
    <div class="text-primary font-600 text-lg">不完全な入力</div>

```astro
<p>{price * }</p>
```

  <div class="opacity-70 text-lg">書きかけや構文エラーがあるときも、どこまで解析を続けられるか</div>
  </div>
  <div class="min-w-0 text-lg">
    <div class="text-primary font-600">それらを保持する表現</div>
    <div class="opacity-70 mt-2">ASTに情報を付加する方法と、<span class="text-primary">Lossless CST</span> のような表現を比較する</div>
    <div class="opacity-60 mt-2">rust-analyzerやBiomeが採っている形</div>
  </div>
</div>

<div class="mt-5 text-xl text-primary font-600">実行できるコードだけでなく、編集途中のコードも扱うための情報が必要になる</div>

<Ref>
  <a href="https://biomejs.dev/internals/architecture/">Biome — Architecture</a>
  <a href="https://github.com/withastro/compiler/blob/main/packages/compiler/src/shared/ast.ts" class="ml-8">Go版Compiler の AST 型定義</a>
</Ref>

<!--
ここでさらに視点を広げます。扱う対象は、完成したコードだけではありません。書いている途中のソースも入ってきます。左上が空白。要素の間に空白があるかないかで表示が変わるので、どの範囲まで保持するかを決めないといけない。右上がコメント。内容と位置をどう保持するか。整形したときにコメントが迷子にならないように。左下が不完全な入力。書きかけや構文エラーがあるときも、どこまで解析を続けられるか。そして右下が、それらを保持する表現です。ここで気をつけたいのは、AST では無理だから CST にする、という結論にしないことです。旧 Astro の AST にも、コメントのノードや位置情報の定義はあります。大事なのは名前ではなく、必要な情報をどこまで保持できるか。もうひとつ、ソースを欠落なく保持する設計と、構文エラーから回復して解析を続ける設計は別の観点です。Biome の説明でも、CST で空白やコメントを保持することと、パーサのエラー回復は分けて書かれています。このスライドの結論は、木の種類の優劣ではありません。実行できるコードだけでなく、編集途中のコードも扱うための情報が必要になる、ということです。
-->

---
layout: default
class: body-center
---

## 3つの設計判断

<div class="mt-12 grid grid-cols-[auto_1fr] gap-x-10 gap-y-6 text-xl items-baseline">
  <div class="text-2xl font-600 text-primary whitespace-nowrap">何を保持するか</div>
  <div class="opacity-70">元の入れ子、ソース位置、式の内部、空白、コメント、不完全な入力</div>
  <div class="text-2xl font-600 text-primary whitespace-nowrap">いつ補正するか</div>
  <div class="opacity-70">読み取る段階で構造を組み替えるのか、元の構造を残して後段で扱うのか</div>
  <div class="text-2xl font-600 text-primary whitespace-nowrap">誰がどこまで受け持つか</div>
  <div class="opacity-70">構文の解析、定義との照合、診断、コード生成、Browserによる解釈</div>
</div>

<!--
ここでは新しい技術も図も足しません。ここまでの個別の困りごとを、3つの設計判断へまとめます。
何を保持するか。元の入れ子、ソース位置、式の内部、空白、コメント、不完全な入力。ここまでの具体例で出てきたものが、全部ここに入ります。
いつ補正するか。読み取る段階で構造を組み替えるのか、元の構造を残して後段で扱うのか。div の例がこれでした。
誰がどこまで受け持つか。構文の解析、定義との照合、診断、コード生成、ブラウザによる解釈。pirce の例で、3つの別の仕事に分かれることを見ました。
この3つを覚えておいてください。第4章の「判断の軸」で、答えが出ます。
-->

---
layout: default
class: body-center
---

## 出力に求めることと、ソースの扱いに求めること

<div class="grid grid-cols-2 gap-10 mt-10 text-xl">
  <div>
    <div class="text-2xl font-600 text-[#A36B09]">Output contract</div>
    <div class="mt-3">生成されたコードを、後段が期待どおりに利用できること</div>
    <ul class="mt-4 text-lg opacity-70">
      <li>実行したときの振る舞い</li>
      <li>生成されるHTMLと、その表示結果</li>
      <li>出力先が期待する形式</li>
    </ul>
  </div>
  <div>
    <div class="text-2xl font-600 text-[#0B7BC1]">Source contract</div>
    <div class="mt-3">書かれたコードを、ツールが必要な精度で調べられること</div>
    <ul class="mt-4 text-lg opacity-70">
      <li>元の入れ子とソース位置</li>
      <li>式の内部構造と、元ソースとの対応</li>
      <li>空白、コメント、不完全な入力の扱い</li>
    </ul>
  </div>
</div>

<!--
ここで初めて、ここまでの要求に名前を付けます。Output contract は、生成されたコードを後段が期待どおりに利用できること。実行したときの振る舞い、生成される HTML と表示結果、出力先が期待する形式。これは最初からあった契約です。Source contract は、書かれたコードをツールが必要な精度で調べられること。元の入れ子とソース位置、式の内部構造と元ソースとの対応、空白とコメントと不完全な入力の扱い。こちらは後から明確になった契約です。誤解してほしくないのは、これは Build だけの要求と Editor だけの要求に完全に分離する図ではない、ということです。要求の対象を分けている。前のスライドが「何を判断するか」で、こちらが「その判断によって何を保証するか」です。
-->

---
layout: default
class: body-center
---

## この章の結論

<div class="mt-20 text-4xl leading-relaxed text-primary font-600">
  何を生成するかだけでなく、<br />何を保持し、いつ変換し、誰が扱うかを設計し直す
</div>

<!--
第2章の結論です。HTML の入れ子から始まって、言語の入れ子、式の内部、元ソース上の位置、編集途中の情報まで、保持すべき情報の範囲がだんだん広がってきました。その帰結がこの一行です。何を生成するかだけでなく、何を保持し、いつ変換し、誰が扱うかを設計し直す。HTML5 parser の挙動からは、書かれた構造とソース位置を保持する必要が出てきた。JSX like からは、式の内部を AST として提供する必要が出てきた。そして3つとも共通して、空白もコメントも落とさない木が必要になった。それともうひとつ、現実的な事情として、Astro のメンバーには Go のスペシャリストが少ないという話もあります。
-->

---
layout: statement
class: flex flex-col justify-center h-full
---

# 2026年にはどうなっていたか

<!--
では、こうした要求に応えるために、2026年には何を利用できるようになっていたのか。第3章です。
-->

---
layout: section
---

# 3. 前提の変化
## 2026年までに周囲はどう変わったのか

<!--
第3章。解決策を決める前に、選択肢がどう増えたのかを整理します。
-->

---
layout: default
class: body-center
---

## Rust製ツールが、実用的な基盤へ育った

<div class="grid grid-cols-4 gap-10 mt-20 text-center">
  <div><logos-swc class="h-20 w-full" /></div>
  <div><logos-biomejs class="h-20 w-full" /></div>
  <div><logos-oxc class="h-20 w-full" /></div>
  <div><logos-rolldown class="h-20 w-full" /></div>
</div>

<div class="mt-16 text-2xl opacity-70">2021年にも存在した基盤が育ち、その後の新しい実装も加わった</div>

<Ref href="https://oxc.rs/docs/guide/introduction.html">SWC と Biome と Oxc</Ref>

<!--
Rust 製のツールが実用的な基盤へ育ちました。SWC は JavaScript と TypeScript の変換基盤。Biome は検査と整形のツールチェーン。Oxc は解析と変換のツール群で、Linter の Oxlint と Formatter の Oxfmt を提供しています。Rolldown は Rust 製のバンドラ。2021年にも存在していたものが育ち、その後の新しい実装も加わりました。
-->

---
layout: default
class: body-center
---

## 再利用できる処理が増えた

<div class="flex flex-wrap justify-center gap-x-12 gap-y-10 mt-12 text-center">
  <div class="w-40">
    <div class="text-2xl font-600">Parser</div>
    <div class="flex items-start justify-center gap-7 mt-4">
      <div class="flex flex-col items-center gap-2">
        <logos-oxc-icon class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">Oxc</span>
      </div>
      <div class="flex flex-col items-center gap-2">
        <logos-swc class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">SWC</span>
      </div>
    </div>
  </div>
  <div class="w-40">
    <div class="text-2xl font-600">Transformer</div>
    <div class="flex items-start justify-center gap-7 mt-4">
      <div class="flex flex-col items-center gap-2">
        <logos-swc class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">SWC</span>
      </div>
      <div class="flex flex-col items-center gap-2">
        <logos-esbuild class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">esbuild</span>
      </div>
    </div>
  </div>
  <div class="w-40">
    <div class="text-2xl font-600">Resolver</div>
    <div class="flex items-start justify-center gap-7 mt-4">
      <div class="flex flex-col items-center gap-2">
        <logos-oxc-icon class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">Oxc</span>
      </div>
      <div class="flex flex-col items-center gap-2">
        <logos-vitejs class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">Vite</span>
      </div>
    </div>
  </div>
  <div class="w-40">
    <div class="text-2xl font-600">Bundler</div>
    <div class="flex items-start justify-center gap-7 mt-4">
      <div class="flex flex-col items-center gap-2">
        <logos-rollupjs class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">Rollup</span>
      </div>
      <div class="flex flex-col items-center gap-2">
        <logos-rolldown-icon class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">Rolldown</span>
      </div>
    </div>
  </div>
  <div class="w-40">
    <div class="text-2xl font-600">Minifier</div>
    <div class="flex items-start justify-center gap-7 mt-4">
      <div class="flex flex-col items-center gap-2">
        <logos-esbuild class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">esbuild</span>
      </div>
      <div class="flex flex-col items-center gap-2">
        <logos-oxc-icon class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">Oxc</span>
      </div>
    </div>
  </div>
  <div class="w-40">
    <div class="text-2xl font-600">Linter</div>
    <div class="flex items-start justify-center gap-7 mt-4">
      <div class="flex flex-col items-center gap-2">
        <logos-biomejs-icon class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">Biome</span>
      </div>
      <div class="flex flex-col items-center gap-2">
        <logos-eslint class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">ESLint</span>
      </div>
    </div>
  </div>
  <div class="w-40">
    <div class="text-2xl font-600">Formatter</div>
    <div class="flex items-start justify-center gap-7 mt-4">
      <div class="flex flex-col items-center gap-2">
        <logos-biomejs-icon class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">Biome</span>
      </div>
      <div class="flex flex-col items-center gap-2">
        <logos-prettier class="w-14 h-14" />
        <span class="text-base text-[#6B7280]">Prettier</span>
      </div>
    </div>
  </div>
</div>

<div class="mt-12 text-2xl text-primary">
  処理の単位で、実際に使える実装が出そろった
</div>

<!--
重要なのは、ツールが増えただけでなく、処理の単位で再利用できるようになったことです。パーサ、トランスフォーマ、リゾルバ、バンドラ、ミニファイア、リンタ、フォーマッタ。完成したツールとして使えるものに加えて、ライブラリとして自分の実装に組み込める部品が増えました。各プロジェクトが、必要な処理を既存の基盤と組み合わせられるようになった。
-->

---
layout: default
class: body-center
---

## Bundlerが変わった

<div class="grid grid-cols-[1fr_auto_1fr] items-center gap-10 mt-16 text-center">
  <div>
    <div class="text-2xl font-600 mb-8">Vite 2</div>
    <div class="flex items-center justify-center gap-10">
      <div><logos-esbuild class="w-16 h-16" /><div class="text-xl mt-4">esbuild</div></div>
      <div><logos-rollupjs class="w-16 h-16" /><div class="text-xl mt-4">Rollup</div></div>
    </div>
  </div>
  <div class="text-5xl text-primary">→</div>
  <div>
    <div class="text-2xl font-600 mb-8">Vite 8</div>
    <div><logos-rolldown class="w-56 h-16" /><div class="text-xl mt-4">Rolldown</div></div>
  </div>
</div>

<div class="mt-16 text-2xl opacity-70">
  フレームワークの外で、汎用的なBuild基盤が育った
</div>

<Ref href="https://vite.dev/blog/announcing-vite8">Announcing Vite 8</Ref>

<!--
ビルドの中身も変わりました。Vite 2 の頃は、開発時の事前バンドルに Go 製の esbuild、本番のバンドルに Rollup、と2つに分かれていました。Vite 8 では Rust 製の Rolldown がバンドラになり、それが統合されました。ここで言いたいのは、フレームワークの外で汎用的なビルド基盤が育ったということです。だから Astro は、自分の構文変換と、ビルド全体の処理を分けて考えられる。
-->

---
layout: default
class: body-center
---

## JavaScriptからRustを利用する方法

<div class="grid grid-cols-2 gap-8 mt-4">
  <div>

```rust
use napi_derive::napi;

#[napi]
pub fn multiply(price: u32, quantity: u32) -> u32 {
    price * quantity
}
```

  </div>
  <div>

```js
const { multiply } = require("./index.js");
console.log(multiply(1200, 3)); // 3600
```

  <div class="opacity-60 text-lg mt-3">この <code>index.js</code> は、ビルド時に生成する JavaScript の読み込み口</div>
  </div>
</div>

<div class="grid grid-cols-3 gap-6 mt-8 text-lg">
  <div><b>Node.js bindings</b><div class="opacity-60">JavaScriptとネイティブ実装を接続する部分</div></div>
  <div><b>Node-API</b><div class="opacity-60">Node.jsからネイティブ実装を利用するためのAPI。N-APIとも呼ばれる</div></div>
  <div><b>napi-rs</b><div class="opacity-60">Rustの関数を、Node.jsから呼び出せるようにするための仕組み</div></div>
</div>

<Ref href="https://napi.rs/docs/introduction/simple-package">napi-rs — Simple package</Ref>

<!--
JavaScript から Rust を使う方法です。これは呼び出しの仕組みだけを示す例で、Astro の実装そのものではありません。Rust の関数に napi の属性を付けると、JavaScript から普通の関数として呼べるようになります。用語を3つ。Node.js bindings が接続部分、Node-API がそのための API、napi-rs が Rust 向けにそれを扱いやすくする仕組みです。
-->

---
layout: default
class: body-center
---

## 実装する言語と、配布する方法を分ける

<div class="grid grid-cols-3 gap-6 mt-8 text-lg">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-2xl font-600">ネイティブバイナリ</div>
    <div class="opacity-65 mt-2">OSとCPUに対応した実行形式を配布する。Node.jsから bindings を通じて利用する</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-2xl font-600">WASM</div>
    <div class="opacity-65 mt-2">対応する実行環境で動かせるバイナリ形式。BrowserやNode.jsなどへ配布する選択肢</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-2xl font-600">Rust crate</div>
    <div class="opacity-65 mt-2">Rustの実装へ組み込めるライブラリ。必要な解析や変換の機能を取り込む</div>
  </div>
</div>

<div class="mt-10 text-xl leading-relaxed">
  <p class="opacity-70">Node-APIやWASM自体は、2021年にも存在していた。napi-rs も2021年には bindings や型定義の生成を提供していた</p>
  <p class="text-primary">変わったのは、<b>組み合わせられる実装と配布の選択肢</b></p>
</div>

<Ref href="https://napi.rs/blog/announce-v2">Announcing napi-rs v2</Ref>

<!--
ここは第1章の「分けて考える選択」の続きです。ネイティブバイナリ、WASM、Rust crate。これらは配布と実行の選択肢です。注意したいのは、Node-API も WASM も 2021年に存在していたということ。napi-rs も2021年には v2 が出ています。だから「新しい技術ができたから」ではないんです。変わったのは、組み合わせられる実装と配布の選択肢の幅です。Node.js でどう実行するか、ブラウザへどう配布するか、を用途ごとに検討できるようになった。
-->

---
layout: default
class: body-center
---

## JavaScript解析に使えるOxc

<div class="text-lg opacity-60 mb-2">第2章の式を、もう一度</div>

```js
price * quantity
```

<div class="text-lg opacity-60 mt-6 mb-2">JavaScript から利用する場合</div>

```js
import { parseSync } from "oxc-parser";
const source = "price * quantity";
const { program } = parseSync("example.js", source);
```

<div class="mt-6 text-xl">
  <p class="opacity-70">ソース文字列を渡すと、ASTを取得できる。これは掛け算を実行する処理ではなく、式の構造を解析する処理</p>
  <p class="text-primary">Astro に残ること — 一般的なJavaScript構文と、Astro固有の構文をどう組み合わせるか</p>
</div>

<Ref href="https://oxc.rs/docs/guide/usage/parser.html">Oxc Parser</Ref>

<!--
第2章で「式の内部まで分解した表現が必要だ」という話をしました。それを自前で書く必要はもうありません。Oxc のパーサが JavaScript と TypeScript を解析します。JavaScript から使う場合はこう、Rust の実装に直接ライブラリとして組み込むこともできます。この章では、使える基盤があることまでを示します。Astro に残るのは、一般的な JavaScript 構文と Astro 固有の構文をどう組み合わせるか。具体的な役割分担は第4章で説明します。
-->

---
layout: default
class: body-center
---

## Astro Syntax 自体も整理された

<div class="text-xl opacity-70 mb-4">2026年2月付の構文仕様ドラフト — どのような書き方を、その言語の構文として扱うかを明文化した資料</div>

```astro
---
const name = "Astro";
---
<h1 class="title">{name}</h1>
<p>複数の要素を、そのまま並べられる</p>
```

<div class="grid grid-cols-4 gap-4 mt-8 text-lg">
  <div class="opacity-70">Component script と Template の境界</div>
  <div class="opacity-70">HTMLの属性</div>
  <div class="opacity-70">埋め込まれたJavaScript式</div>
  <div class="opacity-70">複数のルート要素</div>
</div>

<div class="mt-8 text-xl text-primary">
  新しい実装が扱う構文を、共通の資料で確認できる
</div>

<!--
Astro の構文そのものも整理されました。2026年2月付で構文仕様のドラフトが出ています。ファイル全体の構成、JSX との差分、Astro 固有の構文が明文化された。この例で確認できるのは、Component script と Template の境界、HTML の属性、埋め込まれた JavaScript 式、そして複数のルート要素をそのまま並べられること。新しい実装が何を扱うべきかを、共通の資料で確認できるようになりました。ソース位置や不完全な構文への対応は、利用するツールの要求と合わせて設計します。
-->

---
layout: default
class: body-center
---

## Vue.js Amsterdam 2026 — Astro 6の発表

<div class="grid grid-cols-2 gap-10 mt-10 text-xl">
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-sm uppercase tracking-widest text-[#717781]">実装に利用する基盤</div>
    <div class="text-3xl font-600 mt-2">Oxc と Rust</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-sm uppercase tracking-widest text-[#717781]">実装を進めるための開発支援</div>
    <div class="text-3xl font-600 mt-2">Claude Code</div>
  </div>
</div>

<div class="mt-10 text-xl opacity-70">
  関連する試みとして、自分が取り組んでいた <b>xmdx</b> も紹介された
</div>

<!--
Vue.js Amsterdam 2026 で Astro 6 が発表されました。そこでは Oxc と Rust の話、そして Claude Code を使った開発の話が出ました。2つの変化として整理できます。実装に利用する基盤としての Oxc と Rust、実装を進めるための開発支援としての Claude Code。そしてこの発表のなかで、関連する試みとして自分が取り組んでいた xmdx も紹介されました。ここから全体図の Content の経路へ視野を広げます。少し時間を戻して、2025年から自分が取り組んでいた Markdown と MDX の話をします。
-->

---
layout: default
class: body-center
---

## MarkdownとMDXの処理

```mdx
import ProductCard from "./ProductCard.jsx";

# おすすめの商品

今月のおすすめです。

<ProductCard name="Book" price={1200} />
```

<div class="grid grid-cols-3 gap-6 mt-6 text-lg">
  <div><b>Markdown</b><div class="opacity-60">見出しや箇条書きなどを、テキストで記述する形式</div></div>
  <div><b>MDX</b><div class="opacity-60">Markdownの中で、JSXやJavaScriptの式を使える形式</div></div>
  <div><b>Content Processor</b><div class="opacity-60">こうした本文を解析し、表示に使うコードや情報へ変換する処理</div></div>
</div>

<div class="mt-6 text-xl text-primary">
  <code>.astro</code> Compilerとは別の経路で、AstroのBuildへ接続する
</div>

<!--
Markdown と MDX です。MDX は Markdown の中で JSX や JavaScript の式を使える形式で、この例のように文章とコンポーネントの呼び出しが1つのファイルに入ります。これを解析して表示に使うコードへ変換するのが Content Processor。ここが大事なのですが、これは .astro のコンパイラとは別の経路で Astro のビルドに接続します。同じ「Astro を速くする」でも、別の処理系の話です。
-->

---
layout: default
class: body-center
---

## MarkdownとMDXにもRustの基盤があった

<div class="grid grid-cols-2 gap-16 mt-16 text-center">
  <div>
    <div class="flex items-center justify-center gap-5">
      <logos-markdown class="text-6xl" />
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-14" />
    </div>
    <div class="text-3xl font-600 mt-6">markdown-rs</div>
  </div>
  <div>
    <div class="flex items-center justify-center gap-5">
      <logos-mdx class="text-6xl" />
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-14" />
    </div>
    <div class="text-3xl font-600 mt-6">mdxjs-rs</div>
  </div>
</div>

<div class="mt-16 text-2xl text-primary">
  既存の基盤を組み合わせれば、Astroでも使えるのではないか
</div>

<Ref href="https://github.com/wooorm/mdxjs-rs">markdown-rs / mdxjs-rs</Ref>

<!--
Markdown と MDX にも Rust の基盤がありました。markdown-rs が解析の基盤、mdxjs-rs が MDX を JavaScript へ変換するコンパイラです。mdxjs-rs は内部で markdown-rs と SWC を使っています。つまり、既存の基盤を組み合わせれば Astro でも使えるのではないか、と考えました。
-->

---
layout: default
class: body-center
---

## 自分で試したRust製MDX Compiler

<div class="flex items-center gap-4 mb-6">
  <Status kind="poc" />
  <span class="text-xl opacity-70">2025年7月、Astroへ組み込むPoCを提案した</span>
</div>

<div class="grid grid-cols-3 gap-6 text-lg">
  <div>
    <h3 class="opacity-100 !text-base">検証したかったこと</h3>
    <ul class="mt-2">
      <li>Buildが速くなるか</li>
      <li>既存のAstroプロジェクトで使えるか</li>
    </ul>
  </div>
  <div>
    <h3 class="opacity-100 !text-base">互換性を調べたもの</h3>
    <ul class="mt-2">
      <li>frontmatter — ファイル冒頭のタイトルなどの情報</li>
      <li>見出しのslug — 見出しへのリンクに使うID</li>
      <li>画像と Astro component</li>
    </ul>
  </div>
  <div>
    <h3 class="opacity-100 !text-base">最初の案</h3>
    <ul class="mt-2">
      <li>Rustで処理する経路を、利用者が選べるようにする</li>
      <li>対応できない場合は、既存のJavaScript実装へ戻す</li>
    </ul>
  </div>
</div>

<!--
2025年7月に、これを Astro へ組み込む PoC を提案しました。PoC は小さな実装を作って実現できるかを確かめる試みです。検証したかったのはシンプルで、ビルドが速くなるか、そして既存の Astro プロジェクトでそのまま使えるか。frontmatter、見出しの slug、画像、Astro コンポーネント、それぞれの互換性を調べました。最初の案は、Rust で処理する経路を利用者が選べるようにして、対応できない場合は既存の JavaScript 実装へ戻す、というものでした。
-->

---
layout: default
class: body-center
---

## 既存pluginとの接続が必要だった

<div class="mt-10 text-xl opacity-70">既存の処理は remark と rehype の plugin に依存していた</div>

<div class="mt-4 flex flex-wrap gap-4 text-xl">
  <span class="border border-[#E5E0EC] rounded-lg px-5 py-2"><code>remark-gfm</code></span>
  <span class="border border-[#E5E0EC] rounded-lg px-5 py-2"><code>remark-smartypants</code></span>
  <span class="border border-[#E5E0EC] rounded-lg px-5 py-2"><code>rehype-slug</code></span>
</div>

<div class="mt-10 border border-[#BC52EE] border-opacity-45 rounded-xl px-8 py-6" style="background: rgba(188, 82, 238, 0.06)">
  <p class="!my-0 text-3xl font-600">mdxjs-rs では、これらを実行できなかった</p>
</div>

<Ref href="https://github.com/wooorm/mdxjs-rs#when-should-i-use-this">mdxjs-rs — When should I use this?</Ref>

<!--
ここで壁にぶつかりました。既存の処理は remark と rehype の plugin を使っています。GitHub 風の表を扱う remark-gfm、引用符を変換する remark-smartypants、見出しに ID を付ける rehype-slug。ところが検討した mdxjs-rs では、これらの既存 plugin を実行できませんでした。plugin が必要な構成では JavaScript 実装へ戻ることになるので、Rust の経路を使える範囲が限られてしまう。ここで分かったのは、利用者は解析結果だけでなく、途中で plugin を実行できることにも依存している、ということでした。
-->

---
layout: default
class: body-center
---

## AST Bridgeによる分担を試した

<div class="text-xl opacity-70 mb-6">AST Bridge — RustとJavaScriptの間でASTを受け渡し、処理を分担する仕組み</div>

<div class="grid grid-cols-[1fr_auto] gap-10">
  <div>
    <div class="grid grid-cols-[2rem_1fr] gap-x-4 gap-y-3 text-xl">
      <div class="text-primary">1</div><div>RustでMarkdownとMDXを解析する</div>
      <div class="text-primary">2</div><div>必要な段階で、ASTをJavaScriptへ渡す</div>
      <div class="text-primary">3</div><div>既存のremarkとrehypeのpluginで加工する</div>
      <div class="text-primary">4</div><div>加工したASTをRustへ戻し、コード生成につなげる</div>
    </div>
  </div>
  <div class="text-lg">
    <h3 class="opacity-100 !text-base">扱う構造</h3>
    <ul class="mt-2">
      <li><b>mdast</b> — MarkdownのAST</li>
      <li><b>hast</b> — HTMLのAST</li>
    </ul>
  </div>
</div>

<div class="mt-8 text-xl">
  <p class="text-primary">RustとJavaScriptを、処理ごとに使い分けられる</p>
  <p class="opacity-70">ASTを受け渡す境界も、設計する必要がある</p>
</div>

<!--
そこで AST Bridge という分担を試しました。Rust で解析して、必要な段階で AST を JavaScript へ渡し、既存の remark と rehype の plugin で加工して、加工した AST を Rust へ戻してコード生成につなげる。扱う構造は Markdown の AST である mdast と、HTML の AST である hast です。試して分かったのは、Rust と JavaScript を処理ごとに使い分けられるということ。同時に、AST を受け渡す境界そのものも設計しないといけない、ということでした。
-->

---
layout: default
class: body-center
---

## 開発元への提案

<div class="grid grid-cols-2 gap-8 mt-4 text-lg">
  <div>
    <h3 class="opacity-100 !text-base">markdown-rs へ</h3>
    <ul class="mt-2">
      <li>GFMの表を、ASTからMarkdownへ戻す処理</li>
      <li>JavaScript環境から利用するためのWASM bindings</li>
    </ul>

```markdown
| 商品 | 価格 |
| --- | ---: |
| Book | 1200 |
| Pen | 200 |
```

  </div>
  <div>
    <h3 class="opacity-100 !text-base">mdxjs-rs へ</h3>
    <ul class="mt-2">
      <li>公式npm package</li>
      <li>Node.jsから利用するためのnative bindings</li>
    </ul>
    <div class="border border-[#E5E0EC] rounded-xl p-5 mt-6">
      <p class="text-lg">解析する処理に加えて、加工した構造を<br /><b>再びMarkdownへ書き出す</b>処理も必要になる</p>
      <p class="text-lg opacity-70 mt-3">Astroなどの利用者が、それぞれ接続部分を実装しなくてもよい形を目指した</p>
    </div>
  </div>
</div>

<!--
upstream、つまり自分たちが使っているライブラリの開発元へも提案しました。markdown-rs には、GFM の表を AST から Markdown へ戻す処理と、JavaScript 環境から使うための WASM bindings。表の例が左下にあります。解析するだけでなく、加工した構造をもう一度 Markdown へ書き出す処理が必要になるんです。mdxjs-rs には、公式の npm パッケージと Node.js 向けの native bindings。Astro のような利用者が、それぞれ接続部分を自前で実装しなくてよい形を目指しました。
-->

---
layout: default
class: body-center
---

## communityとのやりとりで見えた条件

<div class="grid grid-cols-2 gap-x-10 gap-y-5 mt-8 text-xl">
  <div>
    <div class="text-primary font-600">配布方法</div>
    <div class="opacity-65 text-lg">WASMとNode-APIのどちらを使うか。両方に対応するか</div>
  </div>
  <div>
    <div class="text-primary font-600">対応環境</div>
    <div class="opacity-65 text-lg">OSとCPUごとのバイナリを誰がビルドし、誰がテストして保守するか</div>
  </div>
  <div>
    <div class="text-primary font-600">依存関係</div>
    <div class="opacity-65 text-lg">追加機能を全員に含めるか、必要な利用者だけが追加する形にするか</div>
  </div>
  <div>
    <div class="text-primary font-600">pluginとの互換性</div>
    <div class="opacity-65 text-lg">既存のpluginを、どこまで利用できるようにするか</div>
  </div>
  <div class="col-span-2">
    <div class="text-primary font-600">汎用部分の担当</div>
    <div class="opacity-65 text-lg">Astro本体が持つか、開発元や独立したprojectが持つか</div>
  </div>
</div>

<div class="mt-8 text-2xl text-primary">実装を試すことで、速度以外の成立条件が具体的になった</div>

<!--
コミュニティとのやりとりで、速度以外の条件が次々に出てきました。配布方法は WASM と Node-API のどちらか、あるいは両方か。OS と CPU ごとのバイナリを誰がビルドし、誰がテストして保守するのか。追加機能を全員の依存に含めるのか、必要な人だけが追加する形にするのか。既存 plugin をどこまで使えるようにするのか。そして汎用部分を Astro 本体が持つのか、開発元や独立したプロジェクトが持つのか。実装を試したからこそ、こういう条件が具体的になりました。
-->

---
layout: default
class: body-center
---

## xmdxとして続けた検証

<div class="flex items-center gap-4 mb-5">
  <Status kind="poc" />
  <span class="text-xl opacity-70">Astroのレビューを受け、汎用的なMarkdownとMDXの処理を独立したprojectとして実装した</span>
</div>

<div class="grid grid-cols-2 gap-8 text-lg">
  <div>
    <h3 class="opacity-100 !text-base">作ったもの</h3>
    <ul class="mt-2">
      <li>Rustの処理を、Node-APIとWASMでJavaScriptから利用できるようにした</li>
      <li>AstroとStarlight向けの integration</li>
      <li>ネイティブ実装、WASM、Astroとの接続を別のpackageとして扱った</li>
    </ul>
  </div>
  <div>
    <h3 class="opacity-100 !text-base">実際のAstro Docsを使って検証した</h3>
    <ul class="mt-2">
      <li>既存のコンテンツを処理できるか</li>
      <li>表示や機能の互換性を保てるか</li>
      <li>Build時間がどう変わるか</li>
    </ul>
  </div>
</div>

<Ref href="https://github.com/jp-knj/xmdx">xmdx</Ref>

<!--
Astro のレビューを受けて、汎用的な Markdown と MDX の処理を独立したプロジェクトとして実装しました。xmdx です。Rust の処理を Node-API と WASM の両方で JavaScript から使えるようにして、Astro と Starlight 向けの integration を作りました。integration は Astro へ機能を組み込むための接続部分、Starlight は Astro を使ったドキュメントサイト向けの仕組みです。ここでもネイティブ実装、WASM、Astro との接続を別のパッケージに分けています。検証は実際の Astro Docs を使いました。既存のコンテンツを処理できるか、表示や機能の互換性を保てるか、ビルド時間がどう変わるか。
-->

---
layout: default
class: body-center
---

## 複数の試みを比較できるようになった

<div class="flex gap-4 mt-6 text-2xl">
  <span class="border border-[#E5E0EC] rounded-lg px-4 py-1">xmdx</span>
  <span class="border border-[#E5E0EC] rounded-lg px-4 py-1">ox-content</span>
  <span class="border border-[#BC52EE] border-opacity-60 rounded-lg px-4 py-1 text-primary">Sätteri</span>
</div>

<div class="grid grid-cols-2 gap-x-10 gap-y-6 mt-12 text-2xl">
  <div><b>実際のBuildでの速度</b></div>
  <div><b>plugin model</b></div>
  <div><b>frameworkとの境界</b></div>
  <div><b>保守主体</b></div>
</div>

<div class="mt-8 text-xl text-primary">自分の試作とcommunityとの対話が、選ぶための判断材料になった</div>

<!--
xmdx に加えて、ox-content などの Rust 製 Content 基盤についてもコミュニティで話しました。Sätteri も、要求に合う基盤を考えるうえでの選択肢になりました。比較できるようになったのは4点。実際のビルドでの速度、plugin がどの段階のどのデータを加工できるかという plugin model、Astro と Content 基盤の境界、そして誰が保守するのか。自分の試作とコミュニティとの対話が、選ぶための判断材料になりました。なぜ Sätteri を勧めるに至ったかは、第4章で説明します。
-->

---
layout: center
---

<Overview
  subs="parser,oxc"
  :annotate="{
    compiler: 'Oxcなどの再利用できる基盤',
    content: 'markdown-rs と mdxjs-rs、そして xmdx と ox-content と Sätteri',
  }"
/>

<!--
全体図に候補を添えます。JavaScript 解析の周囲には Oxc などの再利用できる基盤。ビルドの周囲には Vite と Rolldown。Content の周囲には解析と変換の基盤として markdown-rs と mdxjs-rs、Content 処理の選択肢として xmdx、ox-content、Sätteri。JavaScript とネイティブ実装の境界には Node-API と WASM の経路。そして Astro Syntax を確認する資料として構文仕様のドラフト。この図では、各領域の周囲に候補を添えているだけで、すべてを採用した図にはしていません。ライブラリと、それを組み込んだ Processor は区別してください。
-->

---
layout: default
class: body-center
---

## 2021年から変わった判断材料

<div class="mt-8 text-xl leading-relaxed">
  <ul>
    <li>実装に利用できる <b>Rustの基盤</b> が増えた</li>
    <li>JavaScriptから利用できる <b>packageや配布の選択肢</b> が増えた</li>
    <li>ソースの構造を扱う <b>ツールの要求</b> が明確になった</li>
    <li><b>Astro Syntax を確認する資料</b> が整った</li>
    <li>MarkdownとMDXでも、<b>実装を試して比較</b> できるようになった</li>
    <li>Node.jsでの実行方法とBrowserへの配布方法を、<b>用途ごとに検討</b> できる</li>
  </ul>
</div>

<!--
2021年から変わった判断材料をまとめます。実装に使える Rust の基盤が増えた。JavaScript から使えるパッケージと配布の選択肢が増えた。ソースの構造を扱うツールの要求が明確になった。Astro Syntax を確認する資料が整った。Markdown と MDX でも実装を試して比較できるようになった。そして実行方法と配布方法を用途ごとに検討できるようになった。
-->

---
layout: default
class: body-center
---

## この章の結論

<div class="mt-12 text-2xl leading-relaxed">
  <p>2021年の判断を支えていた条件が、5年間で変わった</p>
  <p>新しい要求に対して、再利用できる基盤と資料が増えた</p>
  <p class="text-primary">自分で試作し、communityと話すことで、選択肢を評価する条件も分かった</p>
</div>

<!--
第3章の結論です。2021年の判断を支えていた条件が、5年間で変わりました。新しい要求に対して、再利用できる基盤と資料が増えた。そして自分で試作してコミュニティと話すことで、選択肢を評価するための条件も分かりました。
-->

---
layout: statement
class: flex flex-col justify-center h-full
---

# その選択肢を使って、<br />Astroは何を自分たちで実装し、<br />何を既存の基盤に任せるのか

<!--
では、その選択肢を使って、Astro は何を自分たちで実装し、何を既存の基盤に任せるのか。第4章です。
-->

---
layout: section
---

# 4. 新しい判断
## その結果、責務をどう分け直したのか

<!--
第4章。ここからは、責務をどう分け直したのかを見ていきます。
-->

---
layout: center
---

<Overview
  subs="parser,oxc,astro-syntax"
  :roles="{
    editor: 'ソースの情報を、診断や補完につなげる',
    build: '変換されたコードをまとめ、実行や配信につなげる',
    content: 'MarkdownとMDXの解析と変換',
  }"
/>

<!--
先に結論の図を出します。各領域が何を担当するか。Astro Compiler は Astro 固有の構文と変換、そしてその中の汎用的な解析には Oxc を使う。Build は変換されたコードをまとめて実行や配信につなげる。Editor のツールはソースの情報を診断や補完につなげる。Content Processor は Markdown と MDX の解析と変換。ブラウザは出力された HTML を解釈して DOM を構築する。
-->

---
layout: default
class: body-center
---

## 判断の軸

<div class="grid grid-cols-2 gap-x-10 gap-y-6 mt-12 text-2xl">
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">どのソース情報を保持するか</div>
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">どの段階で補正や変換を行うか</div>
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">一般的な処理を、どの基盤へ任せるか</div>
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">Astroが、どの処理を実装して保守するか</div>
</div>

<!--
判断の軸は4つです。どのソース情報を保持するか。どの段階で補正や変換を行うか。一般的な処理をどの基盤へ任せるか。そして Astro がどの処理を実装して保守するか。この4つで、HTML、JavaScript、Markdown と MDX の3つの具体例を見ていきます。
-->

---
layout: default
class: body-center
---

## HTMLの例へ戻る — verbatim parsing

```html
<p>before<div>inside</div>after</p>
```

<div class="grid grid-cols-2 gap-8 mt-6 text-lg">
  <div>
    <h3 class="opacity-100 !text-base">ソースを解析する段階の役割</h3>
    <ul class="mt-2">
      <li>ユーザーが何を書いたかを把握する</li>
      <li>書かれた入れ子とソース位置を保持する</li>
    </ul>
    <h3 class="opacity-100 !text-base mt-5">verbatim parsing</h3>
    <ul class="mt-2">
      <li>書かれた構造に沿って解析する方針</li>
      <li>この例では <code>div</code> を <code>p</code> の子として保持する</li>
      <li>ソースに存在しない空の <code>p</code> を追加しない</li>
    </ul>
  </div>
  <div class="flex flex-col justify-center">
    <div class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
      <p class="text-xl">書かれた構造を保持することと、<br />そのHTMLが正しいことは別</p>
      <p class="text-lg opacity-70 mt-3"><code>p</code> の中の <code>div</code> という問題は残っている。保持した構造を使って、問題のある位置を調べられる</p>
    </div>
  </div>
</div>

<!--
第2章で見た例に戻ります。ここで決めたのは、ソースを解析する段階の役割です。ユーザーが何を書いたかを把握し、書かれた入れ子とソース位置を保持する。これを verbatim parsing と呼びます。この例では div を p の子として保持し、ソースに存在しない空の p を追加しません。誤解してほしくないのは、書かれた構造を保持することと、その HTML が正しいことは別だということ。p の中の div という問題は残っています。むしろ保持した構造があるから、問題のある位置を調べられる。
-->

---
layout: default
class: body-center
---

## Compilerが受け入れないものもある

<div class="mt-10 text-2xl leading-relaxed">
  <p>Rust版Compilerでは、<b>HTML correctionを行わない</b>方針が明示されている</p>
  <p class="opacity-70">一方、閉じ忘れたタグなどの構文エラーは拒否する</p>
  <p class="text-primary">どんな入力でも受け入れる、という意味ではない</p>
</div>

<Ref href="https://github.com/withastro/roadmap/issues/1356">withastro/roadmap#1356 — 新Compilerの正式提案</Ref>

<!--
補足です。Rust 版コンパイラでは HTML correction を行わない方針が明示されています。ただし、閉じ忘れたタグなどの構文エラーは拒否します。何でも受け入れるという意味ではありません。
-->

---
layout: default
class: body-center
---

## CompilerのASTと、BrowserのDOMを分ける

<div class="grid grid-cols-2 gap-8 mt-8 text-xl">
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Compiler内部のAST</div>
    <ul class="mt-3 text-lg">
      <li>ソースの構文を表すデータ</li>
      <li>解析や変換、ツールとの連携に使う</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Browserが構築するDOM</div>
    <ul class="mt-3 text-lg">
      <li>出力されたHTMLを読み込んで作る構造</li>
      <li>表示やJavaScriptからの操作に使う</li>
    </ul>
  </div>
</div>

<div class="mt-8 text-xl leading-relaxed">
  <p class="opacity-70">同じ入れ子のHTMLをBrowserへ渡せば、BrowserではHTMLの規則に従って補正が起きる</p>
  <p class="text-primary">HTMLの補正方針は、GoかRustかとは別の設計判断</p>
</div>

<!--
ここで分け直したのは3つの段階です。ソースを理解する段階、コードを生成する段階、そして HTML から DOM を構築する段階。同じ入れ子の HTML をブラウザへ渡せば、ブラウザでは HTML の規則に従って補正が起きます。それでいい。大事なのは、HTML の補正方針は Go か Rust かとは別の設計判断だということです。言語を変えたから補正をやめたのではなく、責務を分け直した結果です。
-->

---
layout: default
class: code-compact body-center
---

## JavaScriptの内部構造を、ASTとして渡す

<div class="grid grid-cols-[1fr_1.35fr] gap-6 mt-8">
  <div class="min-w-0">
    <div class="font-600 text-xl mb-2">Go版 — 文字列として渡す</div>

```json
{
  "type": "text",
  "value": "price * quantity"
}
```

  <div class="mt-3 text-base">
    <p class="!my-1">この情報から、式のソースを取り出せる</p>
    <p class="!my-1 opacity-70">識別子として扱うには追加の解析が必要</p>
  </div>
  </div>
  <div>
    <div class="text-primary font-600 text-xl mb-2">Rust版 — <code>parse()</code> が ESTree互換のASTを返す</div>

```json
{
  "type": "BinaryExpression",
  "operator": "*",
  "left":  { "type": "Identifier",
             "name": "price" },
  "right": { "type": "Identifier",
             "name": "quantity" }
}
```

  <div class="mt-3 text-base">
    <p class="!my-1 text-primary">式や変数名を、種類の分かるデータとして扱える</p>
    <p class="!my-1 opacity-60">周囲の Astro Syntax と位置情報は省いた抜粋</p>
  </div>
  </div>
</div>

<Ref href="https://github.com/withastro/compiler-rs">Rust版Compiler README</Ref>

<!--
JavaScript の例に戻ります。左が Go 版。式の子にある TextNode がソース文字列を持っていて、ここから式のソースは取り出せる。でも price と quantity を個別の識別子として扱うには、追加の解析が必要でした。右が Rust 版です。parse() が ESTree 互換の AST を提供します。ESTree は JavaScript の構文を共通の形式で表すための取り決めなので、式や変数名を種類の分かるデータとして扱えます。
-->

---
layout: default
class: body-center
---

## ツールから見た変化と、Editor に残る処理

<div class="grid grid-cols-2 gap-8 mt-8 text-lg">
  <div class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
    <h3 class="opacity-100 !text-base">ツールから見た変化</h3>
    <ul class="mt-2">
      <li>式の左辺と右辺をたどれる</li>
      <li>演算子と識別子を個別に扱える</li>
      <li>JavaScript ASTを扱うツールと接続しやすくなる</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <h3 class="opacity-100 !text-base">Editor には、引き続き必要な処理がある</h3>
    <ul class="mt-2">
      <li>変数の宣言と使用箇所を対応させる</li>
      <li>型情報を調べる</li>
      <li>Astro固有構文とソース位置を扱う</li>
      <li>不完全な入力を扱う</li>
    </ul>
  </div>
</div>

<div class="mt-8 text-xl text-primary">ASTの提供は、診断や補完を作るための基盤になる</div>

<!--
ツールから見た変化です。式の左辺と右辺をたどれる。演算子と識別子を個別に扱える。JavaScript の AST を扱う既存のツールと接続しやすくなる。ただし、これで Editor の仕事がなくなるわけではありません。変数の宣言と使用箇所の対応、型情報、Astro 固有構文とソース位置、不完全な入力。これらは引き続き Editor の仕事です。AST の提供は、診断や補完を作るための基盤になる、ということです。
-->

---
layout: default
class: body-center
---

## Oxcとの責務分担

<div class="grid grid-cols-2 gap-8 mt-8 text-xl">
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Oxcへ任せる部分</div>
    <ul class="mt-3 text-lg">
      <li>JS と TS の解析</li>
      <li>式と識別子のAST</li>
      <li>汎用的な変換とコード生成</li>
    </ul>
  </div>
  <div class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
    <div class="text-2xl font-600">Astroが持つ部分</div>
    <ul class="mt-3 text-lg">
      <li>Astro固有の構文</li>
      <li>Template と JS の混在</li>
      <li>実行に必要な変換</li>
      <li>元のソースとの対応</li>
    </ul>
  </div>
</div>

<div class="mt-10 text-2xl">
  Rust版は、<b>Astro向けに拡張した Oxc</b> を利用する
</div>

<Ref href="https://github.com/withastro/compiler-rs/blob/main/Cargo.toml">compiler-rs — Cargo.toml</Ref>

<!--
Oxc との責務分担です。Oxc に任せるのは、JavaScript と TypeScript の解析、式や識別子を表す AST、汎用的な変換やコード生成の基盤。Astro が持つのは、Astro 固有の構文、Template と JavaScript が混在する部分、Astro の実行に必要な変換、そして元のソースとの対応。Rust 版コンパイラは Astro 向けに拡張した Oxc を使っています。汎用部分を再利用しながら、必要な変更を加える。自分たちで実装して保守する範囲を絞るという判断です。
-->

---
layout: center
---

<Overview
  highlight="compiler,editor,browser,parser,oxc,astro-syntax"
  subs="parser,oxc,astro-syntax"
  :annotate="{
    'compiler->editor': '書かれた構造とソース位置、埋め込まれたJavaScriptのAST',
    browser: '出力HTMLからDOMを構築',
  }"
/>

<div class="text-center text-2xl text-primary mt-2">Compilerを「less clever」にする</div>

<!--
全体図に戻ります。コンパイラと Editor の間には、書かれた構造とソース位置、そして埋め込まれた JavaScript の AST。コンパイラの中には、Oxc を使った汎用的な解析と、Astro 固有の構文と変換。ブラウザには、出力 HTML から DOM を構築する役割。この方向性を一言でいうと、コンパイラを less clever にする、ということです。暗黙に補正する範囲を減らして、解析と変換と後続処理の境界を明確にする。
-->

---
layout: default
class: body-center
---

## Contentの例へ戻る

<div class="text-xl opacity-70 mb-6">Content Processor — MarkdownとMDXを解析し、HTMLやJavaScriptへ変換する処理系</div>

<div class="grid grid-cols-2 gap-8 text-xl">
  <div class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
    <div class="text-2xl font-600">Astroが担当すること</div>
    <ul class="mt-3 text-lg">
      <li>Processorを接続する入口を用意する</li>
      <li>Content CollectionsやBuildと接続する</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Processorが担当すること</div>
    <ul class="mt-3 text-lg">
      <li>MarkdownとMDXの構文</li>
      <li>Content固有の変換</li>
      <li>拡張機能を実行する仕組み</li>
    </ul>
  </div>
</div>

<div class="mt-8 text-xl text-primary"><code>.astro</code> Compilerとは、別の処理系として選ぶ</div>

<!--
Content の話に戻ります。第3章で、Rust 製 MDX コンパイラの PoC と plugin 互換性の問題を見ました。ここで決めたのは、Markdown と MDX を担当する場所です。Astro が担当するのは、Processor を接続する入口を用意することと、Content Collections やビルドと接続すること。Processor が担当するのは、Markdown と MDX の構文、Content 固有の変換、拡張機能を実行する仕組み。そして .astro のコンパイラとは、別の処理系として選ぶ。
-->

---
layout: default
class: body-center
---

## SätteriとJavaScript pluginの分担

<div class="grid grid-cols-2 gap-10 mt-10 text-xl">
  <div>
    <h3 class="opacity-100 !text-base">Sätteri</h3>
    <ul class="mt-3">
      <li>Rust中心の処理</li>
      <li>よく使う処理は標準機能</li>
      <li>JavaScriptで拡張できる</li>
    </ul>
  </div>
  <div>
    <h3 class="opacity-100 !text-base">pluginとの境界</h3>
    <div class="grid grid-cols-[2rem_1fr] gap-x-3 gap-y-4 mt-3">
      <div class="text-primary">1</div><div>扱う node の種類を指定</div>
      <div class="text-primary">2</div><div>その node を JavaScript で処理</div>
      <div class="text-primary">3</div><div>必要な情報だけを受け渡す</div>
    </div>
  </div>
</div>

<Ref href="https://satteri.bruits.org/docs/plugins/">Sätteri — Plugin API</Ref>

<!--
Sätteri の設計です。Rust を中心に Markdown と MDX を処理して、よく使う処理を標準機能として提供する。そのうえで、JavaScript で独自の変換を追加できる。plugin との境界はこうです。plugin が扱いたいノードの種類を指定して、そのノードを処理する関数を JavaScript で実行し、必要な情報だけを境界で受け渡す。visitor というのは、特定の種類のノードを受け取って調べたり変更したりする関数のことです。見出しだけを処理する、リンクだけを処理する、といった書き方になります。
-->

---
layout: default
class: body-center
---

## unifiedの経路も残す

```js
import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";

const contentProcessor = unified();

export default defineConfig({
  markdown: {
    processor: contentProcessor,
  },
});
```

<div class="mt-8 grid grid-cols-2 gap-8 text-xl">
  <div><span class="text-primary font-600">Astro</span>　Processorを接続する</div>
  <div><span class="text-primary font-600">Processor</span>　Contentを解析して変換する</div>
</div>

<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Markdown Processors — Astro Docs</Ref>

<!--
既存の plugin を使い続けたい人には、unified の経路を残します。unified は remark や rehype を組み合わせて構文を変換する JavaScript の基盤です。Sätteri と remark、rehype では plugin の仕組みが違うので、互換性を保つ方法は2つ。Sätteri 向けに plugin を移植するか、unified の Processor を使うか。必要なパッケージを入れたうえで、この設定のように unified を明示的に選べます。この設定が表しているのは責務分担です。Astro は Processor を接続する。Processor は Content を解析して変換する。
-->

---
layout: default
class: body-center
---

## 提案時の判断と、採用後の状態を分ける

<div class="grid grid-cols-2 gap-10 mt-8 text-lg">
  <div>
    <div class="mb-4"><Status kind="poc" />　自分が試したこと</div>
    <div class="flex flex-col gap-3">
      <div class="border border-[#E5E0EC] rounded-lg px-4 py-3">Rust製MDX Compilerの統合を試した</div>
      <div class="border border-[#E5E0EC] rounded-lg px-4 py-3">AST Bridgeで既存pluginとの接続を試した</div>
    </div>
  </div>
  <div>
    <div class="mb-4"><Status kind="adopted" />　実際に入ったもの</div>
    <div class="flex flex-col gap-3">
      <div class="border border-[#E5E0EC] rounded-lg px-4 py-3">
        <span class="text-primary">Astro 6.4</span>　Markdown Processorを選ぶ仕組みが追加された
      </div>
      <div class="border border-[#E5E0EC] rounded-lg px-4 py-3">
        <span class="text-primary">Astro 7</span>　Sätteriが標準Processorになった
      </div>
      <div class="border border-[#E5E0EC] rounded-lg px-4 py-3">unifiedを選ぶ経路も用意されている</div>
    </div>
  </div>
</div>

<div class="mt-8 flex gap-4 items-center">
  <span class="text-lg opacity-60">スライドには、対象バージョンと状態を添える</span>
  <Status kind="adopted" />
  <Status kind="wip" />
  <Status kind="proposed" />
  <Status kind="poc" />
</div>

<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Markdown Processors — Astro Docs</Ref>

<!--
ここは混同しやすいので分けて話します。自分が PoC として試したのは、Rust 製 MDX コンパイラの統合と、AST Bridge による既存 plugin との接続です。実際に採用されたのは、Astro 6.4 で Markdown Processor を選ぶ仕組みが追加されたこと、Astro 7 で Sätteri が標準 Processor になったこと、そして unified を選ぶ経路も用意されていること。提案した内容と、採用された内容は別です。
-->

---
layout: default
class: body-center
---

## xmdxからSätteriを勧める判断

<div class="grid grid-cols-2 gap-8 mt-6 text-lg">
  <div>
    <h3 class="opacity-100 !text-base">xmdxの検証で、必要な条件が具体的になった</h3>
    <ul class="mt-2">
      <li>速度</li>
      <li>pluginとの接続</li>
      <li>Astroへの統合</li>
      <li>配布と継続的な保守</li>
    </ul>
    <p class="mt-4 text-primary">その条件を使って、ほかの実装も比較できるようになった</p>
  </div>
  <div>
    <h3 class="opacity-100 !text-base">PoCから残ったもの</h3>
    <ul class="mt-2">
      <li>実際に試して分かった制約</li>
      <li>選択肢を比較するための判断材料</li>
      <li>upstreamとcommunityとの関係</li>
    </ul>
    <p class="mt-4 text-primary">自分の実装が採用されること以外にも、<br />次の判断へつながる成果があった</p>
  </div>
</div>

<Ref href="https://github.com/jp-knj/xmdx">xmdx のREADMEでも、Sätteriの利用を案内している</Ref>

<!--
xmdx から Sätteri を勧める判断についてです。xmdx の検証で、速度、plugin との接続、Astro への統合、配布と継続的な保守、という条件が具体的になりました。その条件があったから、ほかの実装も比較できるようになった。そして Astro の要求に合う実装として Sätteri を勧める判断につながりました。xmdx の README でも Sätteri の利用を案内しています。PoC から残ったものは、実際に試して分かった制約、選択肢を比較するための判断材料、そして upstream とコミュニティとの関係です。自分の実装が採用されること以外にも、次の判断につながる成果があります。
-->

---
layout: default
class: body-center
---

## 実装言語と、配布方法を分けて考える

<div class="grid grid-cols-4 gap-5 mt-8 text-lg">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">実装言語</div>
    <div class="opacity-65 mt-2">どの言語で処理を書くか</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">配布と実行方法</div>
    <div class="opacity-65 mt-2">どの環境で、その処理を動かすか</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">AST設計</div>
    <div class="opacity-65 mt-2">ソースをどの構造で表し、何を保持するか</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">責務の所有</div>
    <div class="opacity-65 mt-2">どのprojectが実装して保守するか</div>
  </div>
</div>

<div class="mt-8 text-xl leading-relaxed">
  <p class="text-primary">これらは、それぞれ別の判断になる</p>
  <p class="opacity-70">Node.js向けには native bindings。Browser内でCompilerを動かす場合はWASMの経路を考える</p>
  <p class="opacity-60 text-lg">全体図のBrowserは、生成されたサイトを表示する場所。Compiler自体をBrowser内で実行する話とは区別する</p>
</div>

<Ref href="https://github.com/withastro/compiler-rs">Rust版Compiler README / bindingsの構成</Ref>

<!--
第1章の「分けて考える選択」に戻ります。実装言語、配布と実行方法、AST 設計、責務の所有。この4つはそれぞれ別の判断です。Node.js 向けには native bindings を使い、ブラウザ内でコンパイラを動かす場合は WASM の経路を考える。Rust 版の実装にも WASM 向けの経路があります。提供する環境と API は実装ごとに確認してください。ひとつ注意点として、全体図のブラウザは生成されたサイトを表示する場所であって、コンパイラ自体をブラウザ内で実行する話とは区別しています。
-->

---
layout: center
---

<Overview
  subs="parser,oxc,astro-syntax"
  :annotate="{
    compiler: 'parse() でASTを提供し、transform() でJavaScriptへ変換する',
    editor: 'ASTとソース位置から、診断と補完を提供する',
    content: 'frontmatter と見出しID、コードの色付け、MDX component',
  }"
/>

<!--
最後の全体図です。Astro Compiler は Astro Syntax を解析し、ソース構造と位置を保持し、parse() で AST を提供し、transform() で HTML 生成用の JavaScript へ変換する。汎用的な解析には Oxc を使う。Editor は AST とソース位置を利用して、不完全な構文を扱いながら診断と補完を提供する。Build はモジュールを解決して JavaScript と CSS をまとめる。Vite とその内部の Rolldown を使いますが、この分担は Go 版の導入時から存在していました。Astro の Content は Processor を選べる統合点を提供して、Content Collections とビルドへ接続する。Content Processor は Markdown と MDX を解析して変換し、frontmatter や見出しの ID、コードの色付け、MDX component を扱い、汎用的な機能と plugin model を保守する。unified ecosystem は既存 plugin が必要な利用者の経路を担う。なお Rust 版コンパイラの公開 API は parse() と transform() を中心に説明できます。Language Server 向けの TSX 出力は、実行用コンパイラとは別の要件として扱われています。
-->

---
layout: default
class: body-center
---

## 三つの具体例を、同じ全体図へ重ねる

<div class="grid grid-cols-3 gap-6 mt-10 text-lg">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">HTML</div>
    <div class="text-2xl font-600 mt-1">保持と補正</div>
    <ul class="mt-3">
      <li>書かれた構造を保持する</li>
      <li>Compilerの解析とBrowserのDOM構築を区別する</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">JavaScript</div>
    <div class="text-2xl font-600 mt-1">構造と再利用</div>
    <ul class="mt-3">
      <li>式の内部をASTとして提供する</li>
      <li>汎用的な解析にはOxcを利用する</li>
    </ul>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">Markdown と MDX</div>
    <div class="text-2xl font-600 mt-1">互換性と所有</div>
    <ul class="mt-3">
      <li>pluginとの接続も要件に含める</li>
      <li>Astroとの統合と、汎用的なContent処理を分ける</li>
    </ul>
  </div>
</div>

<!--
3つの具体例を並べます。HTML は保持と補正の話。書かれた構造を保持して、コンパイラの解析とブラウザの DOM 構築を区別する。JavaScript は構造と再利用の話。式の内部を AST として提供して、汎用的な解析は Oxc に任せる。Markdown と MDX は互換性と所有の話。plugin との接続も要件に含めて、Astro との統合と汎用的な Content 処理を分ける。
-->

---
layout: center
---

<Overview
  subs="parser,oxc,astro-syntax"
  contract="source,output,ecosystem"
/>

<!--
3つの契約で整理します。まず「契約」というのは、処理をつなぐ相手へどんな情報や振る舞いを保証するか、という意味で、この講演で設計を整理するために使っている呼び方です。Source contract は主にコンパイラと Editor の間。書かれた構造と位置を保持し、埋め込まれた構文をツールが利用できる形で渡す。Output contract はコンパイラとビルドとブラウザの間。実行や表示につながる成果物を生成し、ソースの構造と最終的な表示の構造を区別する。Ecosystem contract は Content Processor と plugin ecosystem の間。既存 plugin を利用できる経路を維持し、新しい plugin model への移行方法を用意する。
-->

---
layout: default
class: body-center
---

## この章の結論

<div class="mt-10 text-xl leading-relaxed">
  <ul>
    <li>Rustへの移行では、<b>Compilerの設計と保守範囲</b> も見直している</li>
    <li>汎用的な処理には、<b>既存の基盤</b> を利用する</li>
    <li>Astroは、<b>Astro固有の構文と変換と統合</b> を担当する</li>
    <li>用途に応じて、<b>RustとJavaScriptの役割</b> を分ける</li>
    <li><code>.astro</code> Compiler と Markdown と MDX の Processor も、それぞれの要件に合った構成を選ぶ</li>
  </ul>
</div>

<!--
第4章の結論です。Rust への移行では、コンパイラの設計と保守範囲も見直しています。汎用的な処理には既存の基盤を使い、Astro は Astro 固有の構文と変換と統合を担当する。用途に応じて Rust と JavaScript の役割を分ける。そして .astro のコンパイラと、Markdown / MDX の Processor も、それぞれの要件に合った構成を選ぶ。
-->

---
layout: statement
class: flex flex-col justify-center h-full
---

# 動いていたGoコンパイラを、<br />AstroはなぜRustで書き直したのか？

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
    <div class="text-sm uppercase tracking-widest text-[#717781]">当時の判断</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>高速な変換と、複数環境での実行</div>
      <div>GoとWASMが要件に合っていた</div>
    </div>
  </div>
  <div class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">発見した問題</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>ソース構造と位置への要求</div>
      <div>HTML補正による予想しにくい挙動</div>
      <div>独自実装の保守コスト</div>
    </div>
  </div>
  <div class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">前提の変化</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>Rust基盤の成熟</div>
      <div>再利用できる範囲の拡大</div>
      <div>Astro Syntax の整理</div>
    </div>
  </div>
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">新しい判断</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>保持する情報と変換する段階の明確化</div>
      <div>保守範囲を絞る</div>
      <div>改善し続けられる設計へ</div>
    </div>
  </div>
</div>

<!--
4章ぶんの答えです。当時の判断は、高速な変換と複数環境での実行が必要で、Go と WASM がその要件に対応していた。発見した問題は、ソース構造と位置を扱う要求が明確になったこと、HTML 補正が不具合や予想しにくい挙動につながったこと、そして独自実装を継続して保守する難しさ。前提の変化は、Rust の解析と変換基盤が育ち、汎用的な処理を再利用できる範囲が広がり、Astro Syntax の整理も進んだこと。新しい判断は、保持する情報と変換する段階を明確にして、既存基盤を使って自分たちの保守範囲を絞り、チームが継続して改善できるコンパイラへ作り直すこと。Content での取り組みも、同じ責務設計の問題を別の処理経路で検証したものでした。
-->

---
layout: center
class: text-center
---

<div class="text-5xl font-700 leading-[1.5]" style="color: #7611A6">
  既存の基盤を再利用し、<br />
  自分たちが持つ処理を絞り、<br />
  保守し続けられる設計にするため。
</div>

<!--
一言でいうとこうなります。Rust の基盤を再利用しながら、Astro が持つべき処理を絞り、継続して保守できるコンパイラへ再設計するため。速いから、ではありません。
-->

---
layout: default
class: body-center
---

## 持ち帰ってほしいこと

<div class="mt-8 text-2xl text-primary">技術選定は、その時点の要件と利用できる基盤に対する判断</div>

<div class="mt-8 text-xl">
  <h3 class="opacity-100 !text-base">技術を選び直すときに確認すること</h3>
  <ul class="mt-3">
    <li>当時、何を実現するために選んだのか</li>
    <li>利用が広がり、何が新しく必要になったのか</li>
    <li>今なら、どの処理を既存基盤へ任せられるのか</li>
    <li>自分たちが実装して保守するべき処理は何か</li>
  </ul>
</div>

<div class="mt-8 text-xl leading-relaxed">
  <p>技術を選び直す機会に、<b>担当する責務も見直す</b></p>
  <p class="opacity-70">PoCがmergeされなくても、制約を明らかにし、communityの次の判断につなげられる</p>
</div>

<!--
持ち帰ってほしいことです。技術選定は、その時点の要件と利用できる基盤に対する判断です。だから、選び直すときに確認すべきことは4つ。当時、何を実現するために選んだのか。利用が広がって、何が新しく必要になったのか。今ならどの処理を既存基盤へ任せられるのか。そして、自分たちが実装して保守するべき処理は何か。技術を選び直す機会は、担当する責務を見直す機会でもあります。最後にもうひとつ。PoC がマージされなくても、制約を明らかにして、コミュニティの次の判断につなげることはできます。
-->

---
layout: center
class: text-center
---

## ありがとうございました

<div class="mt-8 text-xl opacity-60">Astro Japan Community</div>

<img src="./images/qrcode_discord.com.png" class="h-60 mx-auto mt-6" alt="Discord QR Code" />

<!--
ありがとうございました。Astro Japan Community の Discord です。よかったら覗いてみてください。
-->
