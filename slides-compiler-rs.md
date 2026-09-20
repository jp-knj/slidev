---
theme: ./theme-light
author: jp-knj
title: AstroとRustで考えるフロントエンドツールチェーンの今
info: |
  動いていたGoコンパイラを、AstroはなぜRustで書き直したのか。
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

# Goで動いていたものを、<br />なぜ、Rustに書き直すのか？

<!--
今日の問いはこれ1つです。「動いていた Go コンパイラを、Astro はなぜ Rust で書き直したのか」。速いから、で終わらせずに、何が問題で、何が変わって、どう責務を分け直したのかを見ていきます。
-->

---
layout: default
class: body-center
---

## 話すこと

<div class="grid grid-cols-1 gap-4 mt-10">
  <div>
    <div class="text-3xl font-600 mt-1">1. 当時の判断</div>
    <div class="text-lg opacity-60 mt-2">なぜ最初にGoとWASMを選んだのか</div>
  </div>
  <div>
    <div class="text-3xl font-600 mt-1">2. 発見した問題</div>
    <div class="text-lg opacity-60 mt-2">使い続けるなかで何が見えたのか</div>
  </div>
  <div>
    <div class="text-3xl font-600 mt-1">3. 前提の変化</div>
    <div class="text-lg opacity-60 mt-2">2026年までに周囲はどう変わったのか</div>
  </div>
  <div>
    <div class="text-3xl font-600 mt-1">4. 新しい判断</div>
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

<Overview
  visible="source,compiler,build,browser"
  :labels="{ compiler: 'Svelte Compiler', build: 'Snowpack' }"
  :icons="{ compiler: 'svelte', build: 'snowpack' }"
/>

<div class="text-center text-xl opacity-60 mt-2">Astro 0.x の出発点</div>

<!--
これが出発点です。最初の Astro は、.astro を Svelte のコンパイラの fork で読んで、Snowpack がビルドと配信を担い、ブラウザが表示する。この4つでした。ここに出ている Svelte Compiler と Snowpack は、このあと Go 製のコンパイラと Vite に入れ替わります。その入れ替えがこの章の話です。そしてこの図には、この講演で何度も戻ってきます。章が進むごとに、登場人物と矢印が増えていきます。
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
      <img src="./images/logos/gopher-classic.png" alt="Go" class="h-16 mt-6" />
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
      <img src="./images/logos/gopher-classic.png" alt="Go" class="h-16 mt-6" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col items-center">
      <div class="text-3xl text-[#717781] h-11 leading-none">Dec</div>
      <div class="w-3.5 h-3.5 rounded-full bg-[#9A90AB]"></div>
      <logos-turborepo-icon class="text-6xl mt-8" />
      <div class="text-xl mt-5 leading-snug">Turborepo</div>
      <img src="./images/logos/gopher-classic.png" alt="Go" class="h-16 mt-6" />
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
さきほどの Svelte のコンパイラの fork を、ここで Go に置き換えます。JavaScript との境界には WASM を置き、ビルドは Snowpack から Vite に任せ直した。重要なのは、当時これは「ビルドのためのコンパイラ」だったということです。主な入口は transform API ひとつ。ソースを受け取って、実行できる JavaScript を返す。それが仕事のすべてでした。
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
全体図に登場人物が増えました。Editor のツール、つまり ESLint や Language Server や Formatter が、同じコンパイラを使うようになった。それと MarkdownとMDX の経路。Content の経路は図に残しますが、第3章の後半まで強調はしません。この章では2か所にズームします。HTML の構造と、埋め込まれた JavaScript です。
-->

---
layout: default
class: syntax-overview body-center
clicks: 4
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
  <div v-if="$clicks === 0"><span class="text-primary font-600">Component script</span><br /><code>---</code> で囲む。ビルド時とサーバーで実行する JS と TS</div>
  <div v-if="$clicks === 1"><span class="text-primary font-600">Template</span><br />HTML を基礎に、式やコンポーネントを書ける</div>
  <div v-if="$clicks === 2"><span class="text-primary font-600">{ }</span><br />JavaScript 式の結果を、その場所に表示する</div>
  <div v-if="$clicks === 3"><span class="text-primary font-600">Q. </span>この <code>title</code> は、どちらの値になる？</div>
  <div v-if="$clicks === 3" class="mt-4"><code>first</code> か、<code>second</code> か</div>
  <section v-if="$clicks >= 4" class="syntax-answer-panel" aria-label="属性の値の答え">
    <div class="syntax-answer-heading">
      <strong class="syntax-answer-value"><code>first</code></strong>
      <span class="syntax-answer-context">2022年の報告に基づく例</span>
    </div>
    <div class="syntax-answer-details">
      <div>
        <strong><code>second</code> と予想する理由</strong>
        <div>後から書いた <code>{...props}</code> の <code>title</code> が優先されると考えるため。</div>
      </div>
      <div>
        <strong>当時 <code>first</code> になった理由</strong>
        <div>Astroが同じ名前の属性を出力し、<br />ブラウザが先にある <code>title="first"</code> を採用したため。</div>
      </div>
    </div>
    <div class="syntax-answer-reference">
      <a href="https://github.com/withastro/astro/issues/5558#issuecomment-1343799494" target="_blank" rel="noopener noreferrer">astro#5558の説明</a>
    </div>
  </section>
</div>

<Ref v-if="$clicks < 3" href="https://docs.astro.build/en/reference/astro-syntax/">Astro Syntax</Ref>

<!--
Astro の構文をおさらいします。初めに三本線で囲まれた Component script を示します。1クリック目で Template、2クリック目で波かっこに埋め込んだ JavaScript の式を示します。
3クリック目では同じ例に属性を加え、title がどちらの値になるかを問いかけます。4クリック目で報告者の期待と当時の結果を示します。報告の論点に絞った例です。HTML の重複属性では先の値を採用し、JSX での props 合成では後の指定を優先します。Astro は HTML を基礎にした構文で、JSX に似ていても同じ規則とは限りません。この違いが利用者の期待との不一致になりました。
2022年の元の報告にある class 属性を、ここでは title に簡略化しています。現在のAstroの挙動を示す例ではありません。
-->

---
layout: default
class: body-center
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
2023年の報告です。要素を改行して並べると、要素間に空白だけのテキストノードができます。AstroはSourceの改行を出力にも保持します。Browserの空白の扱いが表示に影響するため、JSXでの表示と比べると違いがあります。次は、CompilerのHTMLパーサーを確認します。
-->

---
layout: default
class: table-comparison body-center
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

<Transition name="reveal-up">
<div class="mt-10 text-center" v-if="$clicks >= 2">
  <div class="text-2xl">HTMLの規則に従って構造を直した結果、<b>表の後の見出しが表の中に入った</b></div>
</div>
</Transition>

</div>

<Ref href="https://github.com/withastro/compiler/issues/870">compiler#870</Ref>

<!--
最初は書いたAstroを確認します。1回目のクリックで、報告された生成HTMLを右に表示します。2回目で問題を整理します。
compiler#870の報告当時、Build向けの変換でtableの後のh2がtableの中に入る不具合がありました。この結果をHTML仕様どおりとは説明しません。Compilerが生成するHTMLと、BrowserがそのHTMLから作るDOMは区別します。
DOMは、Browserが表示のために作るHTMLの木です。HTML5の補正は、HTMLの規則に従って要素の移動や追加を行うことです。補正後の親子関係だけを見ても、書かれた入れ子は分かりません。たとえばpの中にdivを書くと、divの開始でpが閉じられます。補正後の木からは、元の入れ子を診断できません。
次の問い: Editorは、補正される前の構造をどう取得するのか？
-->

---
layout: default
class: body-center
clicks: 3
---

## Go Compilerの二つのパーサー

<div class="mt-10 flex flex-col items-center gap-8 text-3xl">
  <div class="flex items-center gap-4 text-[#717781]">
    <span>.astro Source</span><span class="text-[#9A90AB]">→</span><span>Tokenizer</span>
  </div>
  <div class="grid grid-cols-[auto_auto_auto] items-center gap-x-4 gap-y-7">
    <span v-click="1" class="text-[#A36B09]">HTML5パーサー</span>
    <span v-click="1" class="text-[#9A90AB]">→</span>
    <span v-click="1" class="flex items-baseline gap-3">
      <span class="text-[#0B7BC1]">transform()</span>
      <span class="text-xl text-[#717781]">Build向け</span>
    </span>
    <span v-click="2" class="text-[#7611A6]">Literal modeのパーサー</span>
    <span v-click="3" class="text-[#9A90AB]">→</span>
    <span v-click="3" class="flex items-baseline gap-3">
      <span class="text-[#0B7BC1]">parse()とconvertToTSX()</span>
      <span class="text-xl text-[#717781]">Editor向け</span>
    </span>
  </div>
</div>

<Ref href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/cmd/astro-wasm/astro-wasm.go#L251-L284">Go Compiler 2.12.2とParseとConvertToTSXとTransform</Ref>

<!--
SourceとTokenizerを示し、クリックでtransformの経路、Literal modeの経路、parseとconvertToTSXの順に足します。
Tokenizerは、コードをタグや文字などの小さな単位へ分けます。Literal modeは、HTMLの規則で木を直さず、書かれた入れ子のまま木を作るパーサーです。transformはBuildするコードを作り、parseは書かれたとおりの木をASTにし、convertToTSXはAstroをTypeScriptが読める形に変えます。
Go版2.12.2の実装を確認すると、ParseとConvertToTSXはParseOptionEnableLiteral(true)を指定しています。Transformはこの指定をしていません。HTMLの補正という説明には、どのAPIの経路なのかを明示する必要があります。同じSourceを二つの方法で読んでいた、というのがこの枚の要点です。Go版にもEditor向けの工夫はありました。
次の問い: 取得した木を、各Editor toolはどう使っていたのか？
-->

---
layout: default
class: ch2-code body-center
clicks: 2
---

## Linterに要る二つの情報

