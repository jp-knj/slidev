<template>
  <section class="answer-overlay">
    <div class="answer-overlay-title"><slot name="title" /></div>
    <div class="answer-overlay-body"><slot /></div>
    <div v-if="$slots.reference" class="answer-overlay-reference">
      <slot name="reference" />
    </div>
  </section>
</template>

<style scoped>
.answer-overlay {
  position: absolute;
  inset: 50% 0 auto;
  transform: translateY(-50%);
  width: 100%;
  box-sizing: border-box;
  z-index: 10;
  display: flex;
  flex-direction: column;
  padding: 24px 32px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 4px 24px rgba(31, 35, 40, 0.14);
  font-family: var(--font-body);
  text-align: left;
}

.answer-overlay-title {
  color: var(--astro-heading);
  font-size: 36px;
  font-weight: 600;
  line-height: 44px;
}

.answer-overlay-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 20px;
  font-size: 24px;
  line-height: 36px;
}

.answer-overlay-body :deep(p) {
  margin: 0;
  line-height: inherit;
}

.answer-overlay-body:empty {
  display: none;
}

.answer-overlay-reference {
  margin-top: 16px;
  font-size: 20px;
  line-height: 28px;
}
</style>
