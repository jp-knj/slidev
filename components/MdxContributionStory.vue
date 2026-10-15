<template>
  <div class="mdx-proposal-story" role="group" aria-label="Rust の MDX Compiler の統合、AST Bridge、markdown-rs のフックを提案した">
    <div class="proposal-columns">
      <section class="proposal-column">
        <p class="proposal-date">2025 年 7 月</p>
        <h3>Astro への統合を提案</h3>
        <div class="proposal-flow">
          <div class="proposal-node">
            <span class="proposal-emoji" aria-hidden="true">🦀</span>
            <span>Rust Compiler</span>
          </div>
          <svg class="proposal-arrow" viewBox="0 0 28 24" aria-hidden="true"><path d="M1 12 H25 M18 5 L25 12 L18 19" /></svg>
          <div class="proposal-node">
            <span class="proposal-emoji" aria-hidden="true">🚀</span>
            <span>Astro</span>
          </div>
        </div>
        <p class="proposal-purpose">MDX を速くしたい</p>
      </section>

      <section class="proposal-column">
        <p class="proposal-date">2025 年 8 月</p>
        <h3>AST Bridge<TermMark :n="1" /> を提案</h3>
        <div class="proposal-flow">
          <div class="proposal-node">
            <span class="proposal-emoji" aria-hidden="true">🌳</span>
            <span>Rust の AST</span>
          </div>
          <svg class="proposal-arrow" viewBox="0 0 28 24" aria-hidden="true"><path d="M1 12 H25 M18 5 L25 12 L18 19" /></svg>
          <div class="proposal-node">
            <span class="proposal-emoji" aria-hidden="true">🧩</span>
            <span>JavaScript<br />plugin</span>
          </div>
        </div>
        <p class="proposal-purpose">remark と rehype<TermMark :n="2" /><br />も使いたい</p>
      </section>

      <section class="proposal-column">
        <p class="proposal-date">2025 年 8 月</p>
        <h3>markdown-rs に提案</h3>
        <div class="proposal-flow proposal-rust-flow">
          <div class="proposal-node">
            <span class="proposal-emoji" aria-hidden="true">🌳</span>
            <span>AST</span>
          </div>
          <svg class="proposal-arrow" viewBox="0 0 28 24" aria-hidden="true"><path d="M1 12 H25 M18 5 L25 12 L18 19" /></svg>
          <div class="proposal-node proposal-plugin">
            <span class="proposal-emoji" aria-hidden="true">🧩</span>
            <span>plugin</span>
          </div>
          <svg class="proposal-arrow" viewBox="0 0 28 24" aria-hidden="true"><path d="M1 12 H25 M18 5 L25 12 L18 19" /></svg>
          <div class="proposal-node">
            <span class="proposal-emoji" aria-hidden="true">🌳</span>
            <span>AST</span>
          </div>
        </div>
        <p class="proposal-purpose">Rust の中で AST を変更<br />JavaScript との往復を減らす</p>
      </section>
    </div>
    <p class="proposal-community"><span aria-hidden="true">🤝</span>試作をきっかけに、交流がはじまった。</p>
  </div>
</template>

<style scoped>
.mdx-proposal-story { width: 868px; font-family: var(--font-body); }
.proposal-columns { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; }
.proposal-column { min-width: 0; }
.proposal-column .proposal-date { margin: 0 0 4px; font-size: 16px; line-height: 22px; color: #62516d; }
.proposal-column h3 { margin: 0 0 14px; padding: 0; font-size: 22px; line-height: 30px; font-weight: 600; color: var(--astro-heading); letter-spacing: 0; text-transform: none; }
.proposal-flow { display: grid; grid-template-columns: minmax(0, 1fr) 28px minmax(0, 1fr); align-items: center; }
.proposal-node { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; height: 110px; padding: 6px 2px; border: 1px solid #d9d0df; border-radius: 12px; background: #faf9fc; text-align: center; font-size: 18px; line-height: 24px; }
.proposal-emoji { font-family: "Apple Color Emoji", "Segoe UI Emoji", sans-serif; font-size: 34px; line-height: 40px; }
.proposal-arrow { width: 28px; height: 24px; }
.proposal-arrow path { fill: none; stroke: #887294; stroke-width: 1.8; stroke-linejoin: round; }
.proposal-rust-flow { grid-template-columns: minmax(0, 1fr) 24px 76px 24px minmax(0, 1fr); }
.proposal-rust-flow .proposal-arrow { width: 24px; }
.proposal-plugin { background: #f7effb; border-color: #bc52ee; }
.proposal-column .proposal-purpose { margin: 12px 0 0; font-size: 18px; line-height: 26px; }
.mdx-proposal-story .proposal-community { display: flex; align-items: center; gap: 16px; margin: 20px 0 0; font-size: 24px; line-height: 36px; font-weight: 500; }
.proposal-community > span { font-family: "Apple Color Emoji", "Segoe UI Emoji", sans-serif; font-size: 32px; white-space: nowrap; }
</style>