```astro
---
const { title } = Astro.props;
---
<p class="lead">
  {title}
  <div class="note">{descrption}</div>
</p>
```

<div class="mt-4 flex flex-col gap-3">
  <div v-click="1">
    <div class="text-2xl font-600 text-[#7611A6]">Astroのnodeと位置</div>
    <div class="text-xl">補正で <code>div</code> は <code>p</code> の兄弟になる。位置はsourceから数え直す</div>
  </div>
  <div v-click="2">
    <div class="text-2xl font-600 text-[#0B7BC1]">JavaScriptのESTreeとscope</div>
    <div class="text-xl"><code>descrption</code> に宣言が無いことは、ここで分かる</div>
  </div>
</div>

<Ref href="https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/index.ts">astro-eslint-parser v1.2.2とparseForESLint</Ref>

<!--
コンポーネントを出して、クリックで二つ足します。
Linter に要るものは二種類あります。ひとつは Astro の node と、.astro 上の位置。HTML5 の規則では div の開始で p が閉じるので、補正後の木では div は p の兄弟になります。木をたどる順と、書かれた順がずれる。だから位置は source から数え直します。
もうひとつは JavaScript です。descrption に宣言が無い、という判定はここでしか出せません。
この二つは、別々のところからしか出てきません。
次の問い: 別々のところにある情報を、どうやって一度に検査するのか？
-->

---
layout: default
class: body-center
clicks: 3
---

## ESTreeにAstro nodeを加える

<div class="mt-6 grid grid-cols-[auto_auto_auto_auto_auto] items-center justify-center gap-x-3 gap-y-6">
  <div class="row-span-2 text-[22px] text-[#717781]">Astro AST</div>

  <div v-click="1" class="text-[22px] text-[#9A90AB]">→</div>
  <div v-click="1">
    <div class="text-[22px] font-600 text-[#7611A6]">source順に並べ直す</div>
    <div class="text-xl text-[#0B7BC1]">位置を数え直す</div>
  </div>
  <div v-click="1" class="text-[22px] text-[#9A90AB]">→</div>

  <div class="row-span-2">
    <div v-click="3" class="text-[22px] font-600 text-[#7611A6]">ESTreeにAstro nodeを加える</div>
  </div>

  <div v-click="2" class="text-[22px] text-[#9A90AB]">→</div>
  <div v-click="2">
    <div class="text-[22px] font-600 text-[#A36B09]">JavaScript parserへ渡す形を作る</div>
    <div class="text-xl text-[#0B7BC1]">ESTreeとscopeを受け取る</div>
  </div>
  <div v-click="2" class="text-[22px] text-[#9A90AB]">→</div>
</div>

