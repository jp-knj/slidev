<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    /** adopted | wip | proposed | poc */
    kind?: string;
    /** 対象バージョンなどの補足。例: "Astro 6.4" */
    version?: string;
  }>(),
  { kind: "proposed" },
);

const KINDS: Record<string, { label: string; tone: string }> = {
  adopted: { label: "採用済み", tone: "#167A4D" },
  wip: { label: "開発中", tone: "#0A6FAF" },
  proposed: { label: "提案中", tone: "#946008" },
  poc: { label: "PoC", tone: "#656B78" },
};

const meta = computed(() => KINDS[props.kind] ?? KINDS.proposed);
</script>

<template>
  <span
    class="status-badge"
    :style="{
      color: meta.tone,
      borderColor: meta.tone,
      backgroundColor: `${meta.tone}1f`,
    }"
  >
    <slot>{{ meta.label }}</slot>
    <span v-if="version" class="status-version">{{ version }}</span>
  </span>
</template>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: baseline;
  gap: 0.45em;
  border: 1px solid;
  border-radius: 999px;
  padding: 0.12em 0.8em;
  font-size: 20px;
  line-height: 1.5;
  white-space: nowrap;
}

.status-version {
  font-size: 20px;
  opacity: 0.75;
}
</style>
