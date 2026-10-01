<script setup lang="ts">
import gopher from "../images/logos/gopher-classic.png";
</script>

<template>
  <div class="source-position-comparison" role="group" aria-label="変換に必要な位置対応と、Compiler の位置計算の不具合の修正を分けた図">
    <section class="position-case">
      <h3>変換に必要な位置対応</h3>
      <div class="position-flow">
        <div class="position-data">
          <div class="position-label"><logos-javascript class="position-logo" aria-hidden="true" />変換後の JavaScript と JSX</div>
          <pre>&lt;&gt;&lt;p&gt;{<span>price</span> * amount}&lt;/p&gt;</pre>
          <div class="position-range">[46, 51)</div>
        </div>
        <div class="position-operation">
          <svg viewBox="0 0 76 24" aria-hidden="true"><path d="M2 12 H71 M63 5 L71 12 L63 19" /></svg>
        </div>
        <div class="position-data">
          <div class="position-label"><logos-astro-icon class="position-logo" aria-hidden="true" />.astro</div>
          <pre>&lt;p&gt;{<span>price</span> * amount}&lt;/p&gt;</pre>
          <div class="position-range">[49, 54)</div>
        </div>
      </div>
    </section>

    <section class="position-case position-bug">
      <h3>Compiler の位置情報の不具合</h3>
      <div class="position-flow">
        <div class="position-data">
          <div class="position-label"><img :src="gopher" class="position-logo position-gopher" alt="" />Go Compiler が返す範囲</div>
          <div class="position-range position-wrong">[47, 80)</div>
          <div class="position-description">波かっこの範囲と一致しない</div>
        </div>
        <div class="position-operation">
          <svg viewBox="0 0 76 24" aria-hidden="true"><path d="M2 12 H71 M63 5 L71 12 L63 19" /></svg>
        </div>
        <div class="position-data">
          <div class="position-label"><logos-astro-icon class="position-logo" aria-hidden="true" />波かっこを含む正しい範囲</div>
          <div class="position-range">[48, 64)</div>
          <pre class="position-expression">{price * amount}</pre>
        </div>
      </div>
    </section>

    <p class="position-owner"><logos-eslint class="position-logo" aria-hidden="true" />両方を astro-eslint-parser が担当していた</p>
    <p class="position-caption">範囲は検証例の全文が基準。上段は price、下段は波かっこを含む範囲。</p>
  </div>
</template>

<style scoped>
.source-position-comparison { width: 868px; font-family: var(--font-body); }
.position-case h3 { margin: 0 0 6px; padding: 0; color: var(--astro-heading); font-size: 22px; font-weight: 600; line-height: 30px; letter-spacing: 0; text-transform: none; }
.position-flow { display: grid; grid-template-columns: 382px 76px 362px; gap: 24px; align-items: center; }
.position-label { display: flex; align-items: center; gap: 8px; min-height: 30px; font-size: 20px; line-height: 28px; }
.position-logo { flex-shrink: 0; width: 24px; height: 24px; }
.position-gopher { object-fit: contain; }
.position-data pre { margin: 6px 0 0; padding: 8px; border-radius: 6px; background: var(--slidev-code-background); font-family: var(--font-mono); font-size: 24px; line-height: 32px; white-space: pre; }
.position-data pre span { color: var(--astro-heading); background: rgba(188, 82, 238, .12); }
.position-range { margin-top: 4px; color: var(--astro-heading); font-family: var(--font-mono); font-size: 24px; line-height: 32px; }
.position-operation { display: flex; flex-direction: column; align-items: center; gap: 4px; text-align: center; font-size: 20px; line-height: 28px; }
.position-operation svg { width: 76px; height: 24px; }
.position-operation path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.position-bug { margin-top: 14px; padding-top: 10px; border-top: 1px solid var(--astro-rule); }
.position-wrong { color: #a03e2c; }
.position-description { margin-top: 4px; font-size: 20px; line-height: 28px; }
.position-data .position-expression { padding: 0; border: 0; border-radius: 0; background: transparent; }
.position-owner { display: flex; align-items: center; justify-content: center; gap: 10px; margin: 12px 0 0; color: var(--astro-heading); font-size: 22px; font-weight: 600; line-height: 30px; }
.position-caption { margin: 10px 0 0; font-size: 17px; line-height: 24px; }
</style>
