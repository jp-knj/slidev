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

<div class="text-2xl text-black font-400">Astro Compiler</div>

<h1 class="!text-6xl !font-700 mt-4 leading-tight">
  動いていたものを、<br />なぜ書き直すのか
</h1>

<div class="text-xl text-black mt-8">
  GoとWASMからRustへ、5年ぶんの前提の変化
</div>

<!--
こんにちは。今日は、動いていたものをなぜ書き直すのかを、Astro のコンパイラを題材に話します。2021年に Go と WASM で書かれたコンパイラが、2026年に Rust で書き直されました。その判断の中身を、4つの章に分けて追いかけます。
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
今日の問いは、動いていた Go コンパイラを、Astro はなぜ Rust で書き直したのかです。速さに加えて、何が問題で、何が変わって、どう責務を分け直したのかを確認します。
-->

---
layout: default
class: body-center
---

## 話すこと

<div class="grid grid-cols-1 gap-4 mt-10">
  <div>
    <div class="text-3xl font-600 mt-1">1. 当時の判断</div>
    <div class="text-lg mt-2">なぜ最初にGoとWASMを選んだのか</div>
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

<div class="text-center text-xl mt-2">Astro 0.x の出発点</div>

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
2021年は、Rome が Rust への書き直しを発表し、Parcel 2 と Next.js 12 が Rust 製のコンパイラを採用した年です。同時に、Vite 2 は Go 製の esbuild を使い、Turborepo も Go でした。Rust の採用が進むなかでも、Go を選ぶことは珍しい判断ではありませんでした。
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

<div class="mt-10 flex justify-center gap-10 text-lg ">
  <div>Build のための Compiler だった</div>
  <div>主な入口は <code>transform</code> API</div>
</div>

<div class="mt-12 border-l-2 border-[#BC52EE] pl-5">
  <div class="text-2xl font-600 text-primary">深く考えすぎずに選んだ</div>
  <div class="text-xl mt-2">esbuild が Go だった。Go は学びやすかった。</div>
</div>

<Ref href="https://natemoo.re/posts/hello-from-the-other-side/">Nate Moore: Hello from the other side</Ref>

<!--
Svelte のコンパイラの fork を、ここで Go に置き換えます。JavaScript からは WASM を介して呼び出し、ビルドは Snowpack から Vite に任せました。当時のコンパイラはビルドを目的としていて、主な入口は transform API ひとつ。ソースを受け取り、実行できる JavaScript を返すのが役割でした。
選んだ理由は本人がこう書いています。esbuild が Go で書かれていたこと、Go が学びやすかったこと。深く考えすぎずに選んだ、と。そして esbuild を参考に Go を学んで、HTML5 のパーサを Astro 向けに拡張した。ここで HTML5 パーサをベースにしたことが、第2章の話につながります。
-->

---
layout: default
class: body-center
---

## 分けて考える選択

<div class="grid grid-cols-3 gap-6 mt-10 text-xl">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-black">実装言語</div>
    <div class="text-2xl font-600 mt-2">Go か Rust か</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-black">配布と実行</div>
    <div class="text-2xl font-600 mt-2">ネイティブバイナリか WASM か</div>
  </div>
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-black">置き換える範囲</div>
    <div class="text-2xl font-600 mt-2">全体か、重い解析や変換だけか</div>
  </div>
</div>

<div class="mt-10 text-xl ">
  どの選択でも、JavaScript との境界には WASM の呼び出しや JSON 変換のコストが伴う
</div>

<!--
選択は3つに分かれます。実装言語をどうするか。どう配布して、どこで動かすか。そして、全体を置き換えるのか、時間のかかる解析や変換だけを置き換えるのか。この3つは独立に決められます。どの選択でも、JavaScript との境界には WASM の呼び出しや JSON 変換のコストが伴います。第4章でもこの判断の軸を使います。
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

<div class="mt-8 text-xl ">
  この判断を失敗として扱うのではなく、当時の要件に対する選択として扱う
</div>

<!--
Go はコンパイラの実装要件に、WASM は配布と実行環境の要件に合っていました。2021年の Astro にとって合理的だった選択が、要件の変化に伴って見直された、というのが第1章の結論です。
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

<div class="text-center text-xl mt-2">Editor のツールと Content の経路が増えた</div>

<!--
全体図に登場人物が増えました。Editor のツール、つまり ESLint や Language Server や Formatter が、同じコンパイラを使うようになりました。MarkdownとMDX の経路も加わっています。この章では、HTML の親子関係と埋め込まれた JavaScript を確認します。Content の経路は、第3章の後半で説明します。
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
  <div v-if="$clicks === 1"><span class="text-primary font-600">Template</span><br />HTML を基礎に、expression（JavaScriptの式）や<br />コンポーネントを書ける</div>
  <div v-if="$clicks === 2"><span class="text-primary font-600">{ }</span><br />JavaScript expressionの結果を、その場所に表示する</div>
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
Astro の構文をおさらいします。初めに三本線で囲まれた Component script を示します。1クリック目で Template、2クリック目で波かっこに埋め込んだ JavaScript expressionを示します。
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
  <a href="https://github.com/withastro/astro/issues/6011">astro#6011: 要素間の空白テキストノード</a>
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
  <div class="text-2xl">Compilerの変換で、<b>表の後の見出しが表の中に入った</b></div>
</div>
</Transition>

</div>

<Ref href="https://github.com/withastro/compiler/issues/870">compiler#870</Ref>

<!--
最初は書いたAstroを確認します。1回目のクリックで、報告された生成HTMLを右に表示します。2回目で問題を整理します。
compiler#870の報告当時、Build向けの変換でtableの後のh2がtableの中に入る不具合がありました。この結果をHTML仕様どおりとは説明しません。Compilerが生成するHTMLと、BrowserがそのHTMLから作るDOMは区別します。
DOMは、Browserが表示のために作るHTMLの木です。HTML5の補正は、HTMLの規則に従って要素の移動や追加を行うことです。補正後の親子関係だけを見ても、書かれた入れ子は分かりません。たとえばpの中にdivを書くと、divの開始でpが閉じられます。補正後の木からは、元の入れ子を診断できません。
ここまでの例から、Astro Syntaxに必要な規則を振り返ります。
-->

---
layout: default
class: ch2-detail
---

## Astro Syntaxを振り返る

<div class="ch2-reflection">
  <div><strong>HTMLらしさ</strong><p>HTMLに似た構文と、利用者が期待する挙動</p></div>
  <div><strong>空白の扱い</strong><p>ブラウザで空白になる改行を、<br />Astro Syntaxの規則で扱えないか</p></div>
  <div><strong>HTML5パーサー<br />固有のふるまい</strong><p>タグの補完や入れ子の補正まで、<br />Astroで採用する必要があるか</p></div>
</div>
<div class="ch2-next-question">HTML5パーサーは必要なのか？</div>

<!--
13枚目の属性と14枚目の空白と15枚目の不具合を振り返ります。HTMLに似た構文を解析することと、Browserと同じHTMLの補正を採用することは別の判断です。
改行を含む空白の表示は、HTMLの補正とは別の論点です。Astro Syntaxでどの規則を採用するかという問いであり、空白の仕様が変更済みだという説明ではありません。
tableの後のh2がtableの中に入った例は、Compilerの不具合です。HTML5の正しい挙動として説明しません。Rustへの移行だけで、これらの課題をすべて解決できるという説明もしません。
次は、Go版Compilerの情報を各ツールがどう利用していたかを確認します。
-->

---
layout: default
class: ch2-detail ch2-api-slide
---

## `parse()`と`convertToTSX()`を使うツールの役割

