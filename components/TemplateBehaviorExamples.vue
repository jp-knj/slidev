<script setup lang="ts">
defineProps<{ whitespace?: boolean }>();
</script>

<template>
  <div class="template-behavior" role="group" :aria-label="whitespace ? 'JSX の空白規則による表示' : 'Compiler が書かれた親子関係を保つ例'">
    <h3>{{ whitespace ? '空白を JSX の規則で扱う' : '書かれた親子関係を保つ' }}</h3>
    <div class="behavior-flow">
      <section>
        <div class="text-primary font-600 text-xl mb-1 flex items-center gap-2"><logos-astro-icon class="w-5 h-5 shrink-0" aria-hidden="true" />.astro</div>
        <slot v-if="!whitespace" name="table-source" />
        <slot v-else name="whitespace-source" />
      </section>
      <section>
        <div class="text-primary font-600 text-xl mb-1 flex items-center gap-2"><logos-html-5 v-if="!whitespace" class="w-5 h-5" aria-hidden="true" />{{ whitespace ? 'ブラウザでの表示' : '生成された HTML' }}</div>
        <slot v-if="!whitespace" name="table-output" />
        <div v-else class="behavior-preview"><span>Hello</span><span>World</span></div>
      </section>
    </div>
    <p v-if="!whitespace" class="behavior-takeaway">Compiler は HTML correction を行わない。</p>
    <p v-else class="behavior-takeaway">Astro v7 は標準で <code>compressHTML: 'jsx'</code></p>
  </div>
</template>

<style scoped>
.template-behavior { width: 868px; font-family: var(--font-body); }
.template-behavior h3 { margin: 0 0 24px; padding: 0; font-size: 24px; line-height: 32px; font-weight: 600; color: var(--astro-heading); letter-spacing: 0; text-transform: none; }
.behavior-flow { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: start; gap: 32px; min-height: 212px; }
.behavior-flow section { min-width: 0; }
.behavior-preview { display: flex; align-items: center; justify-content: center; height: 90px; margin: 16px 0; border: 1px solid var(--astro-rule); border-radius: 12px; font-size: 36px; line-height: 44px; }
.template-behavior .behavior-takeaway { margin: 28px 0 0; font-size: 22px; line-height: 32px; }
</style>
