<script setup lang="ts">
defineProps<{ stage: 1 | 2 | 3 }>();
</script>

<template>
  <div class="formatting-information">
    <template v-if="stage === 1">
      <section class="data-route-group">
        <div class="data-route-title"><logos-prettier class="data-logo" aria-hidden="true" />Astro の Prettier plugin で必要だった対応</div>
        <div class="data-route">
          <div><strong>Go Compiler</strong><span>JavaScript expression の<br />AST が足りない</span></div>
          <svg viewBox="0 0 30 24" aria-hidden="true"><path d="M1 12 H27 M20 5 L27 12 L20 19" /></svg>
          <div><strong>コードを作り直す</strong><span>Babel でパースし直し、<br />JavaScript の AST を取得</span></div>
          <svg viewBox="0 0 30 24" aria-hidden="true"><path d="M1 12 H27 M20 5 L27 12 L20 19" /></svg>
          <div><strong>Prettier</strong><span>AST とコメントから<br />整形する</span></div>
        </div>
        <div class="data-route-note">空の Fragment が不正なタグになり、整形が止まった例もあった</div>
      </section>

      <section class="data-route-group">
        <div class="data-route-title"><logos-biomejs-icon class="data-logo" aria-hidden="true" />JavaScript の設計例：Biome</div>
        <div class="data-route">
          <div><strong>JavaScript</strong><span>入力したコード</span></div>
          <svg viewBox="0 0 30 24" aria-hidden="true"><path d="M1 12 H27 M20 5 L27 12 L20 19" /></svg>
          <div class="data-emphasis"><strong>Lossless CST</strong><span>構文に加えて、<br />元の空白とコメントも保持</span></div>
          <svg viewBox="0 0 30 24" aria-hidden="true"><path d="M1 12 H27 M20 5 L27 12 L20 19" /></svg>
          <div><strong>Formatter と Linter</strong><span>整形とコードの修正に<br />同じ情報を使える</span></div>
        </div>
      </section>
      <div class="data-takeaway">ツールの基盤から、どんな情報を受け取れるか</div>
    </template>

    <template v-else-if="stage === 2">
      <div class="information-compare">
        <div class="information-input">
          <div class="data-subtitle">同じ JavaScript のコードで比較</div>
          <pre class="data-source"><code>price<span class="data-spaces">  </span>* amount; <span class="data-comment">// 税込</span>
</code></pre>
        </div>
        <div class="information-columns">
          <section>
            <div class="data-route-title"><logos-prettier class="data-logo" aria-hidden="true" />Prettier と Babel</div>
            <h3>AST とコメント</h3>
            <pre class="data-tree"><code>BinaryExpression
├─ Identifier: price
├─ operator: "*"
└─ Identifier: amount

comments: <span class="data-trivia">["// 税込"]</span></code></pre>
            <p>空白は元のコードを参照する。</p>
          </section>
          <section>
            <div class="data-route-title"><logos-biomejs-icon class="data-logo" aria-hidden="true" />Biome</div>
            <h3>Lossless CST の模式図</h3>
            <pre class="data-tree"><code>ExpressionStatement
├─ BinaryExpression
│  ├─ price <span class="data-trivia">["  "]</span>
│  ├─ "*" <span class="data-trivia">[" "]</span>
│  └─ amount
└─ ";" <span class="data-trivia">[" ", "// 税込", "\n"]</span></code></pre>
            <p>紫は空白とコメントと改行。</p>
          </section>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="data-edit-intent">この 1 か所の <code>price</code> を <code>unitPrice</code> に変えたい</div>
      <div class="data-edit-label">変更前</div>
      <pre class="data-source"><code><span class="data-name">price</span><span class="data-spaces">  </span>* amount; <span class="data-comment">// 税込</span>
</code></pre>
      <div class="data-edit-action"><svg viewBox="0 0 24 28" aria-hidden="true"><path d="M12 1 V25 M5 18 L12 25 L19 18" /></svg><span>CST の名前の部分だけを変更</span></div>
      <div class="data-edit-label">変更後</div>
      <pre class="data-source"><code><span class="data-name">unitPrice</span><span class="data-spaces">  </span>* amount; <span class="data-comment">// 税込</span>
</code></pre>
      <div class="data-edit-kept">空白 2 文字とコメントと末尾の改行は、そのまま</div>
      <div class="data-takeaway">変更しない部分の書式を保ったまま、修正できる</div>
      <p class="data-caption data-edit-caption">整形では、Prettier も Biome も空白と改行を決め直す</p>
    </template>
  </div>
</template>

