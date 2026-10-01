<template>
  <div class="formatter-reuse">
    <section aria-label="公開済みの Astro の Prettier plugin の呼び出し関係">
      <div class="reuse-heading"><logos-prettier aria-hidden="true" /><strong>Prettier plugin は公開済み</strong></div>
      <div class="reuse-route">
        <div class="reuse-node"><strong>Prettier</strong><span>Doc から<br />整形後のコードを作る</span></div>
        <div class="reuse-arrow"><span>呼ぶ</span><svg viewBox="0 0 36 24" aria-hidden="true"><path d="M1 12 H33 M26 5 L33 12 L26 19" /></svg></div>
        <div class="reuse-node"><strong>Astro plugin</strong><span>AST を調整し、<br />Prettier と Doc を作る</span></div>
        <div class="reuse-arrow"><span>呼ぶ</span><svg viewBox="0 0 36 24" aria-hidden="true"><path d="M1 12 H33 M26 5 L33 12 L26 19" /></svg></div>
        <div class="reuse-node reuse-compiler"><strong><logos-astro-icon aria-hidden="true" />Rust Compiler</strong><span>Astro と JavaScript の<br />AST を返す</span></div>
      </div>
      <p class="reuse-caption">AST を整形ツールでも利用する</p>
    </section>

    <section class="reuse-planned" aria-label="Oxfmt の Astro 対応計画。まだ提供されていない">
      <div class="reuse-heading"><logos-oxc-icon aria-hidden="true" /><strong>Oxfmt の Astro 対応は計画中</strong></div>
      <div class="reuse-route">
        <div class="reuse-node"><strong>Oxfmt</strong><span>Oxc の Formatter</span></div>
        <div class="reuse-arrow"><span>利用</span><svg viewBox="0 0 36 24" aria-hidden="true"><path d="M1 12 H33 M26 5 L33 12 L26 19" /></svg></div>
        <div class="reuse-node"><strong>Prettier と<br />Astro plugin</strong></div>
        <div class="reuse-arrow"><span>利用</span><svg viewBox="0 0 36 24" aria-hidden="true"><path d="M1 12 H33 M26 5 L33 12 L26 19" /></svg></div>
        <div class="reuse-node reuse-compiler"><strong><logos-astro-icon aria-hidden="true" />Rust Compiler</strong><span>既存の実装を利用</span></div>
      </div>
      <p class="reuse-caption">別のツールでも、Compiler と plugin を再利用する計画</p>
    </section>
    <div class="reuse-date">2026 年 10 月 1 日の公式資料で確認</div>
  </div>
</template>

<style scoped>
.formatter-reuse { font-family: var(--font-body); color: #17121d; margin-top: 24px; }
.reuse-heading { display: flex; gap: 10px; align-items: center; font-size: 24px; line-height: 32px; color: var(--astro-heading); }
.reuse-heading > svg { width: 28px; height: 28px; flex: none; }
.reuse-heading strong { font-weight: 600; }
.reuse-route { display: grid; grid-template-columns: minmax(0, 1fr) 42px minmax(0, 1.12fr) 42px minmax(0, 1.18fr); align-items: stretch; gap: 10px; margin-top: 12px; }
.reuse-node { display: flex; flex-direction: column; justify-content: center; gap: 6px; min-height: 96px; padding: 10px 8px; background: #f6f4f8; border-radius: 8px; text-align: center; }
.reuse-node strong { display: flex; justify-content: center; align-items: center; gap: 6px; font-size: 22px; font-weight: 600; line-height: 30px; }
.reuse-node strong > svg { width: 24px; height: 24px; flex: none; }
.reuse-node span { font-size: 19px; line-height: 27px; }
.reuse-compiler { background: #f0e3f8; }
.reuse-arrow { display: flex; flex-direction: column; justify-content: center; gap: 4px; align-items: center; font-size: 16px; line-height: 22px; }
.reuse-arrow svg { width: 36px; height: 24px; }
.reuse-arrow path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.formatter-reuse .reuse-caption { margin: 9px 0 0; font-size: 20px; line-height: 28px; }
.reuse-planned { margin-top: 26px; }
.reuse-planned .reuse-node { min-height: 78px; }
.reuse-planned .reuse-arrow path { stroke-dasharray: 3 3; }
.reuse-date { margin-top: 12px; font-size: 16px; line-height: 24px; color: #63596d; }
</style>
