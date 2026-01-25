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
class: text-left flex flex-col justify-center h-full
----

## Astro 2026
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
            <li>Astroの現在地</li>
            <li>現場が抱える「痛み」</li>
            <li>持続可能なエコシステム</li>
        </ol>
    </div>
</div>

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

## Astroは静的ジェネレーターなのか 🤔

---
layout: cover
class: center
---

<div class="mt-8">
  <div class="text-2xl text-white font-light mb-4 text-opacity-60">静的サイトジェネレーターではなく</div>
  <div class="text-5xl font-black text-white filter drop-shadow-lg">
    コンテンツ駆動
  </div>
  <div class="text-2xl text-white font-light mt-4 text-opacity-60">としてがんばってきた</div>
</div>

---
layout: section
---

# 1. コンテンツ駆動の深化
## ファイル管理からデータ基盤へ

---
layout: default
---

## Content Layer API

<div class="grid grid-cols-2 gap-8 mt-10">
  <div class="relative p-6 rounded-xl bg-transparent border border-white/30">
    <div class="absolute -top-4 left-4 bg-white/20 text-white px-3 py-1 text-xs rounded-full font-bold">BEFORE</div>
    <h2 class="font-bold"><span class="text-opacity-30">File Based Management</span></h2>
  </div>
  <div class="relative p-6 rounded-xl bg-transparent border-2 border-white">
      <div class="absolute -top-4 left-4 bg-purple-600 text-white px-3 py-1 text-xs rounded-full font-bold">AFTER</div>
    <h2 class="font-bold text-white">Content Layer</h2>
    Gatsby + GraphQL + Webpack
    Astro + SQLite + zod + Vite
  </div>
</div>
<div class="mt-8 p-4 text-center">
  <span class="font-bold text-white">Live CollectionsでHMRで瞬時にプレビューへ反映。リビルド不要</span>
</div>

---
layout: section
---

# 2. パフォーマンスの再定義
## Islands から Server Islands へ

---
layout: center
---

## Server Islands

**速さと動的のトレードオフを解消**

<div class="flex items-center justify-between gap-4 w-full mt-8">
  <div class="flex-1 text-center min-w-0">
    <div class="bg-transparent border border-white/30 p-6 rounded-lg mb-4 h-32 flex items-center justify-center">
      <span class="text-4xl">🖼️</span>
    </div>
    <h4 class="font-bold text-white whitespace-nowrap overflow-visible">1. Static Shell</h4>
  </div>

  <div class="text-2xl text-white flex-shrink-0">➜</div>

  <div class="flex-1 text-center min-w-0">
    <div class="bg-transparent p-6 rounded-lg mb-4 h-32 flex items-center justify-center border-2 border-white/30">
      <span class="text-4xl animate-pulse">⚙️</span>
    </div>
    <h4 class="font-bold text-white whitespace-nowrap overflow-visible">2. Server Defer</h4>
  </div>

  <div class="text-2xl text-white flex-shrink-0">➜</div>

  <div class="flex-1 text-center min-w-0">
      <div class="bg-transparent p-6 rounded-lg mb-4 h-32 flex items-center justify-center border-2 border-white/30">
      <span class="text-4xl">👤</span>
    </div>
    <h4 class="font-bold text-white whitespace-nowrap overflow-visible">3. Injection</h4>
  </div>

</div>

---
layout: section
---

# 3. アプリケーション基盤の強化
## SaaS開発を支える標準化

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
    <div class="border-2 py-2 border-white/30 flex-grow flex items-center justify-center rounded mb-4 bg-black/20">
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
      <div class="bg-white/20 rounded flex items-center justify-center text-xs text-white font-bold">AWS</div>
      <div class="bg-white/20 rounded flex items-center justify-center text-xs text-white font-bold">Vercel</div>
      <div class="bg-white/20 rounded flex items-center justify-center text-xs text-white font-bold">Cloudflare</div>
      <div class="bg-white/20 rounded flex items-center justify-center text-xs text-white font-bold">Node</div>
    </div>
  </div>
</div>

---
layout: section
---

# 4. 開発基盤の刷新
## Vite Environment API への移行

---
layout: center
---

## Vite Environment API移行

**複雑なレンダリング環境を、開発環境で分離・再現**

<div class="mt-8 flex gap-8">

  <div class="w-1/2 flex flex-col gap-4">
    <div class="bg-transparent border border-white/30 p-4 rounded-lg text-center border-l-4">
      <span class="font-bold block text-white">Browser Runtime</span>
    </div>
    <div class="bg-transparent border border-white/30 p-4 rounded-lg text-center border-l-4">
      <span class="font-bold block text-white">Node.js Runtime</span>
    </div>
    <div class="bg-transparent border border-white/30 p-4 rounded-lg text-center border-l-4">
      <span class="font-bold block text-white">Edge Runtime</span>
    </div>
  </div>

  <div class="w-1/2 flex flex-col justify-center gap-6">
    <div>
      <p class="text-left">
        複雑な構成でも<br/>
        本番環境と同じ挙動を<br/>
        ローカルで再現。
      </p>
    </div>
  </div>
</div>

---
layout: center
class: flex flex-col items-center justify-center h-full
---

## 技術的な成熟が、どのように信頼に繋がったか

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

## Astro Community

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

## ❤️ Sponsors / Donations
## ↓
## Open Collective 🏦
## ↓
## Contributors / Goods / Events
## 💬 Support Squad

---
layout: cover
class: flex flex-col items-center justify-center h-full
---

## Astro AwardsとEcosystem Fund 🤝

<div class="flex gap-6 flex-wrap mt-12">
  <a href="https://github.com/ktym4a">
    <img src="https://github.com/ktym4a.png" width="120" alt="ktym4a" class="rounded-full" />
    ktym4a
  </a>
  <a href="https://github.com/kyosuke">
    <img src="https://github.com/kyosuke.png" width="120" alt="Kyosuke" class="rounded-full" />
    kyosuke
  </a>
  <a href="https://github.com/pilcrowonpaper" class="flex flex-col items-center justify-center h-full">
    <img src="https://github.com/pilcrowonpaper.png" width="120" alt="pilcrow" class="rounded-full" />
    pilcrowonpaper
  </a>
  <a href="https://github.com/ota-meshi">
    <img src="https://github.com/ota-meshi.png" width="120" alt="ota-shi" class="rounded-full" />
    ota-meshi
  </a>
  <a href="https://github.com/morinokami">
    <img src="https://github.com/morinokami.png" width="120" alt="Shinya Fujino" class="rounded-full" />
    morinokami
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
    morinokami
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

## ここから、本題

---

## 境界線の問題

サーバーサイドで実行される領域とタイミング
ブラウザで実行される領域とタイミング

---

## 型システムの制約

.astroファイルの独自構文とTypeScriptの型システムのあいだ

---

## Astroのツールチェーン


---

## nanostores

---
class: flex flex-col items-center justify-center h-full
---

## うーん 🤔

---
layout: center
class: flex flex-col items-center justify-center h-full
---

# Astroという
# 独自言語が抱える
# 宿命的な課題

---
layout: center
class: flex flex-col justify-center
---

## セーフティネット

---
layout: center
class: flex flex-col justify-center
---

## Astro Japan Community 設立

---
layout: center
class: text-center
---

# 迷ったら、資産を選ぶ

<div class="mt-4 mb-12 opacity-80">
  その行動は、未来に残るか
</div>

---
layout: center
class: text-center
---

# 終わり
### Questions / Feedback / Demo follow-up
