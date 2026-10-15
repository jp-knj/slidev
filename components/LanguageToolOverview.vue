<template>
  <div class="language-tool-overview" role="group" aria-label="Go Compiler が TSX と Source map を Language Tool へ渡す">
    <Overview
      layout="language"
      visible="source,compiler,output,editor"
      highlight="source,compiler,output,editor"
      compiler-frame
      :term-markers="{ output: true }"
    />
    <p class="language-purpose">TypeScript が型を調べ、Language Tool が診断を .astro の位置に戻す。</p>
    <p class="language-challenge">JavaScript の構文を独自に判別し、TSX を作り続ける必要があった。</p>
  </div>
</template>

<style scoped>
.language-tool-overview { width: 868px; font-family: var(--font-body); }
.language-tool-overview .language-purpose { margin: 24px 0 0; font-size: 20px; line-height: 28px; }
.language-tool-overview .language-challenge { margin: 16px 0 0; font-size: 20px; line-height: 28px; }
</style>
