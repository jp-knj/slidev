<template>
  <div class="formatter-responsibilities" role="group" aria-label="Compiler が提供してほしい情報と Formatter の担当">
    <div class="formatter-columns">
      <section>
        <h3><logos-astro-icon class="formatter-logo" aria-hidden="true" />Compiler に求める情報</h3>
        <div class="formatter-information"><strong>JavaScript expression の AST</strong><p>識別子と演算子をたどれること</p></div>
        <div class="formatter-information"><strong>Astro の記述と正確な位置</strong><p>タグとコメントも取得できること</p></div>
      </section>
      <section>
        <h3><logos-prettier class="formatter-logo" aria-hidden="true" />Formatter の担当</h3>
        <div class="formatter-information"><strong>Prettier に AST を渡す</strong><p>必要な形式へ変換する</p></div>
        <div class="formatter-information"><strong>改行と字下げを決める</strong><p>Doc を作り、行幅に合わせて整形する</p></div>
      </section>
    </div>
    <div class="formatter-goal">AST を得るまでの再生成と再解析を減らす</div>
  </div>
</template>

<style scoped>
.formatter-responsibilities { width: 868px; font-family: var(--font-body); }
.formatter-columns { display: grid; grid-template-columns: 410px 422px; gap: 36px; margin-top: 18px; }
.formatter-columns h3 { display: flex; align-items: center; gap: 8px; margin: 0 0 12px; padding: 0; color: var(--astro-heading); font-size: 24px; font-weight: 600; line-height: 32px; letter-spacing: 0; text-transform: none; }
.formatter-logo { width: 28px; height: 28px; flex-shrink: 0; }
.formatter-information { min-height: 108px; }
.formatter-information + .formatter-information { margin-top: 22px; }
.formatter-information strong { font-size: 24px; font-weight: 500; line-height: 32px; }
.formatter-information p { margin: 7px 0 0; font-size: 21px; line-height: 32px; }
.formatter-goal { margin-top: 26px; color: var(--astro-heading); font-size: 26px; font-weight: 600; line-height: 36px; }
</style>
