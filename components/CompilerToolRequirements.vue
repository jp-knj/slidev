<script setup lang="ts">
import gopher from "../images/logos/gopher-classic.png";
</script>

<template>
  <div class="compiler-tool-requirements" role="group" aria-label="Go Compiler が返した情報と、ESLint と Prettier と Language Tool が担った仕事">
    <div class="requirements-columns">
      <section class="requirements-compiler">
        <h3><img :src="gopher" class="requirements-logo requirements-gopher" alt="" />Go Compiler が返した情報</h3>
        <ul class="requirements-information">
          <li><strong>JavaScript expression は文字列</strong><span>識別子と演算子の AST がない</span></li>
          <li><strong>Astro AST の位置に不具合</strong><span>波かっこの範囲が不正確</span></li>
          <li><strong>TSX と Source map</strong><span>型の検査に渡すコードと位置の対応</span></li>
        </ul>
      </section>

      <svg class="requirements-arrow" viewBox="0 0 56 24" aria-hidden="true"><path d="M2 12 H51 M43 5 L51 12 L43 19" /></svg>

      <section class="requirements-tools">
        <h3>ツールが担っていた仕事</h3>
        <ul class="requirements-tool-list">
          <li>
            <div class="requirements-tool-name"><logos-eslint class="requirements-logo" aria-hidden="true" /><strong>ESLint</strong></div>
            <p>パースし直し、位置の不具合も修正</p>
          </li>
          <li>
            <div class="requirements-tool-name"><logos-prettier class="requirements-logo" aria-hidden="true" /><strong>Prettier</strong></div>
            <p>コードを再生成してパースし直す</p>
          </li>
          <li>
            <div class="requirements-tool-name"><logos-astro-icon class="requirements-logo" aria-hidden="true" /><strong>Language Tool</strong></div>
            <p>HTML を作り、TSX と位置を<br />Volar に登録して診断と補完につなぐ</p>
          </li>
        </ul>
      </section>
    </div>
    <div class="requirements-takeaway">AST の不足と位置の不具合に、ツールでも対応していた</div>
  </div>
</template>

<style scoped>
.compiler-tool-requirements { width: 868px; font-family: var(--font-body); color: var(--astro-body); }
.requirements-columns { display: grid; grid-template-columns: 364px 56px 400px; gap: 24px; align-items: start; }
.compiler-tool-requirements h3 { display: flex; align-items: center; gap: 10px; margin: 0 0 22px; padding: 0; color: var(--astro-body); font-size: 22px; font-weight: 600; line-height: 32px; letter-spacing: 0; text-transform: none; }
.requirements-logo { flex-shrink: 0; width: 28px; height: 28px; }
.requirements-gopher { object-fit: contain; }
.requirements-information { display: flex; flex-direction: column; gap: 27px; margin: 0; padding: 20px 14px 22px 32px; background: #f6f7f9; border-radius: 8px; list-style: disc; }
.requirements-information li { margin: 0; padding-left: 1px; font-size: 20px; line-height: 30px; }
.requirements-information strong, .requirements-tool-name strong { color: var(--astro-body); font-weight: 600; }
.requirements-information span { display: block; margin-top: 4px; font-size: 18px; line-height: 28px; }
.requirements-arrow { width: 56px; height: 24px; margin-top: 176px; }
.requirements-arrow path { fill: none; stroke: #9a90ab; stroke-width: 2; }
.requirements-tool-list { display: flex; flex-direction: column; gap: 22px; margin: 0; padding: 0; list-style: none; }
.requirements-tool-list li { margin: 0; padding: 0; }
.requirements-tool-name { display: flex; align-items: center; gap: 10px; font-size: 22px; line-height: 30px; }
.requirements-tool-list p { margin: 5px 0 0 38px; color: var(--astro-body); font-size: 20px; line-height: 30px; }
.requirements-takeaway { margin-top: 26px; color: var(--astro-heading); font-size: 25px; font-weight: 600; line-height: 36px; }
</style>
