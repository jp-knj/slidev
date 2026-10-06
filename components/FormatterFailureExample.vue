<script setup lang="ts">
import gopher from "../images/logos/gopher-cutout.png";
defineProps<{ step: number }>();
</script>

<template>
  <div class="formatter-failure" role="group" aria-label="Astro AST とプラグインが作る文字列と Babel のパース">
    <div class="failure-source">
      <div class="failure-label"><logos-astro-icon class="failure-logo" aria-hidden="true" />元の .astro</div>
      <pre class="failure-code"><code>{true ? &lt;p&gt;OK&lt;/p&gt; : <span>&lt;&gt;&lt;/&gt;</span>}</code></pre>
    </div>

    <div class="failure-stage">
      <section v-if="step === 0">
        <h3 class="failure-label"><img :src="gopher" class="failure-logo" alt="" />Go Compiler が返す Astro AST</h3>
        <pre class="failure-code"><code>expression
├─ TextNode.value  "true ? "
├─ p
│  └─ TextNode.value  "OK"
├─ TextNode.value  " : "
└─ <span>Fragment  children: []</span></code></pre>
        <p class="failure-caption">JavaScript expression 全体の AST はない</p>
      </section>

      <section v-else-if="step === 1">
        <h3 class="failure-label"><logos-prettier class="failure-logo" aria-hidden="true" />Astro plugin が文字列を連結する</h3>
        <div class="failure-pieces">
          <code>  "true ? "</code><span>TextNode.value をそのまま使う</span>
          <code>+ "&lt;p&gt;OK&lt;/p&gt;"</code><span>p 要素を文字列に戻す</span>
          <code>+ " : "</code><span>TextNode.value をそのまま使う</span>
          <code>+ "<span class="failure-invalid">&lt; /&gt;</span>"</code><span>空の Fragment が不正なタグになる</span>
        </div>
        <pre class="failure-code failure-joined"><code>true ? &lt;p&gt;OK&lt;/p&gt; : <span class="failure-invalid">&lt; /&gt;</span></code></pre>
      </section>

      <section v-else>
        <h3 class="failure-label"><logos-babel class="failure-logo" aria-hidden="true" />Babel がパースするコード</h3>
        <pre class="failure-code"><code><span class="failure-wrapper">&lt;&gt;{</span>true ? &lt;p&gt;OK&lt;/p&gt; : <span class="failure-invalid">&lt; /&gt;</span>
<span class="failure-wrapper">}&lt;/&gt;</span></code></pre>
        <p class="failure-caption">expression の AST を得るため、JSX で囲んで再パースする</p>
        <div class="failure-error">
          <code>Unexpected token</code>
          <p>構文エラーで、整形を始められない</p>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.formatter-failure { width: 868px; font-family: var(--font-body); }
.failure-source { display: grid; grid-template-columns: 150px 1fr; gap: 12px; align-items: center; }
.formatter-failure .failure-label { display: flex; align-items: center; gap: 8px; margin: 0; color: var(--astro-heading); font-size: 20px; font-weight: 600; line-height: 28px; text-transform: none; letter-spacing: 0; }
.failure-logo { width: 26px; height: 26px; flex-shrink: 0; object-fit: contain; }
.failure-code { margin: 8px 0 0; padding: 8px 16px; background: #f6f7f9; border: 1px solid var(--astro-rule); border-radius: 6px; font-family: var(--font-mono); font-size: 24px; line-height: 32px; }
.failure-source .failure-code { margin: 0; }
.failure-code code { padding: 0; background: none; font: inherit; }
.failure-code span { color: var(--astro-heading); font-weight: 600; }
.failure-stage { height: 296px; margin-top: 20px; }
.formatter-failure .failure-caption { margin: 12px 0 0; font-size: 20px; line-height: 28px; }
.failure-pieces { display: grid; grid-template-columns: 280px 1fr; column-gap: 28px; row-gap: 4px; margin-top: 8px; padding: 8px 16px; border: 1px solid var(--astro-rule); border-radius: 6px; background: #f6f7f9; align-items: center; }
.failure-pieces > code, .failure-error > code { padding: 0; border: 0; border-radius: 0; background: none; color: inherit; font-family: var(--font-mono); font-size: 24px; line-height: 32px; white-space: pre; }
.failure-pieces > span { font-size: 20px; line-height: 28px; }
.failure-joined { margin-top: 16px; }
.failure-invalid { color: var(--astro-heading); text-decoration: underline wavy; text-underline-offset: 5px; }
.failure-code .failure-wrapper { color: #706b79; font-weight: 400; }
.failure-error { margin-top: 24px; color: var(--astro-heading); }
.formatter-failure .failure-error p { margin: 8px 0 0; font-size: 24px; font-weight: 600; line-height: 32px; }
</style>
