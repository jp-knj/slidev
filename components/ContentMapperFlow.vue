<template>
  <div class="content-mapper-flow" role="group" aria-label="Astro の Content Mapper が Biome でパースし、TSX と位置対応を TypeScript に返す">
    <div class="mapper-row">
      <section class="mapper-node">
        <h3>Astro</h3>
        <p>Biome でパース<br />TSX と位置対応を生成</p>
      </section>
      <div class="mapper-result-arrow">
        <p>TSX と<br />位置対応</p>
        <svg viewBox="0 0 84 24" aria-hidden="true"><path d="M2 12 H79 M71 4 L79 12 L71 20" /></svg>
      </div>
      <section class="mapper-node">
        <h3>Content Mapper</h3>
        <p>コードと位置対応を<br />返す</p>
      </section>
      <div class="mapper-result-arrow">
        <p>コードと<br />位置対応</p>
        <svg viewBox="0 0 84 24" aria-hidden="true"><path d="M2 12 H79 M71 4 L79 12 L71 20" /></svg>
      </div>
      <section class="mapper-node mapper-typescript">
        <h3>TypeScript 7.1</h3>
        <p>補完と診断<br />位置対応を使う</p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.content-mapper-flow { width: 868px; font-family: var(--font-body); }
.mapper-row { display: grid; grid-template-columns: 228px 92px 248px 92px 208px; align-items: center; }
.mapper-node { display: flex; flex-direction: column; justify-content: center; min-height: 152px; padding: 10px; border: 1px solid #d9d0df; border-radius: 8px; background: #faf9fc; }
.mapper-node h3 { margin: 0 0 12px; padding: 0; font-size: 24px; line-height: 32px; font-weight: 600; color: var(--astro-heading); letter-spacing: 0; text-transform: none; }
.mapper-node p { margin: 0; font-size: 20px; line-height: 28px; }
.mapper-result-arrow p { margin: 0 0 6px; text-align: center; font-size: 18px; line-height: 26px; }
.mapper-result-arrow svg { display: block; width: 84px; height: 24px; margin: 0 auto; }
.content-mapper-flow path { fill: none; stroke: #887294; stroke-width: 2; }
.mapper-typescript { border-color: #bc52ee; background: #f7effb; }
</style>