<div class="ch2-api-map" aria-label="Go CompilerのAPIから各ツールへの分岐">
  <div class="ch2-api-node ch2-api-parse"><strong><code>parse()</code></strong><span>Astro ASTと位置情報</span></div>
  <svg class="ch2-api-fork" viewBox="0 0 60 220" preserveAspectRatio="none" aria-hidden="true"><path d="M0 110 H25 V55 H55 M25 110 V165 H55 M47 50 L55 55 L47 60 M47 160 L55 165 L47 170" /></svg>
  <div class="ch2-api-consumer"><strong>Linter</strong><span>expressionを再解析し、宣言と参照を検査する</span></div>
  <div class="ch2-api-consumer"><strong>Formatter</strong><span>expressionを再解析し、空白と改行を整える</span></div>
  <div class="ch2-api-node"><strong><code>convertToTSX()</code></strong><span>Virtual TSXとSource map</span></div>
  <svg class="ch2-api-arrow" viewBox="0 0 60 110" preserveAspectRatio="none" aria-hidden="true"><path d="M0 55 H55 M47 50 L55 55 L47 60" /></svg>
  <div class="ch2-api-consumer"><strong>Language Toolの型解析</strong><span>TypeScriptの補完と診断を<br />元のAstroへ対応させる</span></div>
</div>

<Ref href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/cmd/astro-wasm/astro-wasm.go#L251-L284">Go Compilerのparse()とconvertToTSX()</Ref>

<!--
architecture/docs/drafts/astro-go-compiler-internals-and-consumers.mdのAPIと用途の対応表を参照しています。資料はCompiler 3.0.0、続く実測例はCompiler 2.12.2です。
parseはAstro ASTと位置情報を返し、astro-eslint-parserとprettier-plugin-astroが利用します。Linterは宣言と参照を検査し、Formatterは空白と改行を決めます。expressionの再解析については後の具体例で確認します。
convertToTSXはTypeScriptが解析できるコードとSource mapを返します。この図のLanguage Toolは型解析の経路です。HTML属性の補完は別にVirtual HTMLを使います。
Go Compilerの二つの解析モードも区別します。TokenizerとParserの実装は共通です。transform()はLiteral modeを指定せず、parse()とconvertToTSX()はParseOptionEnableLiteral(true)を指定します。Literal modeはHTMLの補正を抑え、書かれた入れ子を保持します。各APIは個別にParserを呼び、返す形式を選びます。一度の解析結果を三つのAPIで共有する図ではありません。
transform()はBuild向けの実行コードを生成します。parse()とconvertToTSX()はEditor向けにも使われます。この違いは2.12.2と、資料の3.0.0の固定コミット8870738a46baf6e639b1fab61e9e443b5e5df8f0で確認しています。
-->

---
layout: default
class: ch2-detail ch2-nesting-slide
clicks: 3
---

## expressionのASTと正確な位置を<br />ツールへ提供できていたか？

<div class="ch2-nesting-cols">
<div class="ch2-source-regions" aria-label="Astroの言語領域">
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
<div class="ch2-tree" aria-label="Component scriptとTemplateは同じ階層">
  <div class="ch2-tree-root">.astro</div>
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
<div class="ch2-note">Astro Syntaxには、expressionの中のMarkupと、Markupの中のexpressionがある</div>

<!--
左は13枚目のproducts.mapを簡略化した例です。Component scriptとTemplateは同じ階層です。TemplateのexpressionにMarkupがあり、そのMarkupに再びexpressionがあります。
三回のクリックでTemplate直下のexpression、liのMarkup、product.nameのexpressionを順に強調します。コードと図の色が対応します。
右はSourceに含まれる言語領域の図であり、Go Compilerが返すASTのNode名を示す図ではありません。Go版はAstro ASTを返し、expressionの子にelementを含めることができ、Markupの入れ子を保持します。公開ASTには、JavaScript expressionの変数名と演算子を表すAST nodeがありません。次の例で公開ASTを確認します。
-->

---
layout: default
class: ch2-detail
---

## Compilerが返すexpression

<div class="ch2-cols">
<div>
<div class="ch2-label">Astro Source</div>

```astro
---
const price = 10;
const amount = 3;
---

<p>{price * amount}</p>
```

</div>
<div>
<div class="ch2-label">Go Compilerの公開AST</div>

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
<div class="ch2-summary">変数名と演算子を、個別のASTノードとしてたどれない</div>

<Ref href="https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/README.md#parse-astro-and-return-an-ast">Compiler 2.12.2と公開AST</Ref>

<!--
左のコードは5行目に空行があり、末尾はLFです。priceとamountはともに宣言されています。
右はparse(source, { position: true })の返却値から、expressionとその子を抜粋したものです。Astro ASTはexpressionの範囲を表し、TextNode.valueにprice * amountという文字列を持ちます。変数名を表すIdentifierや、掛け算を表すBinaryExpressionは、この公開ASTにはありません。
この枚では、expressionの中身が文字列であることだけを伝えます。Compiler 2.12.2で検証しています。
-->

---
layout: default
class: ch2-detail
clicks: 2
---

## コードから変数名と演算子を取得する

<div class="ch2-cols ch2-expression-cols">
<div>
<div class="ch2-label flex items-center gap-2"><logos-astro-icon class="w-6 h-6" />Astro Source</div>

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
<div class="ch2-label">Linter独自のVirtual TSX</div>

```tsx
const price = 10;
const amount = 3;
<>
  <p>{price * amount}</p>
</>;
```

<div class="ch2-note">EspreeでJavaScriptとして解析する</div>
</div>
<div v-else>
<div class="ch2-label">Espreeで解析したAST</div>
<div class="ch2-expression-ast" role="img" aria-label="price * amount全体はBinaryExpression。operatorは掛け算の*。leftはpriceのIdentifier、rightはamountのIdentifier。">
  <div class="ch2-expression-root">
    <strong><code>BinaryExpression</code></strong>
    <div><code>price * amount</code> 全体</div>
    <div>二つの値の間に演算子があるexpression</div>
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
<div v-if="$clicks < 2" class="ch2-summary"><code>astro-eslint-parser</code> がJavaScriptパーサーへ渡すコードを作る</div>
<div v-else class="ch2-summary">変数名と演算子をASTの項目として取得できる</div>

<!--
Go版Compilerの公開ASTでは、price * amountの中身は文字列でした。変数名や演算子を個別に扱うには、JavaScriptとして解析する必要があります。

クリック1でVirtual TSXを表示します。astro-eslint-parserが、右のVirtual TSXを作ります。これはJavaScriptのParserへ渡すためのコードです。この例では、EspreeというParserで解析します。

クリック2で右列をAST図へ切り替えます。price * amount全体がBinaryExpressionになっています。二つの値の間に演算子があるexpressionを表すnodeです。
そのoperatorが掛け算の*です。leftにはprice、rightにはamountを表すIdentifierがあります。Identifierは、ここでは参照している変数名を表します。
これでツールは、変数名と演算子をASTの項目として取得できます。

補足。CompilerのconvertToTSX()とは別の変換です。この例はJavaScriptとJSXだけで表せるため、検証ではEspreeを使います。Component scriptの区切りを外し、TemplateをFragmentで囲みます。実装は区切りを除いた位置にセミコロンを挿入するなどの調整も行います。表示用の抜粋では、そのセミコロンと一部の空行を省き、Fragment内を字下げしています。図はexpressionの部分を抜粋し、位置などの項目を省略しています。

参照: [astro-eslint-parser 1.2.2とprocessTemplate](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/process-template.ts)
-->

---
layout: default
class: ch2-detail
---

## 元のAstroの正確な位置を求める

<div class="ch2-label">6行目の文字オフセット</div>
<pre class="ch2-ruler">十の位  44444555555555566666666
一の位  56789012345678901234567
文字    &lt;p&gt;{price * amount}&lt;/p&gt;</pre>

