<template>
  <div class="language-tool-routes" role="group" aria-label="astro2tsx が生成する TSX と位置対応を、Volar と Content Mapper の二つの経路で使う">
    <svg class="routes-lines" viewBox="0 0 868 350" aria-hidden="true">
      <path d="M110 44 H154 M146 37 L154 44 L146 51" />
      <path d="M482 44 H540 M532 37 L540 44 L532 51" />
      <path d="M707 88 V108 H235 V122 M228 114 L235 122 L242 114" />
      <path d="M707 108 H685 V122 M678 114 L685 122 L692 114" />
      <path d="M125 216 V264 M118 224 L125 216 L132 224 M118 256 L125 264 L132 256" />
      <path d="M373 210 V264 M366 256 L373 264 L380 256" />
      <path d="M685 210 V264 M678 256 L685 264 L692 256" />
    </svg>

    <div class="routes-node routes-input"><strong>.astro</strong></div>
    <div class="routes-node routes-generator routes-accent">
      <strong>@astrojs/astro2tsx</strong>
      <span>Rust と Biome で TSX を生成</span>
    </div>
    <div class="routes-node routes-output">
      <strong>TSX の文字列と位置対応</strong>
    </div>

    <div class="routes-node routes-language-tool routes-accent">
      <strong>Astro Language Tool</strong>
      <span>Volar に TSX と位置対応を登録</span>
    </div>
    <div class="routes-node routes-mapper">
      <strong>Content Mapper</strong>
      <span>@astrojs/ts-content-mapper</span>
    </div>

    <span class="routes-edge routes-api-edge">要求と結果</span>
    <span class="routes-edge routes-editor-edge">.astro の位置へ</span>
    <span class="routes-edge routes-mapper-edge">コードと位置対応を返す</span>

    <div class="routes-node routes-typescript-api">
      <strong>TypeScript</strong>
      <span>JavaScript API</span>
    </div>
    <div class="routes-node routes-editor">
      <strong>Editor</strong>
      <span>補完と診断</span>
    </div>
    <div class="routes-node routes-typescript-native routes-accent">
      <strong>TypeScript 7.1 以降</strong>
      <span>tsc が型検査と位置対応を担当</span>
    </div>
  </div>
</template>

<style scoped>
.language-tool-routes { position: relative; width: 868px; height: 350px; font-family: var(--font-body); }
.routes-lines { position: absolute; inset: 0; width: 100%; height: 100%; }
.routes-lines path { fill: none; stroke: #887294; stroke-width: 1.8; stroke-linejoin: round; }
.routes-node { position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; padding: 8px; border: 1px solid #d9d0df; border-radius: 9px; background: #faf9fc; text-align: center; }
.routes-node strong { font-size: 24px; line-height: 32px; font-weight: 600; color: var(--astro-heading); }
.routes-node span { font-size: 18px; line-height: 26px; }
.routes-accent { border-color: #bc52ee; background: #f7effb; }
.routes-input { left: 0; top: 0; width: 110px; height: 88px; }
.routes-generator { left: 160px; top: 0; width: 322px; height: 88px; }
.routes-output { left: 546px; top: 0; width: 322px; height: 88px; }
.routes-output strong { color: var(--astro-body); }
.routes-language-tool { left: 0; top: 128px; width: 470px; height: 82px; }
.routes-mapper { left: 502px; top: 128px; width: 366px; height: 82px; }
.routes-edge { position: absolute; top: 226px; padding: 0 6px; background: white; font-size: 18px; line-height: 26px; white-space: nowrap; transform: translateX(-50%); }
.routes-api-edge { left: 125px; }
.routes-editor-edge { left: 373px; }
.routes-mapper-edge { left: 685px; }
.routes-typescript-api { left: 0; top: 270px; width: 250px; height: 80px; }
.routes-editor { left: 276px; top: 270px; width: 194px; height: 80px; }
.routes-typescript-native { left: 502px; top: 270px; width: 366px; height: 80px; }
</style>
