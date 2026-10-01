<script setup lang="ts">
import gopher from "../images/logos/gopher-classic.png";
</script>

<template>
  <div class="language-tool-overview" role="group" aria-label="Go Compiler の返却値と Astro Language Server 内部の担当と LSP の通信">
    <section class="language-client">
      <small>Editor の例</small>
      <div class="language-logo-title"><logos-visual-studio-code class="language-logo" aria-hidden="true" /><strong>VS Code</strong></div>
      <span>LSP クライアント</span>
      <small>候補と波線を表示</small>
    </section>

    <div class="language-protocol"><strong>LSP</strong><span>通信の規約</span></div>
    <span class="language-request">変更と要求</span>
    <span class="language-response">補完と診断</span>
    <svg class="language-communication" viewBox="0 0 868 406" aria-hidden="true">
      <path d="M154 179 H281 M273 173 L281 179 L273 185" />
      <path d="M281 223 H154 M162 217 L154 223 L162 229" />
    </svg>

    <section class="language-server">
      <div class="language-server-title language-logo-title"><logos-astro-icon class="language-logo" aria-hidden="true" /><span>Astro Language Server</span></div>
      <div class="language-adapters">
        <div><div class="language-logo-title"><img :src="gopher" class="language-logo" alt="" /><strong>Go Compiler</strong></div><span>TSX と Source map を返す</span><small>元の .astro から生成する</small></div>
        <svg viewBox="0 0 28 24" aria-hidden="true"><path d="M1 12 H25 M19 6 L25 12 L19 18" /></svg>
        <div><strong>Astro の言語対応</strong><span>HTML を作る</span><span>TSX と位置対応を登録する</span></div>
      </div>
      <div class="language-volar"><div class="language-logo-title"><logos-volar class="language-logo" aria-hidden="true" /><strong>Volar</strong></div><span>解析器に渡すコードと、元の位置との対応を管理</span></div>
      <div class="language-services">
        <div class="language-service"><div class="language-logo-title"><logos-html-5 class="language-logo" aria-hidden="true" /><strong>HTML Language Service</strong></div><span>HTML から属性を補完</span></div>
        <div class="language-service"><div class="language-logo-title"><logos-typescript-icon class="language-logo" aria-hidden="true" /><strong>TypeScript</strong></div><span>TSX から型の診断と補完</span></div>
      </div>
      <div class="language-position">Volar が結果を元の位置へ対応させ、サーバーが返す</div>
    </section>
  </div>
</template>

<style scoped>
.language-tool-overview { position: relative; width: 868px; height: 406px; margin-top: 6px; font-family: var(--font-body); }
.language-client { position: absolute; left: 0; top: 133px; width: 150px; height: 144px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; border-radius: 8px; background: #f6f7f9; }
.language-logo-title { display: flex; align-items: center; justify-content: center; gap: 8px; }
.language-logo { flex-shrink: 0; width: 26px; height: 26px; object-fit: contain; }
.language-client strong { color: var(--astro-heading); font-size: 24px; line-height: 32px; }
.language-client span { font-size: 18px; line-height: 26px; }
.language-client small { font-size: 16px; line-height: 24px; }
.language-protocol { position: absolute; left: 154px; top: 94px; width: 127px; text-align: center; }
.language-protocol strong { display: block; color: var(--astro-heading); font-size: 24px; line-height: 32px; }
.language-protocol span { display: block; font-size: 17px; line-height: 24px; }
.language-request, .language-response { position: absolute; left: 154px; width: 127px; text-align: center; font-size: 18px; line-height: 26px; }
.language-request { top: 150px; }
.language-response { top: 231px; }
.language-communication { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.language-communication path, .language-adapters path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.language-server { position: absolute; left: 288px; top: 0; width: 580px; height: 402px; padding: 14px 12px; border: 1.5px solid var(--astro-rule); border-radius: 10px; }
.language-server-title { color: var(--astro-heading); font-size: 24px; font-weight: 600; line-height: 32px; text-align: center; }
.language-adapters { display: grid; grid-template-columns: 248px 28px 252px; gap: 10px; align-items: center; margin-top: 18px; }
.language-adapters > div { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; min-height: 96px; text-align: center; }
.language-adapters strong { color: var(--astro-heading); font-size: 22px; font-weight: 600; line-height: 30px; }
.language-adapters span { font-size: 17px; line-height: 26px; }
.language-adapters small { font-size: 16px; line-height: 24px; }
.language-adapters svg { width: 28px; height: 24px; }
.language-volar { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70px; margin-top: 12px; background: rgba(188, 82, 238, .08); border-radius: 6px; }
.language-volar strong { color: var(--astro-heading); font-size: 22px; line-height: 28px; }
.language-volar span { font-size: 17px; line-height: 26px; }
.language-services { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 12px; }
.language-service { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; min-height: 76px; border-radius: 6px; background: #f6f7f9; text-align: center; }
.language-service span { font-size: 17px; line-height: 26px; }
.language-service strong { font-size: 18px; font-weight: 600; line-height: 26px; }
.language-position { margin-top: 12px; color: var(--astro-heading); font-size: 17px; line-height: 26px; text-align: center; }
</style>