<div class="mt-8 text-center text-xl text-[#717781]">
  <code>parse(source, &#123; position: true &#125;)</code> が返す Astro AST から始まる
</div>

<Ref href="https://github.com/ota-meshi/astro-eslint-parser/pull/14">astro-eslint-parser PR #14とadjustHTML</Ref>

<!--
Astro AST から二手に分かれて、下でまた一つになります。クリックで左、右、最後の一つ、の順に足します。
左は位置の話です。補正後の木は source 順と並びが違うので、adjustHTML と adjustHTMLBody で source 順へそろえてから、fixLocations が source の UTF-16 range を計算し直します。PR #14 はここで crash した話で、木の巡回順を source 順として扱っていたのが原因でした。
右は JavaScript の話です。template から virtual JSX を作って、espree または @typescript-eslint/parser に渡すと、ESTree と token と comment と scope manager が返ってきます。
そして最後に一つにします。返ってきた ESTree へ Astro node を入れて、Astro 用の visitor key と parent と range を加える。virtual JSX にしか無い token と scope は除きます。
ここが今日いちばん言いたいところです。片方へ変換して終わりではありません。二つを組み合わせて、はじめて ESLint が走れる形になります。判定するのは eslint-plugin-astro の rule で、fixer は完成した range で .astro へ edit を当てます。
次の問い: 親子関係を検査できても、書かれたとおりに書き戻せるのか？
-->

---
layout: default
class: ch2-code body-center
clicks: 4
---

## Formatterと書かれた表記

```astro
<p class="lead">
  {title}
  <div class="note">{descrption}</div>
</p>
```

<div class="mt-8 flex flex-col items-center gap-5">
  <div class="flex items-center gap-3 text-2xl">
    <span class="text-[#717781]">Source</span>
    <span v-click="1" class="text-[#9A90AB]">→</span>
    <span v-click="1" class="text-[#7611A6]">Astro AST</span>
    <span v-click="2" class="text-[#9A90AB]">→</span>
    <span v-click="2" class="text-[#A36B09]">Astro Printer</span>
    <span v-click="3" class="text-[#9A90AB]">→</span>
    <span v-click="3" class="text-[#0B7BC1]">Prettier</span>
    <span v-click="4" class="text-[#9A90AB]">→</span>
    <span v-click="4" class="text-[#7611A6]">整形後のSource</span>
  </div>
  <div v-click="1" class="text-xl text-[#7611A6]">補正で div は p の外へ出ている</div>
</div>

<div v-click="4" class="mt-6 text-center text-2xl text-primary">補正後のASTだけでは戻せない。printerはASTとsourceの両方を見る</div>

<Ref href="https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/index.ts">prettier-plugin-astro v0.14.1とparserとSource位置</Ref>

<!--
整形前のSourceを示し、クリックでAstro AST、Astro Printer、Prettier、整形後のSourceの順に足します。
補正後のASTをそのまま直列化すると、div が p の外に出た形で書き戻ります。空白と改行だけでなく、tag の境界まで変わってしまう。
だから Astro 専用の printer は、Astro AST だけでなく source も見ます。prettier-ignore、raw text、quote、comment、補正前の文字範囲は source にしかありません。
prettier-plugin-astro v0.14.1はGo版の同期parse APIを使います。Astro ASTとSource範囲で全体を扱い、locStartとlocEndで範囲を参照します。式はJSX互換の表現にして、babel-tsを基にしたparserで整形します。これは既存Formatterを再利用するための変換です。
参考: https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/printer/embed.ts
次の問い: 書かれた表記はsourceを見れば戻せた。JavaScriptの中身も理解できるのか？
-->

---
layout: default
class: ch2-code body-center
clicks: 5
---

## TextNodeとJavaScript AST

```astro
---
const price = 1_200;
---
<p>{pirce}</p>
```

<div class="mt-6 flex flex-col items-center gap-4">
  <div class="flex items-center gap-3 text-2xl">
    <span class="text-[#717781]">Astro Source</span>
    <span v-click="1" class="text-[#9A90AB]">→</span>
    <span v-click="1" class="text-[#7611A6]">TextNode</span>
    <span v-click="2" class="text-[#9A90AB]">→</span>
    <span v-click="2" class="text-[#A36B09]">Virtual TSX</span>
    <span v-click="3" class="text-[#9A90AB]">→</span>
    <span v-click="3" class="text-[#0B7BC1]">Identifier</span>
    <span v-click="4" class="text-[#9A90AB]">→</span>
    <span v-click="4" class="text-[#0B7BC1]">TypeScript診断</span>
  </div>
  <div v-click="1" class="text-xl text-[#B42318]">TextNode は、式を文字列のまま持つ</div>
  <div v-click="5" class="text-2xl text-[#7611A6]">診断の位置は、元のSourceへ戻す</div>
</div>

<Ref>
  <a href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#parse-astro-and-return-an-ast">Go Compiler 2.12.2と公開ASTの制約</a>
  <a href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#position-data" class="ml-8">同 Position data</a>
</Ref>

<!--
pirceへ波線を引きたい、という目的から始めます。クリックでTextNode、Virtual TSX、Identifier、TypeScriptの診断、位置を戻す、の順に足します。
ASTはコードの部品とその関係を表した木、NodeはASTを構成する一つの部品、TextNodeは文字をひとかたまりで持つNode、Identifierは変数名を表すNodeです。Virtual TSXはTSXと元のSourceの位置を対応させたもの、mappingは変換前と変換後の位置を結び付ける情報です。
TextNodeもASTの一部です。ただし、pirceを変数名として分解していません。Go版の公開ASTでは、ExpressionNodeの子のTextNodeが式のソースを文字列で保持します。周辺ノードと位置フィールドを省くと、type expression の children に type text の value として式がそのまま入っている形です。JavaScriptの式を内部ASTとして提供する形ではありません。
TypeScriptがIdentifierとして扱うことで、priceとの違いを診断できます。診断を出すには、元のAstroファイル上の範囲も要ります。Go版2.12.2のREADMEは、位置データが不完全で一部のケースでは不正確と明記しています。位置情報が存在しなかったという説明は誤りです。astro-eslint-parser v1.2.2にはfixLocationsがあり、元のソースから範囲を再計算しています。
次の問い: HTML補完とJavaScriptの意味解析に、同じ表現を渡せるのか？
-->

---
layout: default
class: body-center
clicks: 4
---

## Language Toolと二つの表現

<div class="mt-10 flex flex-col items-center gap-8 text-2xl">
  <div class="text-[#717781]">Astro Source</div>
  <div class="grid grid-cols-[auto_auto_auto] items-center gap-x-4 gap-y-7">
    <span v-click="1" class="text-[#A36B09]">HTML virtual document</span>
    <span v-click="2" class="text-[#9A90AB]">→</span>
    <span v-click="2" class="flex items-baseline gap-3">
      <span class="text-[#0B7BC1]">HTML Language Service</span>
      <span class="text-xl text-[#717781]">タグと属性の補完</span>
    </span>
    <span v-click="3" class="text-[#A36B09]">Virtual TSX</span>
    <span v-click="4" class="text-[#9A90AB]">→</span>
    <span v-click="4" class="flex items-baseline gap-3">
      <span class="text-[#0B7BC1]">TypeScript</span>
      <span class="text-xl text-[#717781]">pirceの診断</span>
    </span>
  </div>
</div>

<Ref href="https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/index.ts">language-toolsとb4bcb4fとAstroVirtualCode</Ref>

<!--
Astro Sourceを示し、クリックでHTML virtual documentの経路、タグと属性の補完、Virtual TSXの経路、pirceの診断の順に足します。
Language Toolは、補完と診断と定義への移動をEditorへ提供する仕組みです。Language Serviceは、コードを解析して補完や診断の結果を返します。HTML virtual documentは、HTMLの機能へ渡すために一時的に作るHTMLです。
目的に合わせて二つの表現を使い分けています。language-toolsの2025年11月末時点のコミットb4bcb4fを参照しています。AstroVirtualCodeはHTML virtual documentとTSXを作ります。Go版convertToTSXのsource mapをVolarのmappingへ変換し、TypeScriptの診断や補完を元ファイルと対応させます。
参考: https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/astro2tsx.ts
次の問い: 三つのツールを並べると、同じところは何か？
-->

---
layout: default
class: body-center
clicks: 2
---

## 三つのEditor tool

<div class="mt-8 grid grid-cols-[190px_214px_214px_214px] gap-x-3 gap-y-6 text-xl">
<div></div>
<div class="text-[#7611A6] font-600">Source</div>
<div class="text-[#A36B09] font-600">変換</div>
<div class="text-[#0B7BC1] font-600">解析結果</div>
<div class="text-2xl font-600">Linter</div>
<div>Astro AST</div>
<div>virtual JSX<div class="text-base text-[#717781]">ESTreeに加えて、位置を戻す</div></div>
<div>ESTreeとESLint</div>
<div v-click="1" class="text-2xl font-600">Formatter</div>
<div v-click="1">Astro AST</div>
<div v-click="1">Astro Printer<div class="text-base text-[#717781]">整形したSourceを返す</div></div>
<div v-click="1">Prettier</div>
<div v-click="2" class="text-2xl font-600">Language Tool</div>
<div v-click="2">Astro AST</div>
<div v-click="2">HTML virtual documentと<br />Virtual TSX<div class="text-base text-[#717781]">補完と診断を戻す</div></div>
<div v-click="2">HTML Language<br />ServiceとTypeScript</div>
</div>

<!--
クリックごとに一段ずつ足します。Linter、Formatter、Language Toolの順です。
どのツールもSourceを基準にし、必要な形へ変換していました。左にSource、中央に変換、右に解析結果を並べると、三つとも同じ形をしていることが分かります。そして三つとも、結果を元のSourceへ戻す工程を自分で持っています。
次の問い: 変換が多いこと自体が問題だったのか？
-->

---
layout: default
class: body-center
clicks: 2
---

## 必要な変換と、足りない分を書く工程

<div class="mt-6 grid grid-cols-3 gap-x-8 items-center text-xl">
<div>
<div class="text-2xl font-600 text-[#A36B09]">必要な変換</div>
<div class="mt-3">virtual JSX</div>
<div>HTML virtual document</div>
<div>Virtual TSX</div>
<div>整形後のSource</div>
</div>
<div class="text-center">
<div class="inline-block border-2 rounded-xl px-6 py-4 border-[#7611A6] bg-[#7611A614]">
<div class="text-2xl font-600 text-[#7611A6]">Astro AST</div>
</div>
</div>
<div v-click="1">
<div class="text-2xl font-600 text-[#B42318]">足りない分を書く工程</div>
<div class="mt-3">TextNodeをJavaScriptとして<br />パースし直す</div>
<div>不完全な位置を修正する</div>
<div>解析結果を元のSourceへ戻す</div>
</div>
</div>

<div v-click="2" class="mt-10 text-center text-2xl text-primary">変換の前に、必要な木と位置が揃っていなかった</div>

<!--
クリックごとに、次の項目を説明します。
変換先が複数あることは自然です。既存のエコシステムを利用するために要る変換なので、変換そのものを問題として扱いません。問題は右です。JavaScriptの内部ASTを得る工程、不完全な位置を直す工程、結果を元のSourceへ戻す工程を、それぞれのツールが自分で持っていました。共通して必要な情報をCompilerがどこまで提供するか、という設計上の課題です。
次の問い: Compilerは、何を保証すればよかったのか？
-->

---
layout: default
class: body-center
clicks: 3
---

## Compilerの二つの契約

<div class="mt-10 flex flex-col items-center gap-8 text-3xl">
  <div class="text-[#717781]">Compiler</div>
  <div class="grid grid-cols-[auto_auto_auto] items-center gap-x-4 gap-y-7">
    <span v-click="1" class="text-[#A36B09]">Output contract</span>
    <span v-click="1" class="text-[#9A90AB]">→</span>
    <span v-click="1" class="text-[#A36B09]">実行と表示</span>
    <span v-click="2" class="text-[#0B7BC1]">Source contract</span>
    <span v-click="2" class="text-[#9A90AB]">→</span>
    <span v-click="2" class="text-[#0B7BC1]">解析と編集</span>
  </div>
</div>

<div v-click="3" class="mt-8 text-xl text-center text-[#0B7BC1]">
  Source contractが渡す情報　書かれたHTMLの親子関係、JavaScriptのAST、Source位置、変換後との位置対応
</div>

<!--
クリックごとに、Output contractの経路、Source contractの経路、Source contractが渡す情報を足します。
contractは、Compilerが何を渡すかについての約束です。Output contractは実行結果を正しく作るための約束で、Browserが解釈するHTMLを生成します。Source contractは、書かれた事実をツールへ渡す約束です。
BuildとEditorを排他的に分類する用語ではなく、保証する情報を区別するための整理です。
次の問い: この約束を、誰がどこまで担当するのか？
-->

---
layout: default
class: body-center
clicks: 5
---

## 三つの責務

<div class="relative mt-6">
<div v-click="2" class="absolute inset-y-[-10px] left-[196px] w-[226px] border-2 rounded-xl border-[#7611A6] bg-[#7611A60D]"></div>
<div v-click="3" class="absolute inset-y-[-10px] left-[422px] w-[226px] border-2 rounded-xl border-[#A36B09] bg-[#A36B090D]"></div>
<div v-click="4" class="absolute inset-y-[-10px] left-[648px] w-[220px] border-2 rounded-xl border-[#0B7BC1] bg-[#0B7BC10D]"></div>
<div class="relative grid grid-cols-[190px_214px_214px_214px] gap-x-3 gap-y-6 text-xl">
<div></div>
<div class="text-[#7611A6] font-600">Source</div>
<div class="font-600" :class="$clicks >= 1 ? 'text-[#A36B09]' : 'text-[#717781]'">変換</div>
<div class="text-[#0B7BC1] font-600">解析結果</div>
<div class="text-2xl font-600">Linter</div>
<div>Astro AST</div>
<div :class="{ 'text-[#A36B09]': $clicks >= 1 }">virtual JSX<div class="text-base text-[#717781]">ESTreeに加えて、位置を戻す</div></div>
<div>ESTreeとESLint</div>
<div class="text-2xl font-600">Formatter</div>
<div>Astro AST</div>
<div :class="{ 'text-[#A36B09]': $clicks >= 1 }">Astro Printer<div class="text-base text-[#717781]">整形したSourceを返す</div></div>
<div>Prettier</div>
<div class="text-2xl font-600">Language Tool</div>
<div>Astro AST</div>
<div :class="{ 'text-[#A36B09]': $clicks >= 1 }">HTML virtual documentと<br />Virtual TSX<div class="text-base text-[#717781]">補完と診断を戻す</div></div>
<div>HTML Language<br />ServiceとTypeScript</div>
</div>
</div>

<div v-click="5" class="mt-8 grid grid-cols-[190px_214px_214px_214px] gap-x-3 text-xl">
<div></div>
<div class="text-[#7611A6] font-600">Compiler<div class="text-base font-400 text-[#717781]">書かれた事実</div></div>
<div class="text-[#A36B09] font-600">Adapter<div class="text-base font-400 text-[#717781]">形と位置を変換</div></div>
<div class="text-[#0B7BC1] font-600">Ecosystem tool<div class="text-base font-400 text-[#717781]">解析と検査と整形</div></div>
</div>

<!--
三つのツールの処理を並べ、クリックで変換と位置対応を黄色で強調し、Compilerの領域、Adapterの領域、Ecosystem toolの領域を順に囲み、最後に三つの役割を出します。
Adapterは、Compilerと各ツールの間でデータの形と位置を変換する処理です。Ecosystem toolは、ESLintとPrettierとTypeScriptなど、解析を担当するツールです。
実装場所は分かれていました。ただし、無関係な処理が乱立していたわけではありません。各ツールが変換と位置対応を持っていました。共通して必要だったのは、Compilerから渡される構造と位置です。
章の結論です。Compilerは書かれた事実を渡す。Adapterは各ツールが読める形へ変換する。Ecosystem toolが解析する。
次の問い: 2026年、この三つの責務を支える基盤として何が使えるのか？
-->

---
layout: default
class: body-center
clicks: 2
---

## 第3章への接続

<div class="mt-4 grid grid-cols-3 gap-x-6 text-center text-xl">
  <div class="border-2 rounded-xl py-2 border-[#7611A6] text-[#7611A6] font-600">Compiler</div>
  <div class="border-2 rounded-xl py-2 border-[#A36B09] text-[#A36B09] font-600">Adapter</div>
  <div class="border-2 rounded-xl py-2 border-[#0B7BC1] text-[#0B7BC1] font-600">Ecosystem tool</div>
</div>

<div v-click="1" class="mt-8 text-center text-3xl leading-relaxed text-[#7611A6]">
  <p class="!my-1">書かれたHTMLの構造</p>
  <p class="!my-1">JavaScript AST</p>
  <p class="!my-1">Source位置と位置対応</p>
</div>

<div v-click="2" class="mt-8 text-center text-4xl font-700 text-primary">
  これらをAstroだけで作り続ける必要はあるのか？
</div>

<!--
クリックごとに、必要な三つの情報、そして中心の問いを出します。
必要な情報と役割の境界が分かりました。Compilerが書かれた事実を渡し、Adapterが形と位置を変換し、Ecosystem toolが解析する。この三つを支えるために要るのは、書かれたHTMLの構造、JavaScript AST、Source位置と位置対応です。
ここからは、これらをAstroだけで作り続ける必要があるのかを考えます。2026年に使えるParserとASTとToolchainの話へ進みます。
-->
---
layout: section
clicks: 1
---

# 3. 前提の変化
<h2 v-click="1">2026年までに周囲はどう変わったのか</h2>

<!--
クリックごとに、次の項目を説明します。
第3章。解決策を決める前に、選択肢がどう増えたのかを整理します。
-->

---
layout: default
class: body-center
clicks: 4
---

## Rust製ツールが、実用的な基盤へ育った

<div class="grid grid-cols-4 gap-10 mt-20 text-center">
  <div><logos-swc class="h-20 w-full" /></div>
  <div v-click="1"><logos-biomejs class="h-20 w-full" /></div>
  <div v-click="2"><logos-oxc class="h-20 w-full" /></div>
  <div v-click="3"><logos-rolldown class="h-20 w-full" /></div>
</div>

<div v-click="4" class="mt-16 text-2xl opacity-70">2021年にも存在した基盤が育ち、その後の新しい実装も加わった</div>

<Ref href="https://oxc.rs/docs/guide/introduction.html">SWC と Biome と Oxc</Ref>

<!--
クリックごとに、次の項目を説明します。
Rust 製のツールが実用的な基盤へ育ちました。SWC は JavaScript と TypeScript の変換基盤。Biome は検査と整形のツールチェーン。Oxc は解析と変換のツール群で、Linter の Oxlint と Formatter の Oxfmt を提供しています。Rolldown は Rust 製のバンドラ。2021年にも存在していたものが育ち、その後の新しい実装も加わりました。
-->

---
layout: default
class: body-center
clicks: 4
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
  <div v-click="1" class="w-40">
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
  <div v-click="1" class="w-40">
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
  <div v-click="2" class="w-40">
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
  <div v-click="2" class="w-40">
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
  <div v-click="3" class="w-40">
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

<div v-click="4" class="mt-12 text-2xl text-primary">
  処理の単位で、実際に使える実装が出そろった
</div>

<!--
クリックごとに、次の項目を説明します。
重要なのは、ツールが増えただけでなく、処理の単位で再利用できるようになったことです。パーサ、トランスフォーマ、リゾルバ、バンドラ、ミニファイア、リンタ、フォーマッタ。完成したツールとして使えるものに加えて、ライブラリとして自分の実装に組み込める部品が増えました。各プロジェクトが、必要な処理を既存の基盤と組み合わせられるようになった。
-->

---
layout: default
class: body-center
clicks: 2
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
  <div v-click="1" class="text-5xl text-primary">→</div>
  <div v-click="1">
    <div class="text-2xl font-600 mb-8">Vite 8</div>
    <div><logos-rolldown class="w-56 h-16" /><div class="text-xl mt-4">Rolldown</div></div>
  </div>
</div>

<div v-click="2" class="mt-16 text-2xl opacity-70">
  フレームワークの外で、汎用的なBuild基盤が育った
</div>

<Ref href="https://vite.dev/blog/announcing-vite8">Announcing Vite 8</Ref>

<!--
クリックごとに、次の項目を説明します。
ビルドの中身も変わりました。Vite 2 の頃は、開発時の事前バンドルに Go 製の esbuild、本番のバンドルに Rollup、と2つに分かれていました。Vite 8 では Rust 製の Rolldown がバンドラになり、それが統合されました。ここで言いたいのは、フレームワークの外で汎用的なビルド基盤が育ったということです。だから Astro は、自分の構文変換と、ビルド全体の処理を分けて考えられる。
-->

---
layout: default
class: body-center
clicks: 1
---

## napi-rsとRustの関数を公開する

```rust
use napi_derive::napi;
#[napi]
pub fn multiply(p: u32, q: u32) -> u32 {
    p * q
}
```

<div v-click="1" class="mt-5 text-xl text-primary"><code>#[napi]</code> からNode.js bindingsを生成する</div>

<Ref href="https://napi.rs/docs/introduction/simple-package">napi-rsとSimple package</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
呼び出し方法を説明する例です。Astroの実装そのものではありません。Node-APIはネイティブ実装をNode.jsから利用するAPIで、napi-rsはRustから利用するための基盤です。
-->

---
layout: default
class: body-center
clicks: 1
---

## napi-rsとJavaScriptから呼び出す

```js
const { multiply } = require("./index.js");
console.log(multiply(1200, 3)); // 3600
```

<div v-click="1" class="mt-5 text-xl text-primary"><code>index.js</code> は、ビルド時に生成される入口</div>

<Ref href="https://napi.rs/docs/introduction/simple-package">napi-rsとSimple package</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
前ページのRust関数をJavaScriptから呼び出します。生成された入口がOSとCPUに合うネイティブ実装をロードします。
-->

---
layout: default
class: body-center
clicks: 3
---

## 実装する言語と、配布する方法を分ける

<div class="grid grid-cols-3 gap-6 mt-8 text-lg">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-2xl font-600">ネイティブバイナリ</div>
    <div class="opacity-65 mt-2">OSとCPUに対応した実行形式を配布する。Node.jsから bindings を通じて利用する</div>
  </div>
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-2xl font-600">WASM</div>
    <div class="opacity-65 mt-2">対応する実行環境で動かせるバイナリ形式。BrowserやNode.jsなどへ配布する選択肢</div>
  </div>
  <div v-click="2" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-2xl font-600">Rust crate</div>
    <div class="opacity-65 mt-2">Rustの実装へ組み込めるライブラリ。必要な解析や変換の機能を取り込む</div>
  </div>
</div>

<div v-click="3" class="mt-10 text-xl leading-relaxed">
  <p class="opacity-70">Node-APIやWASM自体は、2021年にも存在していた。napi-rs も2021年には bindings や型定義の生成を提供していた</p>
  <p class="text-primary">変わったのは、<b>組み合わせられる実装と配布の選択肢</b></p>
</div>

<Ref href="https://napi.rs/blog/announce-v2">Announcing napi-rs v2</Ref>

<!--
クリックごとに、次の項目を説明します。
ここは第1章の「分けて考える選択」の続きです。ネイティブバイナリ、WASM、Rust crate。これらは配布と実行の選択肢です。注意したいのは、Node-API も WASM も 2021年に存在していたということ。napi-rs も2021年には v2 が出ています。だから「新しい技術ができたから」ではないんです。変わったのは、組み合わせられる実装と配布の選択肢の幅です。Node.js でどう実行するか、ブラウザへどう配布するか、を用途ごとに検討できるようになった。
-->

---
layout: default
class: body-center
clicks: 1
---

## JavaScript解析に使えるOxc

```js
import { parseSync } from "oxc-parser";
const source = "price * quantity";
const { program } = parseSync(
  "example.js", source,
);
```

<div v-click="1" class="mt-5 text-xl text-primary">JavaScriptのソース文字列から、内部ASTを取得する</div>

<Ref href="https://oxc.rs/docs/guide/usage/parser.html">Oxc Parser</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
掛け算の実行ではなく、式の解析です。OxcはJavaScriptとTypeScriptのparserを提供し、Rustライブラリとしても利用できます。Astro固有の構文との分担は第4章で説明します。
-->

---
layout: default
class: body-center
clicks: 1
---

## Biomeと空白とコメントを保持する

```js
const price = 1200; // 税込

// 合計金額
price * quantity;
```

<div v-click="1" class="mt-5 text-xl text-primary">Lossless CSTは、tokenに加えて空白と改行とコメントも保持する</div>

<Ref href="https://biomejs.dev/internals/architecture/#parser-and-cst">Biome ArchitectureとParser and CST</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
第2章で整理したSource contractを実現するための設計例です。Biomeはrowanのforkを基にCSTを実装しています。情報を付加したASTも選択肢です。この説明はAstroがBiomeやCSTを採用したという意味ではありません。
-->

---
layout: default
class: body-center
clicks: 1
---

## Biomeと編集途中の入力を扱う

```js
while {}
```

<div v-click="1" class="mt-5 text-xl text-primary">括弧と条件式が欠けても、解析可能な範囲を扱う</div>

<Ref href="https://biomejs.dev/internals/architecture/#resilient-and-recoverable-parser">Biome ArchitectureとError recovery</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
Biomeの公式資料にある例です。欠けた構文を記録し、解析を継続します。Sourceを欠落なく保持する設計と、エラーから回復するparserの設計は別の観点です。回復できる範囲にも限界があります。
-->

---
layout: default
class: body-center
clicks: 1
---

## Astro Syntaxの仕様ドラフト

```astro
---
const name = "Astro";
---
<h1 class="title">{name}</h1>
<p>複数のルート要素</p>
```

<div v-click="1" class="mt-5 text-xl text-primary">Component script、HTML属性、式、複数ルートの規則を明文化</div>

<!--
まずコードを確認し、クリックで説明を表示します。
2026年2月付の構文仕様ドラフトでは、Astro固有の構文とJSXとの差分を整理しています。実装が扱う構文を共通の資料で確認できます。Source位置や編集途中の入力への対応は、ツールの要求と合わせて設計します。
-->

---
layout: default
class: body-center
clicks: 2
---

## Vue.js Amsterdam 2026 — Astro 6の発表

<div class="grid grid-cols-2 gap-10 mt-10 text-xl">
  <div class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-sm uppercase tracking-widest text-[#717781]">実装に利用する基盤</div>
    <div class="text-3xl font-600 mt-2">Oxc と Rust</div>
  </div>
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-sm uppercase tracking-widest text-[#717781]">実装を進めるための開発支援</div>
    <div class="text-3xl font-600 mt-2">Claude Code</div>
  </div>
</div>

<div v-click="2" class="mt-10 text-xl opacity-70">
  関連する試みとして、自分が取り組んでいた <b>xmdx</b> も紹介された
</div>

<!--
クリックごとに、次の項目を説明します。
Vue.js Amsterdam 2026 で Astro 6 が発表されました。そこでは Oxc と Rust の話、そして Claude Code を使った開発の話が出ました。2つの変化として整理できます。実装に利用する基盤としての Oxc と Rust、実装を進めるための開発支援としての Claude Code。そしてこの発表のなかで、関連する試みとして自分が取り組んでいた xmdx も紹介されました。ここから全体図の Content の経路へ視野を広げます。少し時間を戻して、2025年から自分が取り組んでいた Markdown と MDX の話をします。
-->

---
layout: default
class: body-center
clicks: 1
---

## MarkdownとMDX

```mdx
import Card from "./ProductCard.jsx";

# おすすめの商品

<Card name="Book" price={1200} />
```

<div v-click="1" class="mt-5 text-xl text-primary">Markdownの本文に、JSXやJavaScript式を記述できる</div>

<!--
まずコードを確認し、クリックで説明を表示します。
Content Processorが本文を解析し、表示用コードや情報へ変換します。Astro Compilerとは別の経路でBuildに渡します。
-->

---
layout: default
class: body-center
clicks: 2
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
  <div v-click="1">
    <div class="flex items-center justify-center gap-5">
      <logos-mdx class="text-6xl" />
      <img src="./images/logos/ferris.svg" alt="Rust" class="h-14" />
    </div>
    <div class="text-3xl font-600 mt-6">mdxjs-rs</div>
  </div>
</div>

<div v-click="2" class="mt-16 text-2xl text-primary">
  既存の基盤を組み合わせれば、Astroでも使えるのではないか
</div>

<Ref href="https://github.com/wooorm/mdxjs-rs">markdown-rsとmdxjs-rs</Ref>

<!--
クリックごとに、次の項目を説明します。
Markdown と MDX にも Rust の基盤がありました。markdown-rs が解析の基盤、mdxjs-rs が MDX を JavaScript へ変換するコンパイラです。mdxjs-rs は内部で markdown-rs と SWC を使っています。つまり、既存の基盤を組み合わせれば Astro でも使えるのではないか、と考えました。
-->

---
layout: default
class: body-center
clicks: 3
---

## 自分で試したRust製MDX Compiler

<div class="flex items-center gap-4 mb-6">
  <Status kind="poc" />
  <span class="text-xl opacity-70">2025年7月、Astroへ組み込むPoCを提案した</span>
</div>

<div class="grid grid-cols-3 gap-6 text-lg">
  <div v-click="1">
    <h3 class="opacity-100 !text-base">検証したかったこと</h3>
    <ul class="mt-2">
      <li>Buildが速くなるか</li>
      <li>既存のAstroプロジェクトで使えるか</li>
    </ul>
  </div>
  <div v-click="2">
    <h3 class="opacity-100 !text-base">互換性を調べたもの</h3>
    <ul class="mt-2">
      <li>frontmatter — ファイル冒頭のタイトルなどの情報</li>
      <li>見出しのslug — 見出しへのリンクに使うID</li>
      <li>画像と Astro component</li>
    </ul>
  </div>
  <div v-click="3">
    <h3 class="opacity-100 !text-base">最初の案</h3>
    <ul class="mt-2">
      <li>Rustで処理する経路を、利用者が選べるようにする</li>
      <li>対応できない場合は、既存のJavaScript実装へ戻す</li>
    </ul>
  </div>
</div>

<!--
クリックごとに、次の項目を説明します。
2025年7月に、これを Astro へ組み込む PoC を提案しました。PoC は小さな実装を作って実現できるかを確かめる試みです。検証したかったのはシンプルで、ビルドが速くなるか、そして既存の Astro プロジェクトでそのまま使えるか。frontmatter、見出しの slug、画像、Astro コンポーネント、それぞれの互換性を調べました。最初の案は、Rust で処理する経路を利用者が選べるようにして、対応できない場合は既存の JavaScript 実装へ戻す、というものでした。
-->

---
layout: default
class: body-center
clicks: 3
---

## 既存pluginとの接続が必要だった

<div class="mt-10 text-xl opacity-70">既存の処理は remark と rehype の plugin に依存していた</div>

<div class="mt-4 flex flex-wrap gap-4 text-xl">
  <span class="border border-[#E5E0EC] rounded-lg px-5 py-2"><code>remark-gfm</code></span>
  <span v-click="1" class="border border-[#E5E0EC] rounded-lg px-5 py-2"><code>remark-smartypants</code></span>
  <span v-click="2" class="border border-[#E5E0EC] rounded-lg px-5 py-2"><code>rehype-slug</code></span>
</div>

<div v-click="3" class="mt-10 border border-[#BC52EE] border-opacity-45 rounded-xl px-8 py-6" style="background: rgba(188, 82, 238, 0.06)">
  <p class="!my-0 text-3xl font-600">mdxjs-rs では、これらを実行できなかった</p>
</div>

<Ref href="https://github.com/wooorm/mdxjs-rs#when-should-i-use-this">mdxjs-rs — When should I use this?</Ref>

<!--
クリックごとに、次の項目を説明します。
ここで壁にぶつかりました。既存の処理は remark と rehype の plugin を使っています。GitHub 風の表を扱う remark-gfm、引用符を変換する remark-smartypants、見出しに ID を付ける rehype-slug。ところが検討した mdxjs-rs では、これらの既存 plugin を実行できませんでした。plugin が必要な構成では JavaScript 実装へ戻ることになるので、Rust の経路を使える範囲が限られてしまう。ここで分かったのは、利用者は解析結果だけでなく、途中で plugin を実行できることにも依存している、ということでした。
-->

---
layout: default
class: body-center
clicks: 2
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
  <div v-click="1" class="text-lg">
    <h3 class="opacity-100 !text-base">扱う構造</h3>
    <ul class="mt-2">
      <li><b>mdast</b> — MarkdownのAST</li>
      <li><b>hast</b> — HTMLのAST</li>
    </ul>
  </div>
</div>

<div v-click="2" class="mt-8 text-xl">
  <p class="text-primary">RustとJavaScriptを、処理ごとに使い分けられる</p>
  <p class="opacity-70">ASTを受け渡す境界も、設計する必要がある</p>
</div>

<!--
クリックごとに、次の項目を説明します。
そこで AST Bridge という分担を試しました。Rust で解析して、必要な段階で AST を JavaScript へ渡し、既存の remark と rehype の plugin で加工して、加工した AST を Rust へ戻してコード生成につなげる。扱う構造は Markdown の AST である mdast と、HTML の AST である hast です。試して分かったのは、Rust と JavaScript を処理ごとに使い分けられるということ。同時に、AST を受け渡す境界そのものも設計しないといけない、ということでした。
-->

---
layout: default
class: body-center
clicks: 1
---

## markdown-rsへの提案

```markdown
| 商品 | 価格 |
| --- | ---: |
| Book | 1200 |
| Pen | 200 |
```

<div v-click="1" class="mt-5 text-xl text-primary">GFMの表をASTからMarkdownへ戻す機能とWASM bindings</div>

<!--
まずコードを確認し、クリックで説明を表示します。
加工後のASTをMarkdownへ書き出す機能と、JavaScript環境から利用するためのWASM bindingsを提案しました。
-->

---
layout: default
class: body-center
clicks: 2
---

## mdxjs-rsへの提案

<div class="mt-10 text-2xl">
  <p>公式npm package</p><p v-click="1">Node.js向けのnative bindings</p>
  <p v-click="2" class="text-primary">JavaScriptから使うための共通の入口を提供する</p>
</div>

<!--
クリックごとに、次の項目を説明します。
前ページのmarkdown-rsへの提案と、こちらのmdxjs-rsへの提案を分けて紹介します。Astroなどの利用者が、JavaScriptからの入口をそれぞれ実装しなくてもよい形を目指しました。
-->

---
layout: default
class: body-center
clicks: 5
---

## communityとのやりとりで見えた条件

<div class="grid grid-cols-2 gap-x-10 gap-y-5 mt-8 text-xl">
  <div>
    <div class="text-primary font-600">配布方法</div>
    <div class="opacity-65 text-lg">WASMとNode-APIのどちらを使うか。両方に対応するか</div>
  </div>
  <div v-click="1">
    <div class="text-primary font-600">対応環境</div>
    <div class="opacity-65 text-lg">OSとCPUごとのバイナリを誰がビルドし、誰がテストして保守するか</div>
  </div>
  <div v-click="2">
    <div class="text-primary font-600">依存関係</div>
    <div class="opacity-65 text-lg">追加機能を全員に含めるか、必要な利用者だけが追加する形にするか</div>
  </div>
  <div v-click="3">
    <div class="text-primary font-600">pluginとの互換性</div>
    <div class="opacity-65 text-lg">既存のpluginを、どこまで利用できるようにするか</div>
  </div>
  <div v-click="4" class="col-span-2">
    <div class="text-primary font-600">汎用部分の担当</div>
    <div class="opacity-65 text-lg">Astro本体が持つか、開発元や独立したprojectが持つか</div>
  </div>
</div>

<div v-click="5" class="mt-8 text-2xl text-primary">実装を試すことで、速度以外の成立条件が具体的になった</div>

<!--
クリックごとに、次の項目を説明します。
コミュニティとのやりとりで、速度以外の条件が次々に出てきました。配布方法は WASM と Node-API のどちらか、あるいは両方か。OS と CPU ごとのバイナリを誰がビルドし、誰がテストして保守するのか。追加機能を全員の依存に含めるのか、必要な人だけが追加する形にするのか。既存 plugin をどこまで使えるようにするのか。そして汎用部分を Astro 本体が持つのか、開発元や独立したプロジェクトが持つのか。実装を試したからこそ、こういう条件が具体的になりました。
-->

---
layout: default
class: body-center
clicks: 1
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
  <div v-click="1">
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
クリックごとに、次の項目を説明します。
Astro のレビューを受けて、汎用的な Markdown と MDX の処理を独立したプロジェクトとして実装しました。xmdx です。Rust の処理を Node-API と WASM の両方で JavaScript から使えるようにして、Astro と Starlight 向けの integration を作りました。integration は Astro へ機能を組み込むための接続部分、Starlight は Astro を使ったドキュメントサイト向けの仕組みです。ここでもネイティブ実装、WASM、Astro との接続を別のパッケージに分けています。検証は実際の Astro Docs を使いました。既存のコンテンツを処理できるか、表示や機能の互換性を保てるか、ビルド時間がどう変わるか。
-->

---
layout: default
class: body-center
clicks: 5
---

## 複数の試みを比較できるようになった

<div class="flex gap-4 mt-6 text-2xl">
  <span class="border border-[#E5E0EC] rounded-lg px-4 py-1">xmdx</span>
  <span class="border border-[#E5E0EC] rounded-lg px-4 py-1">ox-content</span>
  <span class="border border-[#BC52EE] border-opacity-60 rounded-lg px-4 py-1 text-primary">Sätteri</span>
</div>

<div class="grid grid-cols-2 gap-x-10 gap-y-6 mt-12 text-2xl">
  <div v-click="1"><b>実際のBuildでの速度</b></div>
  <div v-click="2"><b>plugin model</b></div>
  <div v-click="3"><b>frameworkとの境界</b></div>
  <div v-click="4"><b>保守主体</b></div>
</div>

<div v-click="5" class="mt-8 text-xl text-primary">自分の試作とcommunityとの対話が、選ぶための判断材料になった</div>

<!--
クリックごとに、次の項目を説明します。
xmdx に加えて、ox-content などの Rust 製 Content 基盤についてもコミュニティで話しました。Sätteri も、要求に合う基盤を考えるうえでの選択肢になりました。比較できるようになったのは4点。実際のビルドでの速度、plugin がどの段階のどのデータを加工できるかという plugin model、Astro と Content 基盤の境界、そして誰が保守するのか。自分の試作とコミュニティとの対話が、選ぶための判断材料になりました。なぜ Sätteri を勧めるに至ったかは、第4章で説明します。
-->

---
layout: center
clicks: 2
---

<Overview
  subs="parser,oxc"
  :annotate="{
    ...($clicks >= 1 ? { compiler: 'Oxcなどの再利用できる基盤' } : {}),
    ...($clicks >= 2 ? { content: 'markdown-rs と mdxjs-rs、そして xmdx と ox-content と Sätteri' } : {}),
  }"
/>

<!--
クリックごとに、次の項目を説明します。
全体図に候補を添えます。JavaScript 解析の周囲には Oxc などの再利用できる基盤。ビルドの周囲には Vite と Rolldown。Content の周囲には解析と変換の基盤として markdown-rs と mdxjs-rs、Content 処理の選択肢として xmdx、ox-content、Sätteri。JavaScript とネイティブ実装の境界には Node-API と WASM の経路。そして Astro Syntax を確認する資料として構文仕様のドラフト。この図では、各領域の周囲に候補を添えているだけで、すべてを採用した図にはしていません。ライブラリと、それを組み込んだ Processor は区別してください。
-->

---
layout: default
class: body-center
clicks: 5
---

## 2021年から変わった判断材料

<div class="mt-8 text-xl leading-relaxed">
  <ul>
    <li>実装に利用できる <b>Rustの基盤</b> が増えた</li>
    <li v-click="1">JavaScriptから利用できる <b>packageや配布の選択肢</b> が増えた</li>
    <li v-click="2">ソースの構造を扱う <b>ツールの要求</b> が明確になった</li>
    <li v-click="3"><b>Astro Syntax を確認する資料</b> が整った</li>
    <li v-click="4">MarkdownとMDXでも、<b>実装を試して比較</b> できるようになった</li>
    <li v-click="5">Node.jsでの実行方法とBrowserへの配布方法を、<b>用途ごとに検討</b> できる</li>
  </ul>
</div>

<!--
クリックごとに、次の項目を説明します。
2021年から変わった判断材料をまとめます。実装に使える Rust の基盤が増えた。JavaScript から使えるパッケージと配布の選択肢が増えた。ソースの構造を扱うツールの要求が明確になった。Astro Syntax を確認する資料が整った。Markdown と MDX でも実装を試して比較できるようになった。そして実行方法と配布方法を用途ごとに検討できるようになった。
-->

---
layout: default
class: body-center
clicks: 2
---

## この章の結論

<div class="mt-12 text-2xl leading-relaxed">
  <p>2021年の判断を支えていた条件が、5年間で変わった</p>
  <p v-click="1">新しい要求に対して、再利用できる基盤と資料が増えた</p>
  <p v-click="2" class="text-primary">自分で試作し、communityと話すことで、選択肢を評価する条件も分かった</p>
</div>

<!--
クリックごとに、次の項目を説明します。
第3章の結論です。2021年の判断を支えていた条件が、5年間で変わりました。新しい要求に対して、再利用できる基盤と資料が増えた。そして自分で試作してコミュニティと話すことで、選択肢を評価するための条件も分かりました。
-->

---
layout: statement
class: flex flex-col justify-center h-full
clicks: 2
---

# その選択肢を使って、<br /><span v-click="1">Astroは何を自分たちで実装し、</span><br /><span v-click="2">何を既存の基盤に任せるのか</span>

<!--
クリックごとに、次の項目を説明します。
では、その選択肢を使って、Astro は何を自分たちで実装し、何を既存の基盤に任せるのか。第4章です。
-->

---
layout: section
clicks: 1
---

# 4. 新しい判断
<h2 v-click="1">その結果、責務をどう分け直したのか</h2>

<!--
クリックごとに、次の項目を説明します。
第4章。ここからは、責務をどう分け直したのかを見ていきます。
-->

---
layout: center
clicks: 3
---

<Overview
  subs="parser,oxc,astro-syntax"
  :roles="{
    ...($clicks >= 1 ? { editor: 'ソースの情報を、診断や補完につなげる' } : {}),
    ...($clicks >= 2 ? { build: '変換されたコードをまとめ、実行や配信につなげる' } : {}),
    ...($clicks >= 3 ? { content: 'MarkdownとMDXの解析と変換' } : {}),
  }"
/>

<!--
クリックごとに、Editor、Build、Contentの役割を説明します。
先に結論の図を出します。各領域が何を担当するか。Astro Compiler は Astro 固有の構文と変換、そしてその中の汎用的な解析には Oxc を使う。Build は変換されたコードをまとめて実行や配信につなげる。Editor のツールはソースの情報を診断や補完につなげる。Content Processor は Markdown と MDX の解析と変換。ブラウザは出力された HTML を解釈して DOM を構築する。
-->

---
layout: default
class: body-center
clicks: 3
---

## 判断の軸

<div class="grid grid-cols-2 gap-x-10 gap-y-6 mt-12 text-2xl">
  <div class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">どのソース情報を保持するか</div>
  <div v-click="1" class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">どの段階で補正や変換を行うか</div>
  <div v-click="2" class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">一般的な処理を、どの基盤へ任せるか</div>
  <div v-click="3" class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">Astroが、どの処理を実装して保守するか</div>
</div>

<!--
クリックごとに、次の項目を説明します。
判断の軸は4つです。どのソース情報を保持するか。どの段階で補正や変換を行うか。一般的な処理をどの基盤へ任せるか。そして Astro がどの処理を実装して保守するか。この4つで、HTML、JavaScript、Markdown と MDX の3つの具体例を見ていきます。
-->

---
layout: default
class: body-center
clicks: 1
---

## Rust Compilerとverbatim parsing

```html
<p>before<div>inside</div>after</p>
```

<div v-click="1" class="mt-5 text-xl text-primary"><code>div</code> を <code>p</code> の子として保持し、Source位置を提供する</div>

<Ref href="https://github.com/withastro/roadmap/issues/1356">Rust CompilerとRFC #1356</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
第2章の入力です。Go版のEditor向けAPIにもliteral parsingはありました。Rust版ではBuildを含めHTML correctionを行わない方針です。書かれた入れ子を保持しても、そのHTMLが妥当になるわけではありません。DOMの構築はBrowserが担当します。
-->

---
layout: default
class: body-center
clicks: 2
---

## Compilerが受け入れないものもある

<div class="mt-10 text-2xl leading-relaxed">
  <p>Rust版Compilerでは、<b>HTML correctionを行わない</b>方針が明示されている</p>
  <p v-click="1" class="opacity-70">一方、閉じ忘れたタグなどの構文エラーは拒否する</p>
  <p v-click="2" class="text-primary">どんな入力でも受け入れる、という意味ではない</p>
</div>

<Ref href="https://github.com/withastro/roadmap/issues/1356">withastro/roadmap#1356 — 新Compilerの正式提案</Ref>

<!--
クリックごとに、次の項目を説明します。
補足です。Rust 版コンパイラでは HTML correction を行わない方針が明示されています。ただし、閉じ忘れたタグなどの構文エラーは拒否します。何でも受け入れるという意味ではありません。
-->

---
layout: default
class: body-center
clicks: 2
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
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Browserが構築するDOM</div>
    <ul class="mt-3 text-lg">
      <li>出力されたHTMLを読み込んで作る構造</li>
      <li>表示やJavaScriptからの操作に使う</li>
    </ul>
  </div>
</div>

<div v-click="2" class="mt-8 text-xl leading-relaxed">
  <p class="opacity-70">同じ入れ子のHTMLをBrowserへ渡せば、BrowserではHTMLの規則に従って補正が起きる</p>
  <p class="text-primary">HTMLの補正方針は、GoかRustかとは別の設計判断</p>
</div>

<!--
クリックごとに、次の項目を説明します。
ここで分け直したのは3つの段階です。ソースを理解する段階、コードを生成する段階、そして HTML から DOM を構築する段階。同じ入れ子の HTML をブラウザへ渡せば、ブラウザでは HTML の規則に従って補正が起きます。それでいい。大事なのは、HTML の補正方針は Go か Rust かとは別の設計判断だということです。言語を変えたから補正をやめたのではなく、責務を分け直した結果です。
-->

---
layout: default
class: body-center
clicks: 1
---

## JavaScript ASTとGo版の表現

```json
{
  "type": "text",
  "value": "price * quantity"
}
```

<div v-click="1" class="mt-5 text-xl text-primary">ExpressionNodeの子の抜粋。識別子を扱うには追加の解析が必要</div>

<Ref href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#parse-astro-and-return-an-ast">Go Compiler 2.12.2とTextNode</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
第2章で確認したGo版の表現です。式のソースを取り出せます。次のページではRust版のparse APIが提供する式の内部ASTを確認します。
-->

---
layout: default
class: body-center
clicks: 1
---

## JavaScript ASTとRust版の表現

```json {*|4,5}
{
  "type": "BinaryExpression",
  "operator": "*",
  "left": { "type": "Identifier",
            "name": "price" }
}
```

<div v-click="1" class="mt-5 text-xl text-primary">左辺のみ抜粋。右辺と周囲のAstro ASTと位置情報は省略</div>

<Ref href="https://github.com/withastro/compiler-rs">Rust CompilerとESTree互換AST</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
Rust版のparse APIはESTree互換のASTを返します。実際のBinaryExpressionにはrightもあり、quantityを表すIdentifierです。このページでは左辺に注目しています。ASTで識別子を区別できても、参照先や型の判定は意味解析の仕事です。
-->

---
layout: default
class: body-center
clicks: 2
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
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-6">
    <h3 class="opacity-100 !text-base">Editor には、引き続き必要な処理がある</h3>
    <ul class="mt-2">
      <li>変数の宣言と使用箇所を対応させる</li>
      <li>型情報を調べる</li>
      <li>Astro固有構文とソース位置を扱う</li>
      <li>不完全な入力を扱う</li>
    </ul>
  </div>
</div>

<div v-click="2" class="mt-8 text-xl text-primary">ASTの提供は、診断や補完を作るための基盤になる</div>

<!--
クリックごとに、次の項目を説明します。
ツールから見た変化です。式の左辺と右辺をたどれる。演算子と識別子を個別に扱える。JavaScript の AST を扱う既存のツールと接続しやすくなる。ただし、これで Editor の仕事がなくなるわけではありません。変数の宣言と使用箇所の対応、型情報、Astro 固有構文とソース位置、不完全な入力。これらは引き続き Editor の仕事です。AST の提供は、診断や補完を作るための基盤になる、ということです。
-->

---
layout: default
class: body-center
clicks: 2
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
  <div v-click="1" class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
    <div class="text-2xl font-600">Astroが持つ部分</div>
    <ul class="mt-3 text-lg">
      <li>Astro固有の構文</li>
      <li>Template と JS の混在</li>
      <li>実行に必要な変換</li>
      <li>元のソースとの対応</li>
    </ul>
  </div>
</div>

<div v-click="2" class="mt-10 text-2xl">
  Rust版は、<b>Astro向けに拡張した Oxc</b> を利用する
</div>

<Ref href="https://github.com/withastro/compiler-rs/blob/main/Cargo.toml">compiler-rs — Cargo.toml</Ref>

<!--
クリックごとに、次の項目を説明します。
Oxc との責務分担です。Oxc に任せるのは、JavaScript と TypeScript の解析、式や識別子を表す AST、汎用的な変換やコード生成の基盤。Astro が持つのは、Astro 固有の構文、Template と JavaScript が混在する部分、Astro の実行に必要な変換、そして元のソースとの対応。Rust 版コンパイラは Astro 向けに拡張した Oxc を使っています。汎用部分を再利用しながら、必要な変更を加える。自分たちで実装して保守する範囲を絞るという判断です。
-->

---
layout: center
clicks: 3
---

<Overview
  highlight="compiler,editor,browser,parser,oxc,astro-syntax"
  subs="parser,oxc,astro-syntax"
  :annotate="{
    ...($clicks >= 1 ? { 'compiler->editor': '書かれた構造とソース位置、埋め込まれたJavaScriptのAST' } : {}),
    ...($clicks >= 2 ? { browser: '出力HTMLからDOMを構築' } : {}),
  }"