<style scoped>
.formatting-information { color: #17121d; font-size: 22px; line-height: 30px; }
.data-logo { width: 27px; height: 27px; flex: 0 0 auto; }
.data-route-title { display: flex; align-items: center; gap: 10px; color: var(--astro-heading); font-size: 24px; font-weight: 600; line-height: 32px; }
.data-route-group + .data-route-group { margin-top: 26px; }
.data-route { display: grid; grid-template-columns: minmax(0, 1fr) 30px minmax(0, 1.1fr) 30px minmax(0, 1fr); align-items: center; gap: 12px; margin-top: 12px; }
.data-route > div { align-self: stretch; padding: 12px 10px; border-radius: 8px; background: #f6f4f8; text-align: center; }
.data-route strong { display: block; font-size: 22px; font-weight: 600; line-height: 30px; }
.data-route span { display: block; margin-top: 5px; font-size: 19px; line-height: 27px; }
.data-route > .data-emphasis { background: #f0e3f8; }
.data-route svg { width: 30px; height: 24px; }
.data-route path, .data-edit-action path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.data-route-note { margin-top: 9px; font-size: 20px; line-height: 28px; }
.data-takeaway { margin-top: 22px; color: var(--astro-heading); font-size: 24px; font-weight: 600; line-height: 32px; }
.data-source, .data-tree { margin: 0; padding: 12px 16px; border-radius: 8px; background: var(--slidev-code-background); font-size: 24px; line-height: 32px; }
.data-source code, .data-tree code { padding: 0; background: transparent; font-size: 24px; line-height: 32px; }
.data-source { white-space: pre; }
.data-spaces { background: #ead4f4; border-radius: 2px; }
.data-comment { color: #55505c; }
.data-name { color: var(--astro-heading); font-weight: 600; }
.data-comparison { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 32px; margin-top: 18px; }
.data-comparison > section { min-width: 0; }
.data-subtitle { margin-top: 5px; margin-bottom: 8px; font-size: 20px; line-height: 28px; }
.data-tree { padding: 8px 12px; }
.data-detail { margin-top: 8px; font-size: 20px; line-height: 28px; }
.formatting-information .data-caption { margin: 8px 0 0; font-size: 19px; line-height: 27px; }
.data-preserved { display: grid; gap: 4px; }
.data-preserved > div { display: grid; grid-template-columns: 88px minmax(0, 1fr); align-items: center; padding: 6px 10px; font-size: 19px; line-height: 27px; border-radius: 6px; }
.data-preserved strong { font-weight: 500; }
.data-preserved .data-retained { background: #f2eaf7; }
.data-definitions { display: grid; gap: 2px; margin-top: 16px; font-size: 19px; line-height: 27px; }
.data-definitions > div { display: grid; grid-template-columns: 105px 1fr; }
.data-definitions strong { color: var(--astro-heading); font-weight: 600; }
.data-edit-intent { margin-bottom: 18px; font-size: 22px; line-height: 30px; }
.data-edit-label { margin-bottom: 6px; font-size: 20px; line-height: 28px; }
.data-edit-action { display: flex; align-items: center; gap: 14px; margin: 14px 0; font-size: 22px; line-height: 30px; }
.data-edit-action svg { width: 24px; height: 28px; }
.data-edit-kept { margin-top: 12px; font-size: 22px; line-height: 30px; }
.formatting-information .data-edit-caption { margin-top: 12px; }
/* Stage 2: align the comparison rows and reserve space for the definition. */
.information-input .data-subtitle { margin-top: 0; }
.information-input .data-source { padding-top: 8px; padding-bottom: 8px; }
.information-columns { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 32px; margin-top: 16px; }
.information-columns section { min-width: 0; }
.information-columns h3 { margin: 8px 0 8px; padding: 0; font-size: 22px; line-height: 30px; letter-spacing: 0; text-transform: none; }
.information-columns p { margin: 12px 0 0; font-size: 20px; line-height: 28px; }
.information-kept { display: flex; flex-direction: column; justify-content: center; gap: 8px; min-height: 144px; padding: 12px 16px; border-radius: 8px; background: var(--slidev-code-background); font-size: 22px; line-height: 30px; }
.information-definition { margin-top: 16px; font-size: 20px; line-height: 28px; }
/* Stage 2: six tree rows must fit beside the AST without wrapping token text. */
.information-columns .data-tree, .information-columns .data-tree code, .information-input .data-source, .information-input .data-source code { font-size: 22px; line-height: 30px; }
.information-columns .data-tree { min-height: 196px; }
.data-trivia { color: var(--astro-heading); }
</style>
