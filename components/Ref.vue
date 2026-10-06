<script setup lang="ts">
withDefaults(
  defineProps<{
    /** 参照先 URL。省略した場合は slot に li を渡す */
    href?: string;
    /** スライド下端へ固定せず、その場に流し込む */
    inline?: boolean;
  }>(),
  { inline: false },
);
</script>

<template>
  <div class="ref-note" :class="inline ? 'ref-inline' : 'ref-pinned'">
    <ul class="ref-list" aria-label="参照資料">
      <li v-if="href">
        <a :href="href" target="_blank" rel="noreferrer"><slot /></a>
      </li>
      <slot v-else />
    </ul>
  </div>
</template>

<style scoped>
.ref-note {
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 24px;
  color: var(--astro-muted, #6b7280);
}

.ref-list {
  display: grid;
  gap: 2px;
  margin: 0;
  padding: 0 0 0 1.2em;
  list-style: disc;
}

.ref-list :deep(li) {
  margin: 0;
  padding: 0;
  font-size: inherit;
  line-height: inherit;
}

.ref-list :deep(li::marker) {
  color: inherit;
}

.ref-pinned {
  position: absolute;
  left: 3.5rem;
  right: 3.5rem;
  bottom: 1.5rem;
  text-align: left;
}

.ref-inline {
  margin-top: 1rem;
}

.ref-note :deep(a) {
  color: inherit;
  border-bottom: 1px solid #d9d3e2;
}

.ref-note :deep(a:hover) {
  color: #7611a6;
  border-bottom-color: #bc52ee;
}
</style>