/>

<div v-click="3" class="text-center text-2xl text-primary mt-2">Compilerを「less clever」にする</div>

<!--
クリックごとに、次の項目を説明します。
全体図に戻ります。コンパイラと Editor の間には、書かれた構造とソース位置、そして埋め込まれた JavaScript の AST。コンパイラの中には、Oxc を使った汎用的な解析と、Astro 固有の構文と変換。ブラウザには、出力 HTML から DOM を構築する役割。この方向性を一言でいうと、コンパイラを less clever にする、ということです。暗黙に補正する範囲を減らして、解析と変換と後続処理の境界を明確にする。
-->

---
layout: default
class: body-center
clicks: 2
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
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-6">
    <div class="text-2xl font-600">Processorが担当すること</div>
    <ul class="mt-3 text-lg">
      <li>MarkdownとMDXの構文</li>
      <li>Content固有の変換</li>
      <li>拡張機能を実行する仕組み</li>
    </ul>
  </div>
</div>

<div v-click="2" class="mt-8 text-xl text-primary"><code>.astro</code> Compilerとは、別の処理系として選ぶ</div>

<!--
クリックごとに、次の項目を説明します。
Content の話に戻ります。第3章で、Rust 製 MDX コンパイラの PoC と plugin 互換性の問題を見ました。ここで決めたのは、Markdown と MDX を担当する場所です。Astro が担当するのは、Processor を接続する入口を用意することと、Content Collections やビルドと接続すること。Processor が担当するのは、Markdown と MDX の構文、Content 固有の変換、拡張機能を実行する仕組み。そして .astro のコンパイラとは、別の処理系として選ぶ。
-->

