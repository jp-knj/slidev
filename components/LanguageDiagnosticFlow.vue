<template>
  <div class="diagnostic-flow" role="group" aria-label="Compiler の TSX と Source map を使い、TypeScript の診断を Volar で元のコードへ対応させて Editor に返す">
    <div class="diagnostic-inputs">
      <div><strong>Compiler が返す TSX</strong><span>TypeScript が検査するコード</span></div>
      <div><strong>Compiler が返す Source map</strong><span>生成コードと元のコードの位置の対応表</span></div>
    </div>
    <div class="diagnostic-paths">
      <section><svg class="diagnostic-down" viewBox="0 0 24 26" aria-hidden="true"><path d="M12 0 V23 M6 17 L12 23 L18 17" /></svg><div class="diagnostic-owner"><logos-typescript-icon class="diagnostic-logo" aria-hidden="true" /><strong>TypeScript</strong></div><span>型にないプロパティを診断</span><pre><code>{product.<mark>nmae</mark>}</code></pre><small>診断は TSX の文字位置を指す</small></section>
      <section><svg class="diagnostic-down" viewBox="0 0 24 26" aria-hidden="true"><path d="M12 0 V23 M6 17 L12 23 L18 17" /></svg><div class="diagnostic-owner"><logos-astro-icon class="diagnostic-logo" aria-hidden="true" /><strong>Astro の言語対応</strong></div><span>Source map の形式を変換</span><div class="diagnostic-mapping">Volar の位置対応データ</div><small>元の文字と生成後の文字を対応させる</small></section>
    </div>
    <svg class="diagnostic-merge" viewBox="0 0 868 30" aria-hidden="true"><path d="M210 0 V12 H434 M658 0 V12 H434 M434 12 V27 M428 21 L434 27 L440 21" /></svg>
    <div class="diagnostic-volar"><logos-volar class="diagnostic-logo" aria-hidden="true" /><strong>Volar</strong><span>診断の範囲を元の .astro へ対応させる</span></div>
    <div class="diagnostic-return"><svg viewBox="0 0 24 30" aria-hidden="true"><path d="M12 0 V27 M6 21 L12 27 L18 21" /></svg><span>Astro Language Server が LSP で返す</span></div>
    <div class="diagnostic-editor"><div class="diagnostic-owner"><logos-visual-studio-code class="diagnostic-logo" aria-hidden="true" /><strong>Editor</strong></div><pre><code>{product.<mark>nmae</mark>}</code></pre><span>元の 4 文字に波線を表示</span></div>
  </div>
</template>

<style scoped>
.diagnostic-flow { width: 868px; font-family: var(--font-body); }
.diagnostic-inputs, .diagnostic-paths { display: grid; grid-template-columns: 420px 420px; gap: 28px; }
.diagnostic-inputs > div { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.diagnostic-inputs strong { color: var(--astro-heading); font-size: 24px; font-weight: 600; line-height: 32px; }
.diagnostic-inputs span { font-size: 18px; line-height: 26px; }
.diagnostic-paths section { display: flex; flex-direction: column; align-items: center; gap: 4px; text-align: center; }
.diagnostic-down { width: 24px; height: 26px; margin: 5px auto 4px; }
.diagnostic-flow path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.diagnostic-owner { display: flex; align-items: center; gap: 8px; }
.diagnostic-owner strong { font-size: 24px; font-weight: 500; line-height: 32px; }
.diagnostic-logo { width: 28px; height: 28px; flex-shrink: 0; }
.diagnostic-paths span { font-size: 20px; line-height: 28px; }
.diagnostic-paths small { font-size: 17px; line-height: 26px; }
.diagnostic-flow pre { margin: 0; padding: 6px 14px; border: 1px solid var(--astro-rule); border-radius: 5px; background: #f6f7f9; font-family: var(--font-mono); font-size: 24px; line-height: 32px; }
.diagnostic-flow pre code { padding: 0; background: none; font: inherit; }
.diagnostic-flow mark { padding: 0; color: inherit; background: #fcece9; text-decoration: underline wavy #943f32; text-underline-offset: 5px; }
.diagnostic-mapping { display: flex; align-items: center; height: 46px; padding: 6px 14px; border-radius: 5px; background: #f6f7f9; font-size: 22px; line-height: 32px; }
.diagnostic-merge { display: block; width: 868px; height: 30px; margin-top: 6px; }
.diagnostic-volar { display: flex; align-items: center; justify-content: center; gap: 12px; padding: 10px; border-radius: 6px; background: rgba(188, 82, 238, .08); color: var(--astro-heading); }
.diagnostic-volar strong { font-size: 24px; font-weight: 600; line-height: 32px; }
.diagnostic-volar span { font-size: 22px; line-height: 32px; }
.diagnostic-return { display: flex; align-items: center; justify-content: center; gap: 12px; height: 42px; font-size: 18px; line-height: 28px; }
.diagnostic-return svg { width: 24px; height: 30px; }
.diagnostic-editor { display: flex; align-items: center; justify-content: center; gap: 20px; }
.diagnostic-editor span { font-size: 20px; line-height: 28px; }
</style>
