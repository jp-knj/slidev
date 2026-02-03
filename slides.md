---
theme: ./theme
author: jp-knj
duration: 30min
mdc: true
transition: fade
colorSchema: dark
themeConfig:
  primary: "#e8c4f9"
layout: center-vertical
---

<img src="./images/icon.png" class="" alt="profile" />

---
class: text-left flex flex-col justify-center h-full
---

## コンテンツ駆動と
## コミュニティの役割

---
class: flex items-center justify-center h-full
---

<div class="grid grid-cols-2 gap-8">
    <div>
        <div class="flex items-center gap-4 mt-4">
            <img src="./images/profile.jpeg" class="w-24 rounded-full" alt="profile" />
            <div class="flex flex-col justify-center gap-0">
                <p class="text-2xl !my-0">ケンジ</p>
                <p class="text-xl !my-0">GitHub: <a href="https://github.com/jp-knj">jp-knj</a></p>
            </div>
        </div>
    </div>
    <div>
        <h3>今日のはなし</h3>
        <ol class="text-xl font-bold">
            <li>Astroのいま</li>
            <li>Astroのつらみ</li>
            <li>コミニティの役割</li>
        </ol>
    </div>
</div>

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

## Astroは静的サイト向けなのか 🤔

---
layout: cover
class: center
---

<div class="mt-8">
  <div class="text-2xl text-white font-light mb-4 text-opacity-60">静的サイト向けではなく</div>
  <div class="text-5xl font-black text-white filter drop-shadow-lg">
    コンテンツ駆動
  </div>
  <div class="text-2xl text-white font-light mt-4 text-opacity-60">としてがんばってきた</div>
</div>

---
layout: center
---

# 👀　👀　👀

---
layout: section
---

# 1. コンテンツ駆動の深み
## ファイル管理からデータ基盤へ

---
layout: default
---

## コンテンツのパラダイムシフト

<div class="grid grid-cols-3 gap-3 mt-16">
  <div class="relative p-4 rounded-xl bg-transparent border border-white/30">
    <h2 class="font-bold">Data Layer</h2>
    <h4 class="mt-8 leading-8 tracking-tighter">
      Gatsby.js+GraphQL<br/> 
      Content Mesh
    </h4>
  </div>
  <div class="relative p-4 rounded-xl bg-transparent border border-white/30">
    <h2 class="font-bold text-lg">Validation</h2>
    <h4 class="mt-8 leading-8 tracking-tighter">
      Zod + File System<br/>
      Content Collection
    </h4>
  </div>
  <div class="relative p-6 rounded-xl bg-transparent border-2 border-white">
    <div class="absolute -top-4 left-4 bg-purple-600 text-white px-3 py-1 text-xs rounded-full font-bold">New</div>
    <h2 class="font-bold text-white">Database</h2>
    <h4 class="mt-8">
      Content Layer
    </h4>
  </div>
</div>

<h2 class="mt-8 p-4 text-center">
  エンジンはSQLite化<br/>
  Live Content Collections
</h2>

---
layout: section
---

# 2. パフォーマンスの再定義
## Islands から Server Islands へ

---
layout: center
---

## Server Islands

<div class="flex items-center justify-between gap-4 w-full mt-8">
  <div class="flex-1 text-center min-w-0">
    <div class="bg-transparent border border-white/30 p-6 rounded-lg mb-4 h-32 flex items-center justify-center">
      <span class="text-4xl">🖼️</span>
    </div>
    <h4 class="font-bold text-white whitespace-nowrap overflow-visible">Static Shell</h4>
  </div>

  <div class="text-2xl text-white flex-shrink-0">➜</div>

  <div class="flex-1 text-center min-w-0">
    <div class="bg-transparent p-6 rounded-lg mb-4 h-32 flex items-center justify-center border-2 border-white/30">
      <span class="text-4xl animate-pulse">⚙️</span>
    </div>
    <h4 class="font-bold text-white whitespace-nowrap overflow-visible">Server Defer</h4>
  </div>

  <div class="text-2xl text-white flex-shrink-0">➜</div>

  <div class="flex-1 text-center min-w-0">
      <div class="bg-transparent p-6 rounded-lg mb-4 h-32 flex items-center justify-center border-2 border-white/30">
      <span class="text-4xl">👤</span>
    </div>
    <h4 class="font-bold text-white whitespace-nowrap overflow-visible">Injection</h4>
  </div>
</div>

---
layout: default
---

## Server Islandsのポテンシャル

<h4 class="mt-8 text-center">コンポーネント単位でStatic→Serverへ段階的移行</h4>

<div class="grid grid-cols-2 gap-8 mt-8">
  <div>
    <h4 class="text-center mb-4 font-bold">Static</h4>
    <div class="border border-white/30 p-6 rounded-lg text-center">
      <h2>
        📄<br>
        📄<br>
        📄<br>
        📄<br>
        📄
      </h2>
    </div>
  </div>

  <div>
    <h4 class="text-center mb-4 font-bold">Static + Server</h4>
    <div class="border-2 border-purple-500 p-6 rounded-lg text-center">
      <h2>
        📄<br>
        ⚙️ <span class="text-purple-400">Server</span><br>
        📄<br>
        ⚙️ <span class="text-purple-400">Server</span><br>
        📄
      </h2>
    </div>
  </div>