---
layout: default
class: body-center
clicks: 1
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
  <div v-click="1">
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
クリックごとに、次の項目を説明します。
Sätteri の設計です。Rust を中心に Markdown と MDX を処理して、よく使う処理を標準機能として提供する。そのうえで、JavaScript で独自の変換を追加できる。plugin との境界はこうです。plugin が扱いたいノードの種類を指定して、そのノードを処理する関数を JavaScript で実行し、必要な情報だけを境界で受け渡す。visitor というのは、特定の種類のノードを受け取って調べたり変更したりする関数のことです。見出しだけを処理する、リンクだけを処理する、といった書き方になります。
-->

---
layout: default
class: body-center
clicks: 1
---

## unifiedの設定とimport

```js
import { defineConfig } from "astro/config";
import { unified }
  from "@astrojs/markdown-remark";

const contentProcessor = unified();
```

<div v-click="1" class="mt-5 text-xl text-primary">既存のremarkとrehype pluginを使うための選択肢</div>

<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Astro DocsとMarkdown Processors</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
必要なパッケージを導入したうえで、unifiedのProcessorを作ります。次のページでAstroの設定に指定します。
-->

---
layout: default
class: body-center
clicks: 1
---

## unifiedの設定とProcessorを指定する

```js
export default defineConfig({
  markdown: {
    processor: contentProcessor,
  },
});
```

