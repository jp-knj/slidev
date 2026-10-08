<script setup lang="ts">
defineProps<{ notes: string[] }>();
</script>

<template>
  <aside class="term-notes" aria-label="用語の補足">
    <ul class="term-notes-list">
      <li v-for="(note, i) in notes" :key="note">
        <span class="term-notes-marker">※{{ notes.length > 1 ? i + 1 : '' }}</span>
        <span>{{ note }}</span>
      </li>
    </ul>
    <slot />
  </aside>
</template>

<style scoped>
.term-notes {
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 22px;
  color: var(--astro-muted, #62516d);
  text-align: left;
}
.term-notes-list {
  display: grid;
  gap: 2px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.term-notes-list > li {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin: 0;
  padding: 0;
  font-size: inherit;
  line-height: inherit;
}
.term-notes-marker { flex: none; }
.term-notes :deep(.ref-inline) { margin-top: 8px; }
</style>
