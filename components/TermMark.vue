<script setup lang="ts">
defineProps<{ n?: number }>();
</script>

<template>
  <sup class="term-mark">※{{ n }}</sup>
</template>

<style scoped>
.term-mark {
  margin-left: 2px;
  color: var(--astro-muted, #62516d);
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 400;
  line-height: 1;
  vertical-align: super;
}
</style>