<div class="ch2-ranges">
  <div><span class="ch2-label">Compilerが返す位置</span><code>start: 47, end: 80</code><span>開始と終端が不正確</span></div>
  <div><span class="ch2-label">補正後のexpression</span><code>[48, 64)</code><span><code>{price * amount}</code></span></div>
  <div><span class="ch2-label">元のAstroでの変数名</span><code>[49, 54)</code><span><code>price</code> の5文字</span></div>
</div>
<div class="ch2-summary">1. <code>fixLocations</code> でAstro expressionの範囲を補正する<br />2. <code>restore</code> でVirtual TSXのASTの位置を元のAstroへ戻す</div>
<div class="ch2-note">Rangeは0始まりで終端を含まない</div>

<Ref href="https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/astro-parser/parse.ts">astro-eslint-parser 1.2.2とfixLocations</Ref>

<!--
ASTを取得できたら、次は診断を表示する場所です。Editorで名前に下線を引くには、元のAstroの何文字目なのかが必要になります。ここには二つの調整があります。

一つ目は、Astro expressionの範囲の補正です。この例のCompilerは開始47、終端80を返しています。しかし、波かっこを含む実際の範囲は48から64です。位置情報はありますが、そのまま使える値ではありません。
このバージョンでは、expressionにもHTMLタグ用の位置計算が適用されていました。そのため、astro-eslint-parserが元のソースを確認して、fixLocationsで範囲を補正します。

二つ目は、Virtual TSXで解析したASTの位置を、元のAstroの位置へ戻すことです。前の枚の右に示したコードは変換後のコードなので、その位置をそのままEditorへ渡せません。restoreで元のAstroへ対応させると、掛け算に使われているpriceは49から54の範囲になります。JavaScriptの識別子を解析するのはJavaScriptパーサーです。

補足。Compiler 2.12.2の内部ではexpressionもElementNodeで表します。公開ASTを作るpositionAtは、expressionを区別せず、HTMLタグ用の位置計算を行います。開始位置は48 - 1 = 47です。終端位置は63 + 16 + 1 = 80です。16は内部のn.Dataに入る文字列astro:expressionの長さです。タグ名の長さを使う計算がexpressionにも適用されています。
前のコードの空行と末尾のLFを含めて数えた値です。開始の波かっこは48、閉じ波かっこは63にあり、波かっこを含むAstro expressionの範囲は[48, 64)です。priceは[49, 54)です。CompilerのREADMEも、一部の位置が不正確であることを明記しています。
この例はASCIIなので、UTF-8のbyteとUTF-16の文字オフセットの値が一致します。一般の日本語を含む入力で両者が一致するとは限りません。ESLintの行と列は1始まりで、priceは6行目の5列目から10列目に相当します。終端は含みません。

