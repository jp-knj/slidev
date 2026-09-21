<script setup lang="ts">
withDefaults(
  defineProps<{
    /** 参照先URL。省略すると出典名だけを表示する */
    href?: string;
    /** スライド下端へ固定せず、その場に流し込む */
    inline?: boolean;
  }>(),
  { inline: false },
);
</script>

<template>
  <div class="ref-note" :class="inline ? 'ref-inline' : 'ref-pinned'">
    <a v-if="href" :href="href" target="_blank" rel="noreferrer">
      <slot />
    </a>
    <span v-else><slot /></span>
  </div>
</template>

<style scoped>
.ref-note {
  font-size: 20px;
  line-height: 1.4;
  color: var(--astro-muted, #6b7280);
}

.ref-note:hover {
  color: #7611a6;
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

.ref-note a {
  color: inherit;
  border-bottom: 1px solid #d9d3e2;
}

.ref-note a:hover {
  color: #7611a6;
  border-bottom-color: #bc52ee;
}
</style>