</div>

<div class="mt-8 text-center">
<strong>🚀 メインプロセスを邪魔せず、遅いAPIが全体を止めない</strong><br>
</div>

---
layout: section
---

# 3. アプリケーション基盤の強化
## 開発を支える標準化

---
layout: center
---

## 開発体験の標準化

<div class="grid grid-cols-2 gap-6 mt-8 h-80">

  <div class="bg-transparent border border-white/30 text-white p-6 rounded-xl flex flex-col">
    <div class="flex items-center gap-2 mb-4">
      <span class="text-white text-xl">💻</span>
      <h4 class="text-xl font-bold text-white">Astro Actions</h4>
    </div>
    <div class="border-2 px-2 border-white/30 flex-grow flex items-center justify-center rounded mb-4 bg-black/20">
      <div class="text-lg text-center font-mono">
        actions.like.safe(input)<br>
        ⬇<br>
        Type Safe Result
      </div>
    </div>
  </div>

  <div class="bg-transparent border border-white/30 text-white p-6 rounded-xl flex flex-col">
    <div class="flex items-center gap-2 mb-4">
      <span class="text-white text-xl">👤</span>
      <h4 class="text-xl font-bold text-white">Standard Sessions</h4>
    </div>
    <div class="flex-grow grid grid-cols-2 gap-2 mb-4">
      <div class="bg-white/20 rounded flex items-center justify-center p-4"><img src="./images/aws.svg" class="h-10" alt="AWS" /></div>
      <div class="bg-white/20 rounded flex items-center justify-center p-4"><img src="./images/vercel.svg" class="h-10" alt="Vercel" /></div>
      <div class="bg-white/20 rounded flex items-center justify-center p-4"><img src="./images/cloudflare-pages.svg" class="h-10" alt="Cloudflare" /></div>
      <div class="bg-white/20 rounded flex items-center justify-center p-4"><img src="./images/node.svg" class="h-10" alt="Node" /></div>
    </div>
  </div>
</div>

---
layout: center
---

## どこでも動くAstro
<h4 class="font-bold text-white mt-6">Container API (Enviroment API) + Server Island</h4>

<div class="mt-12 flex items-center justify-center gap-4">
  <!-- Left: Backend Frameworks -->
  <div class="flex flex-col items-center gap-6">
    <div class="flex flex-col items-center gap-1">
      <img src="/images/laravel.svg" class="w-12 h-12" />
      <span class="text-sm opacity-80">Laravel</span>
    </div>
    <div class="flex flex-col items-center gap-1">
      <img src="/images/rails.svg" class="w-12 h-12" />
      <span class="text-sm opacity-80">Rails</span>
    </div>
    <div class="flex flex-col items-center gap-1">
      <img src="/images/hono.svg" class="w-12 h-12" />
      <span class="text-sm opacity-80">Hono</span>
    </div>
  </div>

  <!-- Arrow -->
  <span class="text-4xl opacity-60 mx-2">→</span>

  <!-- Center: Astro -->
  <div class="flex flex-col items-center gap-2 px-6 py-4 rounded-xl">
    <img src="/images/astro.svg" class="w-20 h-20" />
    <span class="text-lg font-bold">Astro</span>
  </div>

  <!-- Arrow -->
  <span class="text-4xl opacity-60 mx-2">→</span>

  <!-- Right: Runtime Environments -->
  <div class="flex flex-col items-center gap-5">
    <div class="flex flex-col items-center gap-1">
      <img src="/images/browser.svg" class="w-10 h-10" />
      <span class="text-sm opacity-80">Browser</span>
    </div>
    <div class="flex flex-col items-center gap-1">
      <img src="/images/edge-runtime.svg" class="w-10 h-10" />
      <span class="text-sm opacity-80">Edge</span>
    </div>
    <div class="flex flex-col items-center gap-1">
      <img src="/images/node.svg" class="w-10 h-10" />
      <span class="text-sm opacity-80">Node.js</span>
    </div>
  </div>
</div>

---
layout: center
class: flex flex-col items-center justify-center h-full
---

## Proxyとしてもイケる
## UIレンダリングエンジン

---

## Astroの2025

<div class="grid grid-cols-[4fr_6fr] gap-4 items-center">
    <div class="text-2xl">npmダウンロード数 📈</div>
    <img src="./images/npm-trends.webp" class="h-100 mx-auto" alt="npm-trend" />
</div>

---

## Astroの2025

<div class="grid grid-cols-[3fr_6fr] gap-4 items-center">
    <div class="text-2xl">
        GitHub Octoverse<br/>
        成長率が高い言語としてピックアップ 🚀
    </div>
    <img src="./images/octoverse.webp" class="h-80 mt-15" alt="octoverse" />
</div>

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

## Astro Ecosystem

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

<h2 class="flex items-center justify-center">
Open Collective 🏦　+

<div class="flex ml-8">
  <img src="./images/cloudflare.svg" class="h-20" alt="Cloudflare" />