参照: [Compiler 2.12.2のpositionAt](https://github.com/withastro/compiler/blob/ab9b285a34c482544da359f0ca91d0b0c25cdee4/internal/printer/print-to-json.go#L134-L175)
参照: [astro-eslint-parser 1.2.2とfixLocations](https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/astro-parser/parse.ts)
-->

---
layout: default
class: ch2-detail
---

## ESLintが未定義の参照を検査する

<div class="ch2-cols ch2-scope">
<div>
<div class="ch2-label">ここで変数名を誤記する</div>

```astro
---
const price = 10;
const amount = 3;
---

<p>{pirce * amount}</p>
<!-- pirceは診断用の誤記 -->
```

</div>
<div>
<div class="ch2-label">宣言と参照を照合する</div>
<div class="ch2-lint-matches"><div><code>price</code><span>宣言あり</span></div><div><code>amount</code><span>参照先の宣言あり</span></div><div><code>pirce</code><span>参照先の宣言なし</span></div></div>
<div class="ch2-label">元のAstroへの診断</div>
<pre class="ch2-lint-diagnostic">&lt;p&gt;{<span>pirce</span> * amount}&lt;/p&gt;</pre>
<div class="ch2-note"><code>no-undef</code><br /><code>'pirce' is not defined.</code></div>
</div>
</div>
<div class="ch2-summary">未定義の参照を検出し、元の5文字に波線を表示する</div>

<Ref href="https://github.com/ota-meshi/astro-eslint-parser/blob/v1.2.2/src/parser/index.ts">parseForESLintと位置の復元</Ref>

<!--
この枚で初めてpirceという誤記を示します。パーサーが用意したスコープ情報では、priceとamountには宣言があります。amountの参照はその宣言に対応します。pirceの参照には対応する宣言がなく、globalScope.throughに含まれます。
parseForESLintは、Virtual TSXを解析してASTとスコープ情報を用意した後、restoreでASTの位置を元のAstroへ戻します。Astro専用のNodeやvisitorKeysも整えた返却値をESLintへ渡します。ESLintのno-undefは、このスコープ情報から未定義の参照を検査します。意図した綴りを推測して修正するルールではありません。
診断JSONの抜粋は { "ruleId": "no-undef", "message": "'pirce' is not defined.", "line": 6, "column": 5, "endLine": 6, "endColumn": 10 } です。ESLint 9.36.0で確認した値で、Rangeでは[49, 54)です。波線はこの範囲を示した図です。
-->

---
layout: default
class: ch2-detail
clicks: 2
---

## Formatterがexpressionを解析する

<div class="ch2-label">整形前のAstro Source</div>

```astro
<ul>
{products.map(product=><li>
{product.name}:{product.price}</li>)}
</ul>
```

<div v-if="$clicks === 1" class="ch2-format-stage">
<div class="ch2-label">1. Astro ASTとSourceから抽出したexpression</div>

```jsx
products.map(product=><li>
{product.name}:{product.price}</li>)
```

</div>
<div v-if="$clicks >= 2" class="ch2-format-stage">
<div class="ch2-label">2. JSXで囲んだBabel入力</div>

```jsx
<>{products.map(product=><li>
{product.name}:{product.price}</li>)
}</>
```

</div>
<div class="ch2-bottom-note"><code>parse()</code> でAstro全体を、<code>babel-ts</code> でexpressionの中身を解析する</div>

<Ref href="https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/index.ts">prettier-plugin-astro 0.14.1とastroExpressionParser</Ref>

<!--
ここからはFormatter専用の例です。変数名の誤記はなく、products.mapの空白と改行をそろえたい場面です。
クリック1でAstro ASTとSourceから取り出したexpressionを示します。クリック2では同じexpressionをJSX Fragmentと波かっこで囲んだBabel入力に切り替えます。astroExpressionParser.preprocessは、この末尾の改行を含むコードを作ります。babel-tsを基にしたparserが解析し、Fragment内部のexpressionのASTを返します。
この入力と整形結果はprettier-plugin-astro 0.14.1とPrettier 3.6.2で確認しています。整形設定はprintWidth 80、tabWidth 2、endOfLine lfです。
-->

---
layout: default
class: ch2-detail
---

## Docから整形後のAstroを作る

<div class="ch2-cols ch2-doc">
<div>
<div class="ch2-label">Astro PrinterのDoc</div>

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
<div class="ch2-label">Prettierによる実際の整形結果</div>

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

<div class="ch2-note">行幅80、インデント2、LF<br />二つのexpressionの間に空白は追加しない</div>
</div>
</div>

<Ref href="https://github.com/withastro/prettier-plugin-astro/blob/v0.14.1/src/printer/embed.ts">Astro PrinterとDoc</Ref>

<!--
Docは、文字列と改行候補と字下げの指示を組み合わせたデータです。Astro Printerは、Babelが解析したexpressionの整形用Docを受け取り、Astroの波かっこやタグのDocと組み合わせます。左はexpressionを囲むDocの抜粋で、実装のlineSuffixBoundaryを省いています。expressionDocは説明用の名前です。
groupは、まとまりを1行で表示するか改行するかを選ぶ単位です。softlineは1行に収まれば空文字、改行を選べば改行になります。indentは改行後の字下げを表します。Prettierがこれらを行幅などの設定に従って文字列にします。
右は前の入力の実出力です。product.nameとproduct.priceの間にはコロンだけがあり、空白を追加しません。
-->

---
layout: default
class: ch2-detail
clicks: 2
---

## 補完と型検査のためにVirtual Codeを作る

<div class="ch2-cols">
<div>
<div class="ch2-label">Astro Source</div>

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
<div class="ch2-result">Component scriptを空白化し、<br />文字オフセットを保持する</div>
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

<div class="ch2-note">型検査用のVirtual TSX<br />TypeScript: <code>nmae</code> は型にない</div>
</div>
</div>
</div>

<Ref href="https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/index.ts">language-tools b4bcb4fとAstroVirtualCode</Ref>

<!--
Language Toolは、Editorに補完や診断を提供します。この例ではproduct.nameを宣言し、Templateでproduct.nmaeと誤記しています。
クリック1でVirtual HTMLを示します。Component scriptを区切りごと同じ長さの空白へ変えます。抜粋では先頭の空白を省いています。HTML Language Serviceは、aタグのhref属性の直前でtargetやtitleを補完候補として返します。
空白化は改行も変えるため、保持するのはUTF-16の文字オフセットです。元コードとVirtual HTMLの行番号が一致する、という意味ではありません。
クリック2で表示を切り替え、CompilerのconvertToTSXが作るVirtual TSXの抜粋を示します。Component scriptの宣言も同じTSXに含まれます。抜粋では先頭のpragmaと一部の空行と末尾の関数を省いています。TypeScriptはproductの型を調べ、nmaeというプロパティがないことを診断します。次の枚で診断位置を確認します。
参照実装はlanguage-tools b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05です。HTMLの前変換はpackages/language-server/src/core/parseHTML.ts、TSXと位置対応は同じディレクトリのastro2tsx.tsにあります。
-->

---
layout: default
class: ch2-detail
---

## TypeScriptの診断位置を戻す

<div class="ch2-cols">
<div>
<div class="ch2-label">Virtual TSX</div>

```tsx
  {product.nmae}
```

<div class="ch2-range-value">[129, 133)</div>
<div class="ch2-note">TypeScript診断 <code>TS2339</code><br />型にあるのは <code>name</code> と <code>price</code></div>
</div>
<div>
<div class="ch2-label">元のAstro</div>

```astro
  {product.nmae}
```

<div class="ch2-range-value">[95, 99)</div>
<div class="ch2-note">8行目の12列目から16列目<br />元のプロパティ名に波線を表示する</div>
</div>
</div>
<div class="ch2-mapping"><strong>Source mapとVolarのmapping</strong><span>TSXの範囲を元コードの範囲へ対応させる</span></div>
<div class="ch2-result ch2-editor-result">
<div><div class="ch2-label">Editor向けの診断</div><div class="ch2-note">LSPの行と列は0始まり</div></div>
<div>
<code>start: { line: 7, character: 11 }</code><br />
<code>end: { line: 7, character: 15 }</code>
</div>
</div>

<Ref href="https://github.com/withastro/language-tools/blob/b4bcb4fc02cd960936a5faee6c9cc0ad94fc4c05/packages/language-server/src/core/astro2tsx.ts">convertToTSXと位置対応</Ref>

<!--
前のAstro全文から、Compiler 2.12.2で生成したTSXをTypeScript 5.9.3へ渡した結果です。型にないnmaeに対する診断TS2339は、TSX上の[129, 133)を指します。CompilerのSource mapで対応する位置を調べると、Astro上では[95, 99)です。抜粋の表示位置から数えた値ではありません。
language-toolsはSource mapをVolarのmappingへ変換します。Volarがこの対応を利用し、診断範囲を元コードへ戻します。一定の差分34を常に引く方法ではなく、この範囲について対応が確認できたという意味です。
下はEditorへ渡す診断のrangeの抜粋です。LSPは行と列が0始まりなので、8行目の12列目をline 7とcharacter 11で表します。終端は含みません。
-->

---
layout: default
class: ch2-detail ch2-flow-slide
clicks: 3
---

## Astroから各ツールのアウトプットまで

<div class="ch2-flow" aria-label="Astroから三つのツールへのフロー">
  <div class="ch2-flow-head ch2-flow-data">中間データ</div><div class="ch2-flow-head ch2-flow-tool">各ツール</div><div class="ch2-flow-head ch2-flow-output">アウトプット</div>
  <div class="ch2-flow-source"><code>.astro</code></div>
  <div v-click="1" class="ch2-flow-row ch2-flow-lint">
    <svg class="ch2-flow-branch" viewBox="0 0 42 180" preserveAspectRatio="none" aria-hidden="true"><path d="M0 180 H14 V60 H40 M33 54 L40 60 L33 66" /></svg>
    <div class="ch2-flow-data"><strong>ASTとスコープ情報</strong><span>astro-eslint-parserが<br />独自のTSXをJS解析</span></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-one" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-tool"><strong>ESLint</strong></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-two" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-output">未定義変数の診断</div>
  </div>
  <div v-click="2" class="ch2-flow-row ch2-flow-format">
    <svg class="ch2-flow-branch" viewBox="0 0 42 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 60 H40 M33 54 L40 60 L33 66" /></svg>
    <div class="ch2-flow-data"><strong>整形用Doc</strong><span>Babelで<br />expressionを解析し、<br />Astro Printerが作成</span></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-one" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-tool"><strong>Prettier</strong></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-two" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-output">整形後のAstro</div>
  </div>
  <div v-click="3" class="ch2-flow-row ch2-flow-language">
    <svg class="ch2-flow-branch" viewBox="0 0 42 180" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0 H14 V120 H40 M33 114 L40 120 L33 126" /></svg>
    <div class="ch2-flow-data"><strong>Virtual HTMLとTSX</strong><span>HTMLはLanguage Tool、<br />TSXはconvertToTSX()</span></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-one" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-tool"><strong>HTML Language<br />ServiceとTypeScript</strong></div>
    <svg class="ch2-flow-arrow ch2-flow-arrow-two" viewBox="0 0 32 30" aria-hidden="true"><path d="M0 15 H28 M20 9 L28 15 L20 21" /></svg>
    <div class="ch2-flow-output">属性補完と<br />型の診断</div>
  </div>
</div>

<!--
共通のAstro Sourceから、中間データと各ツールとアウトプットへ進むフローです。クリック1でLinter、2でFormatter、3でLanguage Toolの経路を示します。
Linterはastro-eslint-parserが独自にVirtual TSXを作り、JavaScriptパーサーからASTとスコープ情報を取得します。位置を元に戻してからESLintが検査します。
FormatterはexpressionをBabel入力へ変換し、Astro PrinterがDocを組み立て、Prettierが文字列にします。DocはPrettierが整形するために必要な形式です。Docへの変換自体をCompilerの不具合とは説明しません。
Language Toolは自分で生成するVirtual HTMLと、CompilerのconvertToTSX()が生成するVirtual TSXを使い分けます。HTML Language Serviceは属性を補完し、TypeScriptは型を検査します。結果は元のAstroと対応させます。
Compilerがすべての中間データを作るわけではありません。二つのVirtual TSXは生成元と用途が異なります。
-->

---
layout: default
class: ch2-detail
---

## `parse()`と`convertToTSX()`を使う難しさ

<div class="ch2-cols ch2-api-recap">
  <div><div class="ch2-label"><code>parse()</code></div><h3 class="!normal-case !tracking-normal">expressionのASTと位置の不足</h3><ul><li>変数名と演算子のAST nodeがない</li><li>位置情報が不正確な箇所がある</li><li>ツールごとにexpressionを再解析する</li></ul></div>
  <div><div class="ch2-label"><code>convertToTSX()</code></div><h3>型検査用の変換と位置対応</h3><ul><li>生成コードをTypeScriptで解析する</li><li>元のAstroとの位置対応が必要</li><li>Editor向け変換も保守する</li></ul></div>
</div>
<div class="ch2-summary">情報の不足や不正確さと、<br />用途別の変換に伴う負担を区別する</div>

<!--
parse()の公開ASTではexpressionの中身が文字列なので、LinterとFormatterはexpressionを再解析します。一部の位置情報は補正が必要です。これは、正確なASTを受け取った後で各ツール向けの形式へ変換する負担とは区別します。
convertToTSX()はTypeScriptの型解析を利用するためのコードを生成します。TypeScriptによる解析と元のAstroへの位置対応とEditor向け変換の保守が必要です。すべてをHTML5由来の欠陥とは説明しません。Rustへ移行してexpressionのASTを提供できても、TypeScriptの型解析やツール固有の形式への変換が不要になるとは限りません。
Source contractは、この発表でCompilerへ求める保証を整理するための呼び名です。書かれたHTMLの親子関係とexpressionのASTと正確なSource位置と生成コードとの位置対応を含みます。Go版がこれらをすべて提供していた、という実装の説明ではありません。
CompilerはSourceの親子関係とexpressionの中身と位置を保証する。Adapterは各ツールに必要な形式へ変換し、元のAstroと対応させる。Ecosystem toolは検査と整形と型解析を担う。この分担で考えると、用途別の変換と、Compilerの情報不足に対する再解析や位置の再計算を区別できます。
Compilerが生成したコードとの位置対応はCompilerに求めます。Adapterが独自に変換したコードとの対応はAdapterが管理します。
-->

---
layout: statement
---

<h1 class="!text-5xl !leading-relaxed !m-0">Astro が使える基盤は、<br />2021年からどう変わったのか？</h1>

<!--
第3章では、Go版を選んだ2021年から、Astro が利用できる基盤がどう変わったかを確認します。
-->

---
layout: section
class: ch3-section
clicks: 1
---

# 3. 前提の変化
<h2 v-click="1">Astroが再利用できる基盤はどう変わったのか</h2>

<!--
第2章では、expressionのASTと位置情報がツールに必要なことを確認した。ここからは、その要求に使える基盤と資料を確認する。
-->

---
layout: default
class: ch3-detail
clicks: 1
---

## OxcでexpressionのASTを取得する

<div class="ch3-cols ch3-oxc">
<div>
<div class="ch3-label">JavaScriptからParserを呼ぶ</div>

```js
import { parseSync } from "oxc-parser";

const { program } = parseSync(
  "example.js",
  "price * amount",
);
```

</div>
<div v-click="1">
<div class="ch3-label">ASTの抜粋</div>

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
<div class="ch3-summary">Rust製Parserをnpm packageから利用できる</div>

<Ref href="https://oxc.rs/docs/guide/usage/parser.html">Oxc Parser</Ref>

<!--
price * amountというJavaScript expressionを解析する。右はprogram.body[0].expressionの抜粋で、位置などのフィールドを省いている。Identifierのnameでpriceとamountを、BinaryExpressionのoperatorで掛け算を確認できる。
このコードはnpm packageの利用例である。Astro CompilerでのRust crateの利用とAstro固有の構文への対応は第4章で説明する。

補足：利用できるツールと機能
SWCはJavaScriptとTypeScriptの変換基盤、Biomeは検査と整形のツール、Oxcは解析と変換のツール群、RolldownはBundlerである。ParserにはOxcとSWC、TransformerにはSWCとesbuild、ResolverにはOxcとVite、BundlerにはRollupとRolldown、MinifierにはesbuildとOxc、LinterにはBiomeとESLint、FormatterにはBiomeとPrettierという選択肢がある。完成したツールとして利用する方法と、ライブラリとして組み込む方法を区別する。
Vite 2では開発時の事前バンドルをesbuild、本番バンドルをRollupが担っていた。Vite 8はRolldownを採用した。Astroの構文変換と汎用的なBuild基盤を分けて考える例である。
参照：https://vite.dev/blog/announcing-vite8

補足：napi-rsと配布方法
Node-APIはネイティブ実装をNode.jsから利用するAPIで、napi-rsはRustの関数を公開するbindingsと型定義を生成する。たとえば#[napi]を付けたmultiply(p: u32, q: u32)がp * qを返すRust関数なら、JavaScriptからmultiply(1200, 3)を呼び、3600を受け取れる。生成されたindex.jsがOSとCPUに合う実装をロードする。これは呼び出し方の例であり、Astroの実装を示すものではない。
ネイティブバイナリはOSとCPUに対応する実行形式、WASMは対応する実行環境向けのバイナリ形式、Rust crateはRustの実装へ組み込むライブラリである。実装言語と配布方法を分けて選ぶ。Node-APIとWASMは2021年にも存在し、napi-rsもbindingsと型定義の生成を提供していた。
参照：https://napi.rs/docs/introduction/simple-package
参照：https://napi.rs/blog/announce-v2
-->

---
layout: default
class: ch3-detail
---

## Biomeから学ぶEditor向けの解析

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

<p>括弧と条件のexpressionが欠けても、<br />本文のブロックを解析できる</p>
</div>
</div>
<div class="ch3-note">Lossless CST：元のソースを再現できるよう、<br />空白と改行とコメントも含めた木</div>

<Ref href="https://biomejs.dev/internals/architecture/">Biome Architecture</Ref>

<!--
ソースの保持とエラーからの回復は別々の設計課題である。Biomeはrowanのforkを基に、空白と改行とコメントも保持するCSTを実装している。情報を付加したASTも選択肢になる。
while {}はBiomeの設計資料の例である。括弧と条件のexpressionを欠落として記録し、本文のブロックを解析できる。一方、function}のような入力では正しく解釈できない部分をBogus nodeで表す。回復できる範囲は入力とエラーの位置に依存する。
これはBiomeの設計例であり、AstroがBiomeやLossless CSTを採用したという説明ではない。現在のAstro実装の回復範囲とも区別する。
-->

