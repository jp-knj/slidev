<script setup lang="ts">
import ferris from "../images/logos/ferris.svg";
</script>

<template>
  <div class="formatter-reuse" role="group" aria-label="Oxfmt が Astro の Prettier plugin と Rust Compiler を利用する計画">
    <div class="reuse-route">
      <div class="reuse-node">
        <strong><logos-oxc-icon class="reuse-logo" aria-hidden="true" />Oxfmt</strong>
        <span>既存の plugin を<br />利用する計画</span>
      </div>
      <div class="reuse-link reuse-planned">
        <span>利用</span>
        <svg viewBox="0 0 36 24" aria-hidden="true"><path d="M1 12 H33 M26 5 L33 12 L26 19" /></svg>
      </div>
      <div class="reuse-node">
        <strong><logos-prettier class="reuse-logo" aria-hidden="true" /><span>Astro の<br />Prettier plugin</span></strong>
        <span>Compiler から<br />AST を受け取る</span>
      </div>
      <div class="reuse-link">
        <span>呼ぶ</span>
        <svg viewBox="0 0 36 24" aria-hidden="true"><path d="M1 12 H33 M26 5 L33 12 L26 19" /></svg>
      </div>
      <div class="reuse-node">
        <strong><img :src="ferris" class="reuse-logo" alt="" />Rust Compiler</strong>
        <span>Astro Template Syntax<br />をパースする</span>
      </div>
    </div>
    <p class="reuse-caption">Compiler と plugin を、別の Formatter でも再利用する</p>
  </div>
</template>

<style scoped>
.formatter-reuse { width: 868px; font-family: var(--font-body); color: #17121d; }
.reuse-route { display: grid; grid-template-columns: minmax(0, 1fr) 36px minmax(0, 1fr) 36px minmax(0, 1fr); align-items: stretch; gap: 10px; }
.reuse-node { display: flex; flex-direction: column; justify-content: center; gap: 16px; min-height: 176px; padding: 16px 8px; background: #f6f4f8; border: 1px solid var(--astro-rule); border-radius: 6px; text-align: center; }
.reuse-node strong { display: flex; justify-content: center; align-items: center; gap: 8px; min-height: 60px; font-size: 22px; font-weight: 600; line-height: 30px; color: var(--astro-heading); }
.reuse-logo { width: 26px; height: 26px; flex: none; object-fit: contain; }
.reuse-node > span { font-size: 20px; line-height: 28px; }
.reuse-link { display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 4px; font-size: 16px; line-height: 24px; }
.reuse-link svg { width: 36px; height: 24px; }
.reuse-link path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.reuse-planned path { stroke-dasharray: 3 3; }
.formatter-reuse .reuse-caption { margin: 28px 0 0; font-size: 24px; line-height: 32px; }
</style>