<div v-click="1" class="mt-5 text-xl text-primary">前ページの続き。Astroが選択したProcessorへ本文を渡す</div>

<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Astro DocsとMarkdown Processors</Ref>

<!--
まずコードを確認し、クリックで説明を表示します。
AstroはProcessorを呼び出し、ProcessorはContentを解析して変換します。既存pluginを利用する経路を明示的に選べます。
-->

---
layout: default
class: body-center
clicks: 2
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
  <div v-click="1">
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

<div v-click="2" class="mt-8 flex gap-4 items-center">
  <span class="text-lg opacity-60">スライドには、対象バージョンと状態を添える</span>
  <Status kind="adopted" />
  <Status kind="wip" />
  <Status kind="proposed" />
  <Status kind="poc" />
</div>

<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Markdown Processors — Astro Docs</Ref>

<!--
クリックごとに、次の項目を説明します。
ここは混同しやすいので分けて話します。自分が PoC として試したのは、Rust 製 MDX コンパイラの統合と、AST Bridge による既存 plugin との接続です。実際に採用されたのは、Astro 6.4 で Markdown Processor を選ぶ仕組みが追加されたこと、Astro 7 で Sätteri が標準 Processor になったこと、そして unified を選ぶ経路も用意されていること。提案した内容と、採用された内容は別です。
-->

