import { defineShikiSetup } from "@slidev/types";

/**
 * コードフェンスに `word:title` と書くと、その語のトークンへ .code-word を付ける。
 * @shikijs/transformers を足さずに、語単位の強調だけを実現するための最小実装。
 * 装飾の見た目は theme-light/styles/layout.css 側に置く。
 */
const wordHighlight = {
  name: "slidev:word-highlight",
  span(this: any, node: any) {
    const raw: string | undefined = this.options?.meta?.__raw;
    if (!raw) return;
    const words = Array.from(
      raw.matchAll(/word:([\w$.-]+)/g),
      (m: RegExpMatchArray) => m[1],
    );
    if (words.length === 0) return;
    const child = node.children?.[0];
    if (child?.type !== "text") return;
    if (!words.includes(child.value.trim())) return;
    this.addClassToHast(node, "code-word");
  },
};

export default defineShikiSetup(() => {
  return {
    themes: {
      dark: "houston",
      // colorSchema: light のデッキ（slides-compiler-rs.md）向け。
      // 既存デッキは colorSchema: dark のため houston のまま。
      light: "github-light",
    },
    transformers: [wordHighlight],
  };
});