---
layout: default
class: ch3-detail
---

## Astro Syntaxの規則を明文化する

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
  <div><strong>HTML属性</strong><span><code>class="title"</code></span></div>
  <div><strong>expression</strong><span><code>{name}</code></span></div>
  <div><strong>複数のルート要素</strong><span><code>h1</code> と <code>p</code> を並べたTemplate</span></div>
</div>
</div>

<Ref href="https://github.com/withastro/compiler/blob/04170031ce2f30d1882fe480e87998197e0016aa/SYNTAX_SPEC.md">Astro Syntax仕様ドラフト（Draft、2026年2月）</Ref>

<!--
2026年2月3日付のDraftを参照する。Component script、HTMLの属性名、expression、複数ルートの規則を確認できる。右のexpressionラベルは波かっこを含むAstro expressionの領域に対応し、その中のnameがJavaScript expressionである。
このページでは構文規則を紹介する。位置情報の精度と編集中の入力への対応は、ツールの要求と合わせて別途設計する。仕様ドラフトが、それらの実装を保証しているという説明ではない。
-->

---
layout: default
class: ch3-detail
---

## MarkdownとMDXでもRustを試した

<div class="ch3-cols ch3-proposals">
<div>
<h3>Rustライブラリへの提案</h3>
<div class="ch3-proposal">
  <strong>markdown-rs</strong>
  <p>GFMの表の再生成と<br />WASM bindings</p>
  <div class="ch3-links"><a href="https://github.com/wooorm/markdown-rs/pull/184">PR #184</a> と <a href="https://github.com/wooorm/markdown-rs/pull/185">PR #185</a></div>
</div>
<div class="ch3-proposal">
  <strong>mdxjs-rs</strong>
  <p>npm配布とnative bindings</p>
  <div class="ch3-links"><a href="https://github.com/wooorm/mdxjs-rs/issues/71">Issue #71</a></div>