---
layout: default
class: body-center
clicks: 1
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
  <div v-click="1">
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
クリックごとに、次の項目を説明します。
xmdx から Sätteri を勧める判断についてです。xmdx の検証で、速度、plugin との接続、Astro への統合、配布と継続的な保守、という条件が具体的になりました。その条件があったから、ほかの実装も比較できるようになった。そして Astro の要求に合う実装として Sätteri を勧める判断につながりました。xmdx の README でも Sätteri の利用を案内しています。PoC から残ったものは、実際に試して分かった制約、選択肢を比較するための判断材料、そして upstream とコミュニティとの関係です。自分の実装が採用されること以外にも、次の判断につながる成果があります。
-->

---
layout: default
class: body-center
clicks: 4
---

## 実装言語と、配布方法を分けて考える

<div class="grid grid-cols-4 gap-5 mt-8 text-lg">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">実装言語</div>
    <div class="opacity-65 mt-2">どの言語で処理を書くか</div>
  </div>
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">配布と実行方法</div>
    <div class="opacity-65 mt-2">どの環境で、その処理を動かすか</div>
  </div>
  <div v-click="2" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">AST設計</div>
    <div class="opacity-65 mt-2">ソースをどの構造で表し、何を保持するか</div>
  </div>
  <div v-click="3" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">責務の所有</div>
    <div class="opacity-65 mt-2">どのprojectが実装して保守するか</div>
  </div>
</div>

<div v-click="4" class="mt-8 text-xl leading-relaxed">
  <p class="text-primary">これらは、それぞれ別の判断になる</p>
  <p class="opacity-70">Node.js向けには native bindings。Browser内でCompilerを動かす場合はWASMの経路を考える</p>
  <p class="opacity-60 text-lg">全体図のBrowserは、生成されたサイトを表示する場所。Compiler自体をBrowser内で実行する話とは区別する</p>
