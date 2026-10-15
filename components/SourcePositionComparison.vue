<script setup lang="ts">
import gopher from "../images/logos/gopher-cutout.png";
</script>

<template>
  <div class="source-position-comparison" role="group" aria-label="変換に必要な位置対応と、Compiler の位置計算の不具合の修正を分けた図">
    <section class="position-case">
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
      <div class="position-flow">
        <div class="position-data position-compiler" role="group" aria-label="Go Compiler が返す Astro AST の位置情報">
          <div class="position-label position-compiler-heading"><img :src="gopher" class="position-logo position-gopher" alt="" />Go Compiler</div>
          <pre>position: {
  start: { offset: <span>47</span> },
  end: { offset: <span>80</span> }
}</pre>
          <div class="position-description">波かっこの範囲と一致しない</div>
        </div>
        <div class="position-operation">
          <svg viewBox="0 0 76 24" aria-hidden="true"><path d="M2 12 H71 M63 5 L71 12 L63 19" /></svg>
        </div>
        <div class="position-data">
          <div class="position-label"><logos-astro-icon class="position-logo" aria-hidden="true" />波かっこを含む正しい範囲</div>
          <pre>position: {
  start: { offset: <span>48</span> },
  end: { offset: <span>64</span> }
}</pre>
          <pre class="position-expression">{price * amount}</pre>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.source-position-comparison { width: 868px; font-family: var(--font-body); }
.position-flow { display: grid; grid-template-columns: 394px 60px 366px; gap: 24px; align-items: center; }
.position-label { display: flex; align-items: center; gap: 8px; min-height: 30px; font-size: 20px; line-height: 28px; }
.position-logo { flex-shrink: 0; width: 24px; height: 24px; }
.position-gopher { object-fit: contain; }
.position-compiler { padding: 12px; border: 1.2px solid #d9d0e4; border-radius: 12px; background: #fff; }
.position-compiler-heading { color: var(--astro-heading); font-weight: 600; }
.position-data pre { margin: 6px 0 0; padding: 16px; border-radius: 6px; background: var(--slidev-code-background); font-family: var(--font-mono); font-size: 24px; line-height: 32px; white-space: pre; }
.position-data pre span { color: var(--astro-heading); background: rgba(188, 82, 238, .12); }
.position-range { margin-top: 4px; color: var(--astro-heading); font-family: var(--font-mono); font-size: 24px; line-height: 32px; }
.position-operation { display: flex; flex-direction: column; align-items: center; gap: 4px; text-align: center; font-size: 20px; line-height: 28px; }
.position-operation svg { width: 60px; height: 24px; }
.position-operation path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.position-bug { margin-top: 14px; padding-top: 24px; border-top: 1px solid var(--astro-rule); }
.position-wrong { color: #a03e2c; }
.position-description { margin-top: 4px; font-size: 20px; line-height: 28px; }
.position-data .position-expression { padding: 0; border: 0; border-radius: 0; background: transparent; }
</style>