</div>
</div>
<div>
<h3>Astroへの提案</h3>
<div class="ch3-proposal">
  <strong>Rust製MDX Compilerの試作</strong>
  <div class="ch3-links"><a href="https://github.com/withastro/astro/pull/14080">PR #14080</a></div>
</div>
<div class="ch3-proposal">
  <strong>既存pluginを利用する<br />AST Bridgeの案</strong>
  <div class="ch3-links"><a href="https://github.com/withastro/astro/pull/14181">PR #14181</a></div>
</div>
</div>
</div>

<!--
提案先で二つに分けた。時系列を示す図ではない。markdown-rsにはGFMの表をASTからMarkdownへ再生成するPR #184と、WASM bindingsを追加するPR #185を提案した。mdxjs-rsのnpm配布とnative bindingsの提案はIssue #71であり、PRではない。
AstroへのPR #14080とPR #14181は、いずれも未マージの試作PRとして紹介する。2026年9月21日の確認では、どちらも未マージでcloseされている。

補足：MarkdownとMDXの基盤
MDXではMarkdownの本文にJSXとJavaScript expressionを書ける。Content Processorは本文を解析して表示用コードへ変換し、Astro Compilerとは別の経路でBuildへ渡す。markdown-rsはMarkdownの解析基盤、mdxjs-rsはmarkdown-rsとSWCを使ってMDXをJavaScriptへ変換するCompilerである。

補足：試作とAST Bridge
2025年7月のPR #14080では、Rust実装の利用を選べるようにし、利用できない場合は既存のJavaScript実装へ戻す案を試した。frontmatter、見出しのslug、画像、Astro componentとの互換性を検証対象にした。
既存の構成では、GFMの表を扱うremark-gfm、引用符を変換するremark-smartypants、見出しにIDを付けるrehype-slugなどを使う。検討したmdxjs-rsはこれらのJavaScript pluginを実行できなかった。
PR #14181のAST Bridgeは、RustでMarkdownとMDXを解析し、必要な段階でASTをJavaScriptへ渡し、remarkとrehypeのpluginで加工し、加工したASTをRustへ戻してコードを生成する案である。MarkdownのASTはmdast、HTMLのASTはhastと呼ぶ。ASTを受け渡す形式とタイミングも設計対象になる。
対話では、WASMとNode-APIの配布方法、OSとCPUごとのビルドとテストの担当、追加の依存を必要な利用者だけに含める方法、pluginの互換性、汎用部分の保守主体を検討した。
-->

---
layout: default
class: ch3-detail
---

## 自作のxmdxでAstroへの統合を試した

<div class="ch3-integration">
  <div><strong>作ったもの</strong><span>Rust実装をNode-APIとWASMで<br />JavaScriptから利用するpackage</span></div>
  <div><strong>組み込んだもの</strong><span>AstroとStarlight向けのintegration</span></div>
  <div><strong>検証したこと</strong><span>実際のAstro Docsでの変換と表示とBuild</span></div>
</div>
<div class="ch3-summary">再利用には、pluginとの互換性と配布方法の検討も必要だった</div>

<Ref href="https://github.com/jp-knj/xmdx">xmdxのpackageとAstro integration</Ref>

<!--
Astroへの提案に続き、汎用的なMarkdownとMDXの実装を独立したxmdxとして試作した。Rust実装をNode-APIとWASMでJavaScriptから利用するpackageと、AstroとStarlight向けのintegrationを作った。StarlightはAstroを使ったドキュメントサイト向けの仕組みである。
当時のAstro Docsにastro-xmdxを組み込んだ開発環境で、既存コンテンツの変換、ブラウザでの表示と機能、サイト全体のBuildを検証した。これは当時の試作の検証範囲であり、現在のすべてのAstro構成での互換性を保証するものではない。ネイティブ実装とWASMを配布したことと、Docsで検証した環境を区別する。速度の比較値は掲載しない。

補足：Amsterdamと他の実装
Vue.js Amsterdam 2026のAstro 6の発表では、実装に利用するOxcとRust、開発を支援するClaude Codeの話があり、関連する試みとしてxmdxも紹介された。
xmdxに加えてox-contentとSätteriも検討した。比較した観点は、実際のBuildでの速度、pluginが加工できるデータとタイミング、AstroとContent基盤の境界、保守主体である。Sätteriを勧める判断は第4章で説明する。xmdxの現在のREADMEもSätteriの利用を案内しており、このページは当時の試作経験として紹介する。
-->

---
layout: default
class: ch3-detail
---

## 第3章の結論

<table class="ch3-recap">
<thead><tr><th>第2章からの課題</th><th>第3章で確認したこと</th></tr></thead>
<tbody>
<tr><td>expressionのAST</td><td>OxcのParserを利用できる</td></tr>
<tr><td>元のソースと編集中の入力</td><td>Biomeの設計を参考にできる</td></tr>
<tr><td>Astro固有の構文</td><td>仕様ドラフトで規則を確認できる</td></tr>
</tbody>
</table>
<div class="ch3-summary">Astro固有の実装と、<br />既存の基盤に任せる範囲を選び直せる</div>

<!--
expressionのASTにはOxcのParser、元のソースの保持と編集中の入力にはBiomeの設計例、Astro固有の構文には仕様ドラフトという基盤と資料を確認した。MarkdownとMDXでの試作も、pluginの互換性と配布方法という利用条件を検証する経験になった。
Astro固有の実装と、既存の基盤に任せる範囲を選び直せる。第4章では位置情報も含めてAstro Compilerの担当範囲を確認する。
-->

---
layout: section
class: ch3-section
clicks: 1
---

# 4. 新しい判断
<h2 v-click="1">Astroは何を実装し、<br />何を既存の基盤に任せるのか</h2>

<!--
ここから、Astro自身の実装と既存基盤の担当範囲を説明する。次の38枚目の全体図で、CompilerとEditorとBuildとContentの担当範囲を確認する。
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
  <div v-click="2" class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">汎用的な解析と変換を、どの基盤に任せるか</div>
  <div v-click="3" class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">Astroが、どの機能を実装して保守するか</div>
</div>

<!--
クリックごとに、次の項目を説明します。
判断の軸は4つです。どのソース情報を保持するか。どの段階で補正や変換を行うか。汎用的な解析と変換をどの基盤に任せるか。そして Astro がどの機能を実装して保守するか。この4つで、HTML、JavaScript、Markdown と MDX の3つの具体例を確認します。
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
  <p v-click="1" class="">一方、閉じ忘れたタグなどの構文エラーは拒否する</p>
  <p v-click="2" class="text-primary">どんな入力でも受け入れる、という意味ではない</p>
</div>

<Ref href="https://github.com/withastro/roadmap/issues/1356">withastro/roadmap#1356: 新Compilerの正式提案</Ref>

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
      <li>出力HTMLから作るnodeの親子関係</li>
      <li>表示やJavaScriptからの操作に使う</li>
    </ul>
  </div>
</div>

<div v-click="2" class="mt-8 text-xl leading-relaxed">
  <p class="">同じ入れ子のHTMLをBrowserへ渡せば、BrowserではHTMLの規則に従って補正が起きる</p>
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
第2章で確認したGo版の表現です。expressionのソースを取り出せます。次のページではRust版のparse APIが提供するexpressionのASTを確認します。
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

## ツールから見た変化とEditorの役割