</div>
</h2>

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

## withastro 🚀 + astrolicious 🍨

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

## Astro AwardsとEcosystem Fund 🤝

<div class="flex gap-6 flex-wrap mt-12">
  <a href="https://github.com/ktym4a">
    <img src="./images/ktym4a.png" width="120" alt="ktym4a" class="rounded-full" />
    ktym4a
  </a>
  <a href="https://github.com/kyosuke">
    <img src="./images/kyosuke.png" width="120" alt="Kyosuke" class="rounded-full" />
    kyosuke
  </a>
  <a href="https://github.com/pilcrowonpaper" class="flex flex-col items-center justify-center h-full">
    <img src="./images/pilcrowonpaper.png" width="120" alt="pilcrow" class="rounded-full" />
    pilcrowonpaper
  </a>
  <a href="https://github.com/ota-meshi">
    <img src="./images/ota-meshi.png" width="120" alt="ota-shi" class="rounded-full" />
    ota-meshi
  </a>
  <a href="https://github.com/morinokami">
    <img src="https://github.com/morinokami.png" width="120" alt="Shinya Fujino" class="rounded-full" />
    Shinya Fujino
  </a>
</div>

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

## New Maintainer 🥳

<div class="flex gap-6 flex-wrap mt-12">
  <a href="https://github.com/morinokami">
    <img src="https://github.com/morinokami.png" width="120" alt="Shinya Fujino" class="rounded-full" />
    Shinya Fujino
  </a>
</div>

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

# Astroは順調だ

<div class="mt-4"></div>

## 📈 🚀 🤝

---
class: flex flex-col items-center justify-center h-full
---

## ...本当に？🤔

---
class: flex flex-col items-center justify-center h-full
---

## ここから本題
### Astroのつらみ

---

## シリアライズの壁

<img src="./images/boundary.png" class="mx-auto" alt="境界線の問題" />

---

## nanostores

<img src="./images/nanostore.png" class="mt-10 h-90 mx-auto" alt="nanostores" />

---

## Astroはサーバーで完結させたい
### ComponentPropsとPolymorphicの限界がある

<div class="flex justify-center items-center gap-6 mt-20">
  <img src="./images/logos/react.svg" class="h-20" alt="React" />
  <img src="./images/logos/vue.svg" class="h-20" alt="Vue" />
  <img src="./images/logos/svelte.svg" class="h-20" alt="Svelte" />
  <img src="./images/logos/solid.svg" class="h-20" alt="SolidJS" />
</div>
<div class="flex justify-center items-center gap-6 mt-8">
  <img src="./images/logos/preact.svg" class="h-20" alt="Preact" />
  <img src="./images/logos/alpine-js.svg" class="h-20" alt="Alpine.js" />
  <img src="./images/logos/lit.svg" class="h-20" alt="Lit" />
</div>

---

## Astroのツールチェーン

<img src="./images/vscode.png" class="mt-10 h-90 mx-auto" alt="vscode" />

---
layout: center
class: flex flex-col items-center justify-center h-full
---

# .astroという
# 独自言語が抱える
# 宿命的な課題

---
layout: center
class: flex flex-col justify-center
---

## 話がしたい。話を聞きたい。

---
layout: center
class: flex flex-col justify-center
---

## Astro Japan Community 設立

### 設立したはいいんだけど

---
layout: center
class: flex flex-col justify-center
---

## 🥹 🥹 🥹

<p>もしかしたら、会場提供のお願いとか</p>
<p>登壇依頼するかもしれません。 助けてください🙏</p>

---
layout: center
class: text-center
---

## 終わり

---
layout: center
class: text-center
---

## 休憩

---
layout: center
---

<h2>#Gulp #jQuery #Webpack #EJS</h2>
<h2 class="mt-6">#MPA #SPA</h2>
<h2 class="mt-6">#Vite #Next.js(Turbopack)</h2>
<h2 class="mt-6">#Node #WinterCG(Deno, Bun)</h2>
<h2 class="mt-6">#ホースティングサービス</h2>
<h2 class="mt-6">#Nuxt #React #Svelte #Starlight #Edge</h2>

<div class="mt-6 flex gap-8 flex-wrap justify-center">
  <div class="flex flex-col items-center text-center w-36">
      <img src="./images/jp-knj.png" width="100" class="rounded-full" alt="冨田 健治"/>
  </div>
  <div class="flex flex-col items-center text-center w-36">
    <img src="./images/kyosuke.png" width="100" class="rounded-full" alt="中村 享介" />
    <p class="text-sm !my-0">kyosuke</p>
  </div>
  <div class="flex flex-col items-center text-center w-36">
    <img src="./images/wattanx.png" width="100" class="rounded-full" alt="渡邊 涼太" />
    <p class="text-sm !my-0">wattanx（わったん）</p>
  </div>
  <div class="flex flex-col items-center text-center w-36">
      <img src="./images/yuheiy.png" width="100" class="rounded-full" alt="安田 祐平" />
      <p class="text-sm !my-0">全部入りHTML太郎</p>
  </div>
</div>

---
