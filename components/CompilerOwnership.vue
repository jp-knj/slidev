<script setup lang="ts">
import lightningCssLogo from "../images/tools/lightning-css.svg";
</script>

<template>
  <div class="compiler-ownership" role="group" aria-label="ライブラリの機能を利用し、Astro が実装して保守する範囲">
    <section>
      <h3>利用する基盤</h3>
      <div class="ownership-libraries">
        <div class="ownership-card">
          <strong class="ownership-brand"><logos-oxc-icon class="ownership-logo" aria-hidden="true" />Oxc</strong>
          <p>JavaScript と TypeScript<br />Parser と AST と変換</p>
        </div>
        <div class="ownership-card">
          <strong class="ownership-brand"><img :src="lightningCssLogo" class="ownership-logo" alt="" />Lightning CSS</strong>
          <p>CSS のパースと出力</p>
        </div>
      </div>
    </section>
    <div class="ownership-connection" aria-hidden="true">
      <span>利用</span>
      <svg viewBox="0 0 64 32"><path d="M2 16 H60 M49 5 L60 16 L49 27" /></svg>
    </div>
    <section>
      <h3 class="ownership-brand"><logos-astro-icon class="ownership-logo" aria-hidden="true" />Astro が実装して保守</h3>
      <div class="ownership-card ownership-astro">
        <div><strong>Astro Template Syntax</strong><p>タグと Component script への対応</p></div>
        <div><strong>Astro Codegen</strong><p>Astro の実行コードを生成</p></div>
        <div><strong>CSS スコープ規則</strong><p>スタイルをコンポーネントに限定</p></div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.compiler-ownership { display: grid; grid-template-columns: 350px 64px 422px; gap: 16px; width: 868px; font-family: var(--font-body); }
.compiler-ownership h3 { margin: 0 0 18px; padding: 0; font-size: 24px; line-height: 32px; font-weight: 600; color: var(--astro-heading); letter-spacing: 0; text-transform: none; }
.ownership-libraries { display: grid; grid-template-rows: 154px 122px; gap: 16px; }
.ownership-card { display: flex; flex-direction: column; justify-content: center; padding: 20px 24px; border: 1px solid #d9d0df; border-radius: 9px; background: #faf9fc; }
.ownership-card strong { font-size: 24px; line-height: 32px; font-weight: 600; color: var(--astro-heading); }
.ownership-brand { display: flex; align-items: center; gap: 12px; }
.ownership-logo { width: 32px; height: 32px; flex: 0 0 32px; object-fit: contain; }
.ownership-card p { margin: 8px 0 0; font-size: 20px; line-height: 28px; }
.ownership-astro { height: 292px; gap: 18px; background: #f7effb; border-color: #bc52ee; }
.ownership-astro p { margin-top: 2px; }
.ownership-connection { display: flex; flex-direction: column; justify-content: center; gap: 8px; padding-top: 50px; text-align: center; font-size: 20px; line-height: 28px; }
.ownership-connection svg { width: 64px; height: 32px; }
.ownership-connection path { fill: none; stroke: #887294; stroke-width: 2; }
</style>
