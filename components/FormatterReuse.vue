<script setup lang="ts">
import ferris from "../images/logos/ferris.svg";
</script>

<template>
  <div class="formatter-reuse" role="group" aria-label="Oxfmt が Astro の Prettier plugin と Rust Compiler を利用する計画">
    <div class="reuse-route">
      <div class="reuse-node reuse-oxfmt">
        <strong><logos-oxc-icon class="reuse-logo" aria-hidden="true" />Oxfmt</strong>
        <div class="reuse-foundation">
          <logos-biomejs-icon class="reuse-logo" aria-hidden="true" />
          <span>Biome Formatter</span>
        </div>
      </div>
      <div class="reuse-link reuse-planned">
        <svg viewBox="0 0 36 24" aria-hidden="true"><path class="reuse-shaft" d="M1 12 H27" /><path class="reuse-arrow" d="M25 6 L35 12 L25 18 Z" /></svg>
      </div>
      <div class="reuse-node">
        <strong><logos-prettier class="reuse-logo" aria-hidden="true" />Prettier plugin</strong>
      </div>
      <div class="reuse-link">
        <svg viewBox="0 0 36 24" aria-hidden="true"><path class="reuse-shaft" d="M1 12 H27" /><path class="reuse-arrow" d="M25 6 L35 12 L25 18 Z" /></svg>
      </div>
      <div class="reuse-node">
        <strong><img :src="ferris" class="reuse-logo reuse-logo-rust" alt="" />Rust Compiler</strong>
      </div>
    </div>
  </div>
</template>

<style scoped>
.formatter-reuse { width: 868px; max-width: 100%; font-family: var(--font-body); color: #17121d; }
.reuse-route { display: grid; grid-template-columns: minmax(0, 1fr) 36px minmax(0, 1fr) 36px minmax(0, 1fr); align-items: center; gap: 10px; }
.reuse-node { display: flex; justify-content: center; align-items: center; height: 80px; padding: 0 10px; background: #fff; border: 1.2px solid #d9d0e4; border-radius: 12px; text-align: center; }
.reuse-node strong { display: flex; justify-content: center; align-items: center; gap: 8px; font-size: 24px; font-weight: 700; line-height: 32px; white-space: nowrap; color: var(--astro-heading); }
.reuse-oxfmt { flex-direction: column; gap: 8px; height: 140px; padding: 12px 10px; }
.reuse-foundation { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; padding: 6px 4px; border: 1px solid #d9d0e4; border-radius: 8px; background: #f2eff8; font-size: 20px; line-height: 28px; color: var(--astro-heading); }
.reuse-logo { width: 26px; height: 26px; flex: none; object-fit: contain; }
.reuse-logo-rust { width: 34px; }
.reuse-link { display: flex; justify-content: center; align-items: center; }
.reuse-link svg { width: 36px; height: 24px; }
.reuse-shaft { fill: none; stroke: #bc52ee; stroke-width: 3; }
.reuse-arrow { fill: #bc52ee; }
.reuse-planned .reuse-shaft { stroke-dasharray: 4 3; }
</style>