</div>

<Ref href="https://github.com/withastro/compiler-rs">Rust版Compiler READMEとbindingsの構成</Ref>

<!--
クリックごとに、次の項目を説明します。
第1章の「分けて考える選択」に戻ります。実装言語、配布と実行方法、AST 設計、責務の所有。この4つはそれぞれ別の判断です。Node.js 向けには native bindings を使い、ブラウザ内でコンパイラを動かす場合は WASM の経路を考える。Rust 版の実装にも WASM 向けの経路があります。提供する環境と API は実装ごとに確認してください。ひとつ注意点として、全体図のブラウザは生成されたサイトを表示する場所であって、コンパイラ自体をブラウザ内で実行する話とは区別しています。
-->

---
layout: center
clicks: 3
---

<Overview
  subs="parser,oxc,astro-syntax"
  :annotate="{
    ...($clicks >= 1 ? { compiler: 'parse() でASTを提供し、transform() でJavaScriptへ変換する' } : {}),
    ...($clicks >= 2 ? { editor: 'ASTとソース位置から、診断と補完を提供する' } : {}),
    ...($clicks >= 3 ? { content: 'frontmatter と見出しID、コードの色付け、MDX component' } : {}),
  }"
/>

<!--
クリックごとに、次の項目を説明します。
最後の全体図です。Astro Compiler は Astro Syntax を解析し、ソース構造と位置を保持し、parse() で AST を提供し、transform() で HTML 生成用の JavaScript へ変換する。汎用的な解析には Oxc を使う。Editor は AST とソース位置を利用して、不完全な構文を扱いながら診断と補完を提供する。Build はモジュールを解決して JavaScript と CSS をまとめる。Vite とその内部の Rolldown を使いますが、この分担は Go 版の導入時から存在していました。Astro の Content は Processor を選べる統合点を提供して、Content Collections とビルドへ接続する。Content Processor は Markdown と MDX を解析して変換し、frontmatter や見出しの ID、コードの色付け、MDX component を扱い、汎用的な機能と plugin model を保守する。unified ecosystem は既存 plugin が必要な利用者の経路を担う。なお Rust 版コンパイラの公開 API は parse() と transform() を中心に説明できます。Language Server 向けの TSX 出力は、実行用コンパイラとは別の要件として扱われています。
-->

---
layout: default
class: body-center
clicks: 2
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
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">JavaScript</div>
    <div class="text-2xl font-600 mt-1">構造と再利用</div>
    <ul class="mt-3">
      <li>式の内部をASTとして提供する</li>
      <li>汎用的な解析にはOxcを利用する</li>
    </ul>
  </div>
  <div v-click="2" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">Markdown と MDX</div>
    <div class="text-2xl font-600 mt-1">互換性と所有</div>
    <ul class="mt-3">
      <li>pluginとの接続も要件に含める</li>
      <li>Astroとの統合と、汎用的なContent処理を分ける</li>
    </ul>
  </div>
</div>

<!--
クリックごとに、次の項目を説明します。
3つの具体例を並べます。HTML は保持と補正の話。書かれた構造を保持して、コンパイラの解析とブラウザの DOM 構築を区別する。JavaScript は構造と再利用の話。式の内部を AST として提供して、汎用的な解析は Oxc に任せる。Markdown と MDX は互換性と所有の話。plugin との接続も要件に含めて、Astro との統合と汎用的な Content 処理を分ける。
-->

---
layout: center
clicks: 3
---

<Overview
  subs="parser,oxc,astro-syntax"
  :contract="$clicks === 0 ? '' : $clicks === 1 ? 'source' : $clicks === 2 ? 'source,output' : 'source,output,ecosystem'"
/>

<!--
クリックごとに、次の項目を説明します。
3つの契約で整理します。まず「契約」というのは、処理をつなぐ相手へどんな情報や振る舞いを保証するか、という意味で、この講演で設計を整理するために使っている呼び方です。Source contract は主にコンパイラと Editor の間。書かれた構造と位置を保持し、埋め込まれた構文をツールが利用できる形で渡す。Output contract はコンパイラとビルドとブラウザの間。実行や表示につながる成果物を生成し、ソースの構造と最終的な表示の構造を区別する。Ecosystem contract は Content Processor と plugin ecosystem の間。既存 plugin を利用できる経路を維持し、新しい plugin model への移行方法を用意する。
-->

---
layout: default
class: body-center
clicks: 4
---

## この章の結論

<div class="mt-10 text-xl leading-relaxed">
  <ul>
    <li>Rustへの移行では、<b>Compilerの設計と保守範囲</b> も見直している</li>
    <li v-click="1">汎用的な処理には、<b>既存の基盤</b> を利用する</li>
    <li v-click="2">Astroは、<b>Astro固有の構文と変換と統合</b> を担当する</li>
    <li v-click="3">用途に応じて、<b>RustとJavaScriptの役割</b> を分ける</li>
    <li v-click="4"><code>.astro</code> Compiler と Markdown と MDX の Processor も、それぞれの要件に合った構成を選ぶ</li>
  </ul>
</div>

<!--
クリックごとに、次の項目を説明します。
第4章の結論です。Rust への移行では、コンパイラの設計と保守範囲も見直しています。汎用的な処理には既存の基盤を使い、Astro は Astro 固有の構文と変換と統合を担当する。用途に応じて Rust と JavaScript の役割を分ける。そして .astro のコンパイラと、MarkdownとMDX の Processor も、それぞれの要件に合った構成を選ぶ。
-->

---
layout: statement
class: flex flex-col justify-center h-full
clicks: 1
---

# 動いていたGoコンパイラを、<br /><span v-click="1">AstroはなぜRustで書き直したのか？</span>

<!--
クリックごとに、次の項目を説明します。
最初の問いに戻ります。
-->

---
layout: default
class: body-center
clicks: 3
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
  <div v-click="1" class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">発見した問題</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>ソース構造と位置への要求</div>
      <div>HTML補正による予想しにくい挙動</div>
      <div>独自実装の保守コスト</div>
    </div>
  </div>
  <div v-click="2" class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">前提の変化</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>Rust基盤の成熟</div>
      <div>再利用できる範囲の拡大</div>
      <div>Astro Syntax の整理</div>
    </div>
  </div>
  <div v-click="3" class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">
    <div class="text-sm uppercase tracking-widest text-[#717781]">新しい判断</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>保持する情報と変換する段階の明確化</div>
      <div>保守範囲を絞る</div>
      <div>改善し続けられる設計へ</div>
    </div>
  </div>
</div>

<!--
クリックごとに、次の項目を説明します。
4章ぶんの答えです。当時の判断は、高速な変換と複数環境での実行が必要で、Go と WASM がその要件に対応していた。発見した問題は、ソース構造と位置を扱う要求が明確になったこと、HTML 補正が不具合や予想しにくい挙動につながったこと、そして独自実装を継続して保守する難しさ。前提の変化は、Rust の解析と変換基盤が育ち、汎用的な処理を再利用できる範囲が広がり、Astro Syntax の整理も進んだこと。新しい判断は、保持する情報と変換する段階を明確にして、既存基盤を使って自分たちの保守範囲を絞り、チームが継続して改善できるコンパイラへ作り直すこと。Content での取り組みも、同じ責務設計の問題を別の処理経路で検証したものでした。
-->

---
layout: center
class: text-center
clicks: 2
---

<div class="text-5xl font-700 leading-[1.5]" style="color: #7611A6">
  既存の基盤を再利用し、<br />
  <span v-click="1">自分たちが持つ処理を絞り、</span><br />
  <span v-click="2">保守し続けられる設計にするため。</span>
</div>

<!--
クリックごとに、次の項目を説明します。
一言でいうとこうなります。Rust の基盤を再利用しながら、Astro が持つべき処理を絞り、継続して保守できるコンパイラへ再設計するため。速いから、ではありません。
-->

---
layout: default
class: body-center
clicks: 3
---

## 持ち帰ってほしいこと

<div class="mt-8 text-2xl text-primary">技術選定は、その時点の要件と利用できる基盤に対する判断</div>

<div class="mt-8 text-xl">
  <h3 class="opacity-100 !text-base">技術を選び直すときに確認すること</h3>
  <ul class="mt-3">
    <li>当時、何を実現するために選んだのか</li>
    <li v-click="1">利用が広がり、何が新しく必要になったのか</li>
    <li v-click="2">今なら、どの処理を既存基盤へ任せられるのか</li>
    <li v-click="3">自分たちが実装して保守するべき処理は何か</li>
  </ul>
</div>

<div class="mt-8 text-xl leading-relaxed">
  <p>技術を選び直す機会に、<b>担当する責務も見直す</b></p>
  <p class="opacity-70">PoCがmergeされなくても、制約を明らかにし、communityの次の判断につなげられる</p>
</div>

<!--
クリックごとに、次の項目を説明します。
持ち帰ってほしいことです。技術選定は、その時点の要件と利用できる基盤に対する判断です。だから、選び直すときに確認すべきことは4つ。当時、何を実現するために選んだのか。利用が広がって、何が新しく必要になったのか。今ならどの処理を既存基盤へ任せられるのか。そして、自分たちが実装して保守するべき処理は何か。技術を選び直す機会は、担当する責務を見直す機会でもあります。最後にもうひとつ。PoC がマージされなくても、制約を明らかにして、コミュニティの次の判断につなげることはできます。
-->

---
layout: center
class: text-center
clicks: 1
---

## ありがとうございました

<div class="mt-8 text-xl opacity-60">Astro Japan Community</div>

<img v-click="1" src="./images/qrcode_discord.com.png" class="h-60 mx-auto mt-6" alt="Discord QR Code" />

<!--
クリックごとに、次の項目を説明します。
ありがとうございました。Astro Japan Community の Discord です。よかったら覗いてみてください。
-->