<div class="grid grid-cols-2 gap-8 mt-8 text-lg">
  <div class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
    <h3 class="opacity-100 !text-base">ツールから見た変化</h3>
    <ul class="mt-2">
      <li>expressionの左辺と右辺をたどれる</li>
      <li>演算子と識別子を個別に扱える</li>
      <li>JavaScript ASTを扱うツールと連携しやすくなる</li>
    </ul>
  </div>
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-6">
    <h3 class="opacity-100 !text-base">Editor が引き続き担当すること</h3>
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
ツールから見た変化です。expressionの左辺と右辺をたどれる。演算子と識別子を個別に扱える。JavaScript の AST を扱う既存のツールで利用しやすくなる。ただし、これで Editor の仕事がなくなるわけではありません。変数の宣言と使用箇所の対応、型情報、Astro 固有構文とソース位置、不完全な入力。これらは引き続き Editor の仕事です。AST の提供は、診断や補完を作るための基盤になる、ということです。
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
      <li>expressionと識別子のAST</li>
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

<Ref href="https://github.com/withastro/compiler-rs/blob/main/Cargo.toml">compiler-rs: Cargo.toml</Ref>

<!--
クリックごとに、次の項目を説明します。
Oxc との責務分担です。Oxc に任せるのは、JavaScript と TypeScript の解析、expressionや識別子を表す AST、汎用的な変換やコード生成の基盤。Astro が持つのは、Astro 固有の構文、Template と JavaScript が混在する部分、Astro の実行に必要な変換、そして元のソースとの対応。Rust 版コンパイラは Astro 向けに拡張した Oxc を使っています。汎用部分を再利用しながら、必要な変更を加える。自分たちで実装して保守する範囲を絞るという判断です。
-->

---
layout: center
clicks: 3
---

<Overview
  highlight="compiler,editor,browser,parser,oxc,astro-syntax"
  subs="parser,oxc,astro-syntax"
  :annotate="{
    ...($clicks >= 1 ? { 'compiler->editor': '書かれた親子関係とソース位置、埋め込まれたJavaScriptのAST' } : {}),
    ...($clicks >= 2 ? { browser: '出力HTMLからDOMを構築' } : {}),
  }"
/>

<div v-click="3" class="text-center text-2xl text-primary mt-2">Compilerを less clever にする</div>

<!--
クリックごとに、次の項目を説明します。
コンパイラは Editor に、書かれた親子関係とソース位置、埋め込まれた JavaScript の AST を提供します。コンパイラ内部では Oxc が汎用的な解析を担い、Astro が固有の構文と変換を担当します。ブラウザは出力 HTML から DOM を構築します。コンパイラを less clever にするとは、暗黙に補正する範囲を減らし、解析と変換、Editor やブラウザの担当範囲を明確にすることです。
-->

---
layout: default
class: body-center
clicks: 2
---

## Contentの例へ戻る

<div class="text-xl mb-6">Content ProcessorはMarkdownとMDXを解析し、HTMLやJavaScriptへ変換する</div>

<div class="grid grid-cols-2 gap-8 text-xl">
  <div class="border border-[#BC52EE] border-opacity-45 rounded-xl p-6" style="background: rgba(188, 82, 238, 0.06)">
    <div class="text-2xl font-600">Astroが担当すること</div>
    <ul class="mt-3 text-lg">
      <li>Processorを組み込む入口を用意する</li>
      <li>Content CollectionsとBuildに統合</li>
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

<div v-click="2" class="mt-8 text-xl text-primary">Content Processorは<code>.astro</code> Compilerとは別に選ぶ</div>

<!--
クリックごとに、次の項目を説明します。
第3章では、Rust 製 MDX コンパイラの PoC と plugin 互換性の問題を確認しました。ここでは、Markdown と MDX の担当範囲を分けます。Astro は Processor を組み込む入口を用意し、Content Collections や Build に統合します。Processor は Markdown と MDX の構文、Content 固有の変換、拡張機能を実行する仕組みを担当します。Content Processor は .astro Compiler とは別に選びます。
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
      <li>Rustが解析と変換を担う</li>
      <li>よく使う変換を標準機能として提供</li>
      <li>JavaScriptで拡張できる</li>
    </ul>
  </div>
  <div v-click="1">
    <h3 class="opacity-100 !text-base">pluginとの境界</h3>
    <div class="grid grid-cols-[2rem_1fr] gap-x-3 gap-y-4 mt-3">
      <div class="text-primary">1</div><div>扱う node の種類を指定</div>
      <div class="text-primary">2</div><div>JavaScriptでnodeを検査と変更</div>
      <div class="text-primary">3</div><div>必要な情報だけを受け渡す</div>
    </div>
  </div>
</div>

<Ref href="https://satteri.bruits.org/docs/plugins/">Sätteri: Plugin API</Ref>

<!--
クリックごとに、次の項目を説明します。
Sätteri では、Rust が Markdown と MDX の解析と変換を担い、よく使う変換を標準機能として提供します。JavaScript では独自の変換を追加できます。plugin は扱う node の種類を指定し、その node を検査したり変更したりする関数を JavaScript で実行します。これが visitor です。たとえば見出しやリンクの node を指定し、必要な情報だけを Rust と JavaScript の間で受け渡します。
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
      <div class="border border-[#E5E0EC] rounded-lg px-4 py-3">AST Bridgeで既存pluginとの連携を試した</div>
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
  <span class="text-lg ">スライドには、対象バージョンと状態を添える</span>
  <Status kind="adopted" />
  <Status kind="wip" />
  <Status kind="proposed" />
  <Status kind="poc" />
</div>

<Ref href="https://docs.astro.build/en/guides/markdown-content/#markdown-processors">Astro Docs: Markdown Processors</Ref>

<!--
クリックごとに、次の項目を説明します。
PoC で試したのは、Rust 製 MDX コンパイラの統合と、AST Bridge による既存 plugin との連携です。採用後は、Astro 6.4 で Markdown Processor を選ぶ仕組みが追加され、Astro 7 で Sätteri が標準 Processor になりました。unified を選ぶ経路も用意されています。提案時の試みと、採用後の状態を分けて確認します。
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
      <li>pluginとの互換性</li>
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
xmdx の検証で、速度、plugin との互換性、Astro への統合、配布と継続的な保守という条件が具体的になりました。その条件を使ってほかの実装も比較し、Astro の要求に合う Sätteri を勧める判断につながりました。xmdx の README でも Sätteri の利用を案内しています。PoC では、実際に試して分かった制約、選択肢を比較するための判断材料、upstream とコミュニティとの関係を得られました。自分の実装の採用に至らなくても、次の判断につながる成果がありました。
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
    <div class="mt-2">どの言語で実装するか</div>
  </div>
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">配布と実行方法</div>
    <div class="mt-2">どう配布し、どの環境で実行するか</div>
  </div>
  <div v-click="2" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">AST設計</div>
    <div class="mt-2">構文の表し方と保持する情報</div>
  </div>
  <div v-click="3" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-xl font-600">責務の所有</div>
    <div class="mt-2">どのprojectが実装して保守するか</div>
  </div>
</div>

<div v-click="4" class="mt-8 text-xl leading-relaxed">
  <p class="text-primary">これらは、それぞれ別の判断になる</p>
  <p class="">Node.js向けには native bindings。Browser内でCompilerを動かす場合はWASMの経路を考える</p>
  <p class="text-lg">全体図のBrowserは、生成されたサイトを表示する場所。Compiler自体をBrowser内で実行する話とは区別する</p>
</div>

<Ref href="https://github.com/withastro/compiler-rs">Rust版Compiler READMEとbindingsの構成</Ref>

