<script setup lang="ts">
import gopher from "../images/logos/gopher-cutout.png";
defineProps<{ step: number }>();
</script>

<template>
  <div class="formatter-failure" role="group" aria-label="空の Fragment を含む expression のパースと文字列化と整形エラー">
    <div class="failure-label"><logos-astro-icon class="failure-logo" aria-hidden="true" />元の .astro</div>
    <pre class="failure-code"><code>{true ? &lt;p&gt;OK&lt;/p&gt; : <span>&lt;&gt;&lt;/&gt;</span>}</code></pre>
    <div class="failure-route">
      <div><div class="failure-label"><img :src="gopher" class="failure-logo" alt="" />Go Compiler</div><strong>Astro AST を返す</strong><span>TextNode とタグの node</span></div>
      <svg viewBox="0 0 44 24" aria-hidden="true"><path d="M1 12 H40 M33 5 L40 12 L33 19" /></svg>
      <div><div class="failure-label"><logos-prettier class="failure-logo" aria-hidden="true" />Astro plugin</div><strong>タグを文字列に戻し<br />TextNode の値と連結</strong></div>
      <svg viewBox="0 0 44 24" aria-hidden="true"><path d="M1 12 H40 M33 5 L40 12 L33 19" /></svg>
      <div><div class="failure-label"><logos-babel class="failure-logo" aria-hidden="true" />Babel</div><strong>再パースする</strong></div>
    </div>
    <div class="failure-generated" :class="{ 'is-revealed': step >= 1 }">
      <div class="failure-label">空の Fragment を文字列に戻すと、不正なタグになる</div>
      <pre class="failure-code"><code>true ? &lt;p&gt;OK&lt;/p&gt; : <span class="failure-invalid">&lt; /&gt;</span></code></pre>
    </div>
    <div class="failure-result" :class="{ 'is-revealed': step >= 2 }">Babel が構文エラーを返し、整形できない</div>
  </div>
</template>

<style scoped>
.formatter-failure { width: 868px; font-family: var(--font-body); }
.failure-label { display: flex; align-items: center; gap: 8px; color: var(--astro-heading); font-size: 20px; font-weight: 600; line-height: 28px; }
.failure-logo { width: 26px; height: 26px; flex-shrink: 0; object-fit: contain; }
.failure-code { margin: 7px 0 0; padding: 10px 16px; background: #f6f7f9; border: 1px solid var(--astro-rule); border-radius: 6px; font-family: var(--font-mono); font-size: 24px; line-height: 32px; }
.failure-code code { padding: 0; background: none; font: inherit; }
.failure-code span { color: var(--astro-heading); font-weight: 600; }
.failure-route { display: grid; grid-template-columns: 240px 44px 252px 44px 240px; gap: 12px; align-items: start; margin-top: 26px; }
.failure-route > div { display: flex; flex-direction: column; gap: 4px; }
.failure-route strong { font-size: 22px; font-weight: 500; line-height: 30px; }
.failure-route span { font-size: 17px; line-height: 26px; }
.failure-route > svg { width: 44px; height: 24px; margin-top: 34px; }
.failure-route > svg path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.failure-generated { margin-top: 24px; visibility: hidden; }
.failure-result { margin-top: 18px; color: var(--astro-heading); font-size: 24px; font-weight: 600; line-height: 32px; visibility: hidden; }
.is-revealed { visibility: visible; }
.failure-code .failure-invalid { color: var(--astro-heading); text-decoration: underline wavy; text-underline-offset: 5px; }
</style>
