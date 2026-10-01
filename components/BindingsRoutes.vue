<template>
  <div class="bindings-routes">
    <p class="bindings-definition">bindings は、関数の呼び出しと値の受け渡しを担う</p>
    <div class="bindings-columns">
      <section>
        <h3>NAPI-RS <span class="bindings-reading">ナピ アールエス</span></h3>
        <p>Node-API を使う bindings を<br />Rust で実装する</p>
        <div class="bindings-node"><logos-nodejs-icon aria-hidden="true" /><strong>Node.js の JavaScript</strong></div>
        <div class="bindings-path"><svg viewBox="0 0 24 60" aria-hidden="true"><path d="M12 2 V58 M5 9 L12 2 L19 9 M5 51 L12 58 L19 51" /></svg><span>Node-API bindings</span></div>
        <div class="bindings-node"><img src="/images/logos/ferris.svg" alt="" /><strong>ネイティブの実装</strong></div>
        <div class="bindings-footnote">対応する OS と CPU を決め、<br />バイナリをビルドして配布する</div>
      </section>
      <section>
        <h3>wasm-bindgen</h3>
        <p>JavaScript と WASM の呼び出しと<br />値の受け渡しを支えるコードを作る</p>
        <div class="bindings-node"><logos-javascript aria-hidden="true" /><strong>JavaScript</strong></div>
        <div class="bindings-path"><svg viewBox="0 0 24 60" aria-hidden="true"><path d="M12 2 V58 M5 9 L12 2 L19 9 M5 51 L12 58 L19 51" /></svg><span>wasm-bindgen の bindings</span></div>
        <div class="bindings-node"><logos-webassembly aria-hidden="true" /><strong>WASM の実装</strong></div>
        <div class="bindings-footnote">WASM と補助コードを配布し、<br />対応する実行環境で動かす</div>
      </section>
    </div>
    <div class="bindings-example">採用後も続く、対応環境ごとのビルドとテストと配布</div>
  </div>
</template>

<style scoped>
.bindings-routes { color: #17121d; font-size: 22px; line-height: 30px; }
.bindings-routes .bindings-definition { margin: 0 0 16px; font-size: 22px; line-height: 30px; }
.bindings-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.bindings-columns > section { min-width: 0; }
.bindings-columns h3 { margin: 0; color: var(--astro-heading); font-size: 26px; line-height: 34px; }
.bindings-reading { margin-left: 8px; color: #55505c; font-size: 17px; font-weight: 400; }
.bindings-columns p { margin: 6px 0 14px; font-size: 20px; line-height: 28px; }
.bindings-node { display: flex; align-items: center; justify-content: center; gap: 14px; min-height: 55px; padding: 8px 12px; border-radius: 8px; background: #f3edf7; }
.bindings-node > svg, .bindings-node > img { width: 30px; height: 30px; object-fit: contain; flex: none; }
.bindings-node strong { font-size: 22px; font-weight: 500; line-height: 30px; }
.bindings-path { display: flex; align-items: center; justify-content: center; gap: 14px; height: 68px; font-size: 20px; line-height: 28px; }
.bindings-path svg { width: 24px; height: 60px; }
.bindings-path path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.bindings-footnote { margin-top: 12px; text-align: center; font-size: 20px; line-height: 28px; }
.bindings-example { margin-top: 20px; color: var(--astro-heading); font-size: 24px; font-weight: 600; line-height: 32px; }
</style>