<!--
クリックごとに、次の項目を説明します。
第1章の選択を、ここでは4つに分けます。実装言語、配布と実行方法、AST 設計、責務の所有です。Node.js 向けには native bindings を使い、ブラウザ内でコンパイラを動かす場合は WASM の経路を考えます。Rust 版にも WASM 向けの実装があり、提供する環境と API は実装ごとに確認する必要があります。全体図のブラウザは生成されたサイトを表示する場所です。コンパイラ自体をブラウザ内で実行する場合とは区別します。
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
Astro Compiler は Astro Syntax を解析して親子関係とソース位置を保持し、parse() で AST を提供し、transform() で HTML 生成用の JavaScript へ変換します。汎用的な解析には Oxc を使います。Editor は AST とソース位置を利用し、不完全な構文を扱いながら診断と補完を提供します。Build はモジュールを解決し、JavaScript と CSS をまとめます。Vite とその内部の Rolldown を使いますが、Compiler と Build の分担は Go 版の導入時から存在していました。Astro の Content は Processor を選ぶ入口を用意し、Content Collections とビルドに統合します。Content Processor は Markdown と MDX の解析と変換、frontmatter、見出しの ID、コードの色付け、MDX component を担当し、汎用的な機能と plugin model を保守します。unified ecosystem は既存 plugin が必要な利用者の経路を担います。Rust 版コンパイラの公開 API は parse() と transform() が中心です。Language Server 向けの TSX 出力は、実行用コンパイラとは別の要件として扱われています。
-->

---
layout: default
class: body-center
clicks: 2
---

## 三つの具体例を、同じ全体図へ重ねる

<div class="grid grid-cols-3 gap-6 mt-10 text-lg">
  <div class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-black">HTML</div>
    <div class="text-2xl font-600 mt-1">保持と補正</div>
    <ul class="mt-3">
      <li>書かれた親子関係を保持する</li>
      <li>Compilerの解析とBrowserのDOM構築を区別する</li>
    </ul>
  </div>
  <div v-click="1" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-black">JavaScript</div>
    <div class="text-2xl font-600 mt-1">ASTの提供と再利用</div>
    <ul class="mt-3">
      <li>expressionの内部をASTとして提供する</li>
      <li>汎用的な解析にはOxcを利用する</li>
    </ul>
  </div>
  <div v-click="2" class="border border-[#E5E0EC] rounded-xl p-5">
    <div class="text-sm uppercase tracking-widest text-black">Markdown と MDX</div>
    <div class="text-2xl font-600 mt-1">互換性と所有</div>
    <ul class="mt-3">
      <li>pluginとの互換性も要件に含める</li>
      <li>Astroとの統合と、Contentの解析と変換を分ける</li>
    </ul>
  </div>
</div>

<!--
クリックごとに、次の項目を説明します。
3つの具体例を並べます。HTMLでは、書かれた親子関係を保持し、コンパイラの解析とブラウザのDOM構築を区別します。JavaScriptではexpressionのASTを提供し、汎用的な解析はOxcに任せます。MarkdownとMDXではpluginの互換性も要件に含め、Astroとの統合と汎用的なContentの変換を分けます。
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
ここでの契約とは、連携する相手へ保証する情報や振る舞いを指します。Source contract は主にコンパイラと Editor の間の契約です。書かれた親子関係と位置を保持し、埋め込まれた構文をツールが利用できる形で渡します。Output contract はコンパイラとビルドとブラウザの間の契約です。実行や表示に使う成果物を生成し、ソースの入れ子と表示時の DOM の親子関係を区別します。Ecosystem contract は Content Processor と plugin ecosystem の間の契約です。既存 plugin を利用できる経路を維持し、新しい plugin model への移行方法を用意します。
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
    <li v-click="1">汎用的な解析と変換には、<b>既存の基盤</b> を利用する</li>
    <li v-click="2">Astroは、<b>Astro固有の構文と変換と統合</b> を担当する</li>
    <li v-click="3">用途に応じて、<b>RustとJavaScriptの役割</b> を分ける</li>
    <li v-click="4"><code>.astro</code> Compiler と Markdown と MDX の Processor も、それぞれの要件に合った構成を選ぶ</li>
  </ul>
</div>

<!--
クリックごとに、次の項目を説明します。
Rust への移行では、コンパイラの設計と保守範囲も見直しています。汎用的な解析と変換には既存の基盤を使い、Astro は固有の構文と変換と統合を担当します。用途に応じて Rust と JavaScript の役割を分け、.astro Compiler と MarkdownとMDX の Processor も、それぞれの要件に合った構成を選びます。
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
    <div class="text-sm uppercase tracking-widest text-black">当時の判断</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>高速な変換と、複数環境での実行</div>
      <div>GoとWASMが要件に合っていた</div>
    </div>
  </div>
  <div v-click="1" class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-sm uppercase tracking-widest text-black">発見した問題</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>ソースの親子関係と位置への要求</div>
      <div>HTML補正による予想しにくい挙動</div>
      <div>独自実装の保守コスト</div>
    </div>
  </div>
  <div v-click="2" class="border-l-2 border-[#E5E0EC] pl-5">
    <div class="text-sm uppercase tracking-widest text-black">前提の変化</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>Rust基盤の成熟</div>
      <div>再利用できる範囲の拡大</div>
      <div>Astro Syntax の整理</div>
    </div>
  </div>
  <div v-click="3" class="border-l-2 border-[#BC52EE] border-opacity-60 pl-5">
    <div class="text-sm uppercase tracking-widest text-black">新しい判断</div>
    <div class="mt-2 flex flex-col gap-1">
      <div>保持する情報と変換する段階の明確化</div>
      <div>保守範囲を絞る</div>
      <div>改善し続けられる設計へ</div>
    </div>
  </div>
</div>

<!--
クリックごとに、次の項目を説明します。
当時は、高速な変換と複数環境での実行が必要で、Go と WASM がその要件に対応していました。使い続けるなかで、ソースの親子関係と位置を扱う要求が明確になり、HTML 補正による不具合や予想しにくい挙動、独自実装の保守の難しさが分かりました。その後、Rust の解析と変換基盤が育ち、汎用的な機能を再利用できる範囲が広がり、Astro Syntax の整理も進みました。新しい判断は、保持する情報と変換する段階を明確にし、既存基盤を使って保守範囲を絞り、チームが継続して改善できるコンパイラへ作り直すことです。Content での取り組みも、Markdown と MDX の解析と変換を通じて、同じ責務設計の問題を検証したものでした。
-->

---
layout: center
class: text-center
clicks: 2
---

<div class="text-5xl font-700 leading-[1.5]" style="color: #7611A6">
  既存の基盤を再利用し、<br />
  <span v-click="1">自分たちの実装範囲を絞り、</span><br />
  <span v-click="2">保守し続けられる設計にするため。</span>
</div>

<!--
クリックごとに、次の項目を説明します。
Rust の基盤を再利用し、Astro が実装して保守する範囲を絞って、継続して改善できるコンパイラへ再設計するためです。
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
    <li v-click="2">今なら、どの機能を既存基盤に任せられるのか</li>
    <li v-click="3">自分たちが実装して保守すべき範囲はどこか</li>
  </ul>
</div>

<div class="mt-8 text-xl leading-relaxed">
  <p>技術を選び直す機会に、<b>担当する責務も見直す</b></p>
  <p class="">PoCがmergeされなくても、制約を明らかにし、communityの次の判断につなげられる</p>
</div>

<!--
クリックごとに、次の項目を説明します。
技術選定は、その時点の要件と利用できる基盤に対する判断です。選び直すときには、当時何を実現するために選んだのか、利用が広がって何が新しく必要になったのか、今ならどの機能を既存基盤に任せられるのか、自分たちが実装して保守すべき範囲はどこかを確認します。技術を選び直す機会に、担当する責務も見直します。PoC がマージされなくても、制約を明らかにして、コミュニティの次の判断につなげることはできます。
-->

---
layout: center
class: text-center
clicks: 1
---

## ありがとうございました

<div class="mt-8 text-xl ">Astro Japan Community</div>

<img v-click="1" src="./images/qrcode_discord.com.png" class="h-60 mx-auto mt-6" alt="Discord QR Code" />

<!--
クリックごとに、次の項目を説明します。
ありがとうございました。Astro Japan Community の Discord です。よかったら覗いてみてください。
-->
