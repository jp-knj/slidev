<template>
  <div class="content-mapper-flow" role="group" aria-label="Astro の外部プラグイン Content Mapper と TypeScript の連携">
    <div class="mapper-row">
      <div class="mapper-source"><logos-astro-icon class="mapper-logo" aria-hidden="true" /><strong>.astro</strong></div>
      <svg class="mapper-arrow" viewBox="0 0 28 24" aria-hidden="true"><path d="M1 12 H25 M18 5 L25 12 L18 19" /></svg>
      <section class="mapper-astro">
        <h3><logos-astro-icon class="mapper-logo" aria-hidden="true" />Astro</h3>
        <div class="mapper-node"><strong>Content Mapper</strong></div>
      </section>
      <div class="mapper-transfer">
        <svg viewBox="0 0 132 24" aria-hidden="true"><path d="M2 12 H127 M119 4 L127 12 L119 20" /></svg>
      </div>
      <section class="mapper-typescript">
        <h3><logos-typescript-icon class="mapper-logo" aria-hidden="true" />TypeScript 7.1</h3>
        <div class="mapper-node"><strong>.astro の診断</strong></div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.content-mapper-flow { width: 868px; max-width: 100%; font-family: var(--font-body); }
.mapper-row { display: grid; grid-template-columns: 140px 28px 232px 132px 288px; gap: 12px; align-items: center; }
.mapper-source { display: flex; align-items: center; justify-content: center; gap: 8px; min-height: 70px; border-bottom: 3px solid #bc52ee; }
.mapper-source strong, .mapper-node strong { font-size: 24px; line-height: 32px; font-weight: 600; color: var(--astro-heading); white-space: nowrap; }
.mapper-astro { padding: 16px 10px; border: 1.2px solid #d9d0e4; border-radius: 12px; background: #fff; }
.mapper-typescript { padding: 16px; border: 1.2px solid #bc52ee; border-radius: 12px; background: #f2eff8; }
.content-mapper-flow h3 { display: flex; justify-content: center; align-items: center; gap: 8px; margin: 0 0 12px; padding: 0; font-size: 24px; line-height: 32px; font-weight: 600; color: var(--astro-heading); letter-spacing: 0; text-transform: none; white-space: nowrap; }
.mapper-node { display: flex; align-items: center; justify-content: center; gap: 8px; min-height: 60px; padding: 8px; border: 1px solid #d9d0e4; border-radius: 8px; background: #fff; }
.mapper-logo { width: 26px; height: 26px; flex: none; }
.mapper-arrow { width: 28px; height: 24px; }
.mapper-transfer svg { display: block; width: 132px; height: 24px; }
.content-mapper-flow path { fill: none; stroke: #bc52ee; stroke-width: 2; }
</style>
