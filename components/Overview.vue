<script setup lang="ts">
import { computed } from "vue";

// foreignObject の中に置くので、相対パスではなく import して解決させる
import gopher from "../images/logos/gopher-classic.png";

const props = withDefaults(
  defineProps<{
    /** 強調するノードid。カンマ区切り。例: "compiler,editor" */
    highlight?: string;
    /** 描画する上位ノード。省略時は全ノード */
    visible?: string;
    /** Astro Compiler の内部に表示する項目。例: "oxc,lightning-css,astro-syntax" */
    subs?: string;
    /** 図の下に添える注釈。キーはノードid、または "compiler->editor" のエッジid */
    annotate?: Record<string, string>;
    /** 各ノードの責務。annotate と同じ凡例に並ぶ */
    roles?: Record<string, string>;
    /** 重ねる契約。"source" | "output" | "ecosystem"（カンマ区切り可） */
    contract?: string;
    /** ノードのラベル差し替え。キーはノードid。"\n" で改行する */
    labels?: Record<string, string>;
    /** ノードのアイコン差し替え。"" でアイコンなし、"go" で Gopher */
    icons?: Record<string, string>;
    /** 箱の中の小さな補足の差し替え。"" で消す */
    subnotes?: Record<string, string>;
    /** 破線で描くエッジid。カンマ区切り */
    dashed?: string;
    /** 矢印の上に置く小さなラベル。キーはエッジid */
    edgeLabels?: Record<string, string>;
  }>(),
  { highlight: "", visible: "", subs: "", contract: "", dashed: "" },
);

/*
 * 座標系はスライド内部座標の px と 1:1。
 * svg を width=868px（= 980 - px-14*2）、height=viewBoxの高さ で描くので
 * 拡大縮小が起きず、ここで書いた font-size がそのまま px として出る。
 * 最小フォントサイズ 20px を図の中でも守るための作り。
 */
const W = 868;

type Rect = { x: number; y: number; w: number; h: number };
type Node = Rect & {
  id: string;
  label: string;
  note?: string;
  icon?: string;
  tab?: boolean;
  stack?: boolean;
};

const SUBS = [
  { id: "html5-parser", label: "HTML5 Parser", h: 34 },
  { id: "go-ast", label: "独自の AST", h: 32 },
  { id: "html-correction", label: "HTML correction", h: 32 },
  { id: "esbuild-css", label: "esbuild（CSS）", h: 34 },
  { id: "oxc", label: "Oxc（Parser と AST）", h: 58 },
  { id: "astro-codegen", label: "Astro Codegen", h: 34 },
  { id: "lightning-css", label: "Lightning CSS", h: 34 },
  { id: "astro-syntax", label: "Astro syntax", h: 34 },
] as const;

const CONTRACTS: Record<
  string,
  { label: string; tone: string; edges: string[]; desc: string }
> = {
  source: {
    label: "Source contract",
    tone: "#0B7BC1",
    edges: ["compiler->editor"],
    desc: "書かれた親子関係と位置情報を保持し、ツールが使える AST を渡す",
  },
  output: {
    label: "Output contract",
    tone: "#A36B09",
    edges: ["compiler->build", "build->browser"],
    desc: "実行や表示につながる成果物を生成し、Source と表示の親子関係を区別する",
  },
  ecosystem: {
    label: "Ecosystem contract",
    tone: "#198755",
    edges: ["mdsource->content", "content->build"],
    desc: "plugin を引き続き利用できるようにし、新しい plugin model への移行方法を用意する",
  },
};

const toList = (s?: string) =>
  (s ?? "")
    .split(",")
    .map((v) => v.trim())
    .filter(Boolean);
const toSet = (s?: string) => new Set(toList(s));

const on = computed(() => toSet(props.highlight));
const dimming = computed(() => on.value.size > 0);
const subIds = computed(() => toSet(props.subs));

/** サブ枠の枚数ぶんだけ Astro Compiler が伸びる */
const SUB_GAP = 8;
const SUB_TOP = 40;
const isComparison = computed(() => subIds.value.has("go-ast") || subIds.value.has("astro-codegen"));
const activeSubs = computed(() => SUBS.filter((s) => subIds.value.has(s.id)).map(s => ({
  ...s,
  label: props.labels?.[s.id] ?? s.label,
  h: isComparison.value && subIds.value.has("go-ast") ? 32 : s.h,
})));
const hasGoSubs = computed(() =>
  subIds.value.has("html5-parser") || subIds.value.has("esbuild-css"),
);
// Give the Gopher icon breathing room inside the compiler group.
const compilerSubTop = computed(() => hasGoSubs.value ? (isComparison.value ? 44 : 56) : SUB_TOP);
const compilerH = computed(() =>
  activeSubs.value.length
    ? compilerSubTop.value
      + activeSubs.value.reduce((height, s) => height + s.h, 0)
      + (activeSubs.value.length - 1) * SUB_GAP
      + 12
    : 54,
);

/** 中心 y を固定したまま高さを決める */
const box = (id: string, x: number, w: number, cy: number, h: number) => ({
  id,
  x,
  w,
  h,
  y: cy - h / 2,
});

const BASE_NODES = computed<Node[]>(() => [
  // source 系はエディタのファイルタブに見えるよう tab: true で上端だけ角丸にする
  { ...box("source", 0, 175, 175, 70), label: ".astro", icon: "astro", tab: true },
  { ...box("mdsource", 0, 175, 320, 70), label: ".md と .mdx", icon: "md", tab: true },
  { ...box("compiler", 215, 250, 175, compilerH.value), label: "Astro Compiler", icon: "compiler" },
  {
    ...box("content", 215, 250, 320, 70),
    label: "Content Processor",
    note: "Markdown と MDX",
  },
  {
    ...box("editor", 490, 378, 35, 70),
    label: "Editor",
    note: "ESLint と LSP と Formatter",
    icon: "editor",
  },
  // ラベルが長いぶん、アイコンは横ではなく上に積んで幅に収める
  { ...box("build", 490, 175, 175, 70), label: "Vite と Rolldown", icon: "vite", stack: true },
  { ...box("browser", 693, 175, 175, 70), label: "Browser", icon: "browser" },
]);

/*
 * ラベルとアイコンはスライド側から差し替えられる。
 * icons に "" を渡すとアイコンを消せるよう、?? で拾ってから空文字を undefined に落とす。
 */
const NODES = computed<Node[]>(() =>
  BASE_NODES.value.map((n) => {
    const icon = props.icons?.[n.id] ?? n.icon;
    const note = props.subnotes?.[n.id] ?? n.note;
    const label = props.labels?.[n.id];
    const noteLines = note?.split("\n").length ?? 0;
    const h = n.id === "build" && noteLines > 1
      ? Math.max(n.h, 56 + noteLines * 24)
      : n.h;
    return {
      ...n,
      h,
      y: n.y - (h - n.h) / 2,
      label: label ?? n.label,
      icon: icon || undefined,
      note: note || undefined,
      // 積み上げは既定の長いラベルのための処理なので、差し替えたら横並びに戻す
      stack: label === undefined ? n.stack : false,
    };
  }),
);

/** ラベルの "\n" は箱の中だけで改行として扱う */
const labelLines = (label: string) => label.split("\n");

const shownNodes = computed(() => {
  const want = toSet(props.visible);
  return NODES.value.filter((n) => want.size === 0 || want.has(n.id));
});
const byId = computed(() => new Map(shownNodes.value.map((n) => [n.id, n])));

const shownSubs = computed(() => {
  const c = byId.value.get("compiler");
  if (!c) return [];
  let y = c.y + compilerSubTop.value;
  return activeSubs.value.map((s) => {
    const rect = { ...s, x: c.x + 14, y, w: c.w - 28 };
    y += s.h + SUB_GAP;
    return rect;
  });
});

/** ノードの矩形から矢印のパスを組み立てる */
const GAP = 9;
const shownEdges = computed(() => {
  const g = byId.value;
  const out: {
    id: string;
    from: string;
    to: string;
    d: string;
    mx: number;
    ty: number;
    by: number;
  }[] = [];
  const push = (id: string, from: string, to: string, d: string) => {
    const a = g.get(from);
    const b = g.get(to);
    if (!a || !b) return;
    // ラベルと境界線の位置。x は向かい合う辺の中間、y は2つの箱の上端と下端
    out.push({
      id,
      from,
      to,
      d,
      mx: (a.x + a.w + b.x) / 2,
      ty: Math.min(a.y, b.y),
      by: Math.max(a.y + a.h, b.y + b.h),
    });
  };
  const cx = (n: Node) => n.x + n.w / 2;
  const cy = (n: Node) => n.y + n.h / 2;

  const straight = (a: Node, b: Node) => `M${a.x + a.w},${cy(a)} L${b.x - GAP},${cy(b)}`;
  const branch = (a: Node, b: Node, off: number) => {
    const sx = a.x + a.w;
    const sy = cy(a) + off;
    const ex = b.x - GAP;
    const ey = cy(b);
    const mid = sx + (ex - sx) * 0.55;
    return `M${sx},${sy} C${mid},${sy} ${mid},${ey} ${ex},${ey}`;
  };

  const s = g.get("source");
  const c = g.get("compiler");
  const e = g.get("editor");
  const b = g.get("build");
  const br = g.get("browser");
  const md = g.get("mdsource");
  const ct = g.get("content");

  if (s && c) push("source->compiler", "source", "compiler", straight(s, c));
  if (md && ct) push("mdsource->content", "mdsource", "content", straight(md, ct));
  if (c && e) {
    // Leave the Go group from its top to keep the WASM label clear.
    const path = hasGoSubs.value
      ? `M${cx(c)},${c.y} C${cx(c)},${cy(e)} ${e.x - GAP - 36},${cy(e)} ${e.x - GAP},${cy(e)}`
      : branch(c, e, -c.h * 0.26);
    push("compiler->editor", "compiler", "editor", path);
  }
  // Editor へ分岐しないなら、下へ振らずまっすぐ引く
  if (c && b)
    push("compiler->build", "compiler", "build", e ? branch(c, b, c.h * 0.26) : straight(c, b));
  if (b && br) push("build->browser", "build", "browser", straight(b, br));
  if (ct && b) {
    const sx = ct.x + ct.w;
    const sy = cy(ct);
    const ex = cx(b);
    const ey = b.y + b.h + GAP;
    push(
      "content->build",
      "content",
      "build",
      `M${sx},${sy} C${ex - 50},${sy} ${ex},${sy} ${ex},${ey}`,
    );
  }
  return out;
});

const dashedEdges = computed(() => toSet(props.dashed));

const edgeLabelOf = (id: string) => props.edgeLabels?.[id];

/** 破線のエッジは「またぐ境界」として、矢印の上に縦の破線も引く */
const isBoundary = (id: string) => dashedEdges.value.has(id);

const activeContracts = computed(() =>
  toList(props.contract)
    .map((k) => CONTRACTS[k])
    .filter(Boolean),
);

const contractOf = (edgeId: string) =>
  activeContracts.value.find((c) => c.edges.includes(edgeId));

const edgeState = (id: string, from: string, to: string) => {
  if (contractOf(id)) return "is-contract";
  if (activeContracts.value.length) return "is-off";
  if (!dimming.value) return "is-base";
  if (on.value.has(id) || (on.value.has(from) && on.value.has(to))) return "is-on";
  return "is-off";
};

const stateOf = (id: string) =>
  !dimming.value ? "is-base" : on.value.has(id) ? "is-on" : "is-off";

/** サブ枠は、明示指定がなければ Astro Compiler の状態を引き継ぐ */
const subState = (id: string) =>
  dimming.value && on.value.has(id) ? "is-on" : stateOf("compiler");

const MARKERS: Record<string, string> = {
  "is-base": "ov-arrow",
  "is-off": "ov-arrow",
  "is-on": "ov-arrow-on",
};
const markerFor = (id: string, state: string) => {
  const c = contractOf(id);
  if (c) return `ov-arrow-${c.label.split(" ")[0].toLowerCase()}`;
  return MARKERS[state] ?? "ov-arrow";
};

const labelOf = (id: string): string => {
  if (id.includes("->")) {
    const [a, b] = id.split("->");
    return `${labelOf(a)} → ${labelOf(b)}`;
  }
  // 箱の中の改行は、凡例では空白に潰す
  return (
    NODES.value.find((n) => n.id === id)?.label ??
    SUBS.find((s) => s.id === id)?.label ??
    id
  ).replace(/\n/g, " ");
};

/*
 * 責務ラベルは箱の中に入れない。
 * 20px を下回らせずに箱へ収めるのは無理があるので、注釈と同じ凡例へ並べる。
 */
const notes = computed(() => {
  const rows = [
    ...Object.entries(props.roles ?? {}),
    ...Object.entries(props.annotate ?? {}),
  ];
  return rows.map(([id, text]) => ({ id, target: labelOf(id), text }));
});

const hasLegend = computed(
  () => activeContracts.value.length > 0 || notes.value.length > 0,
);

/** 表示中のノードを縦方向だけ切り詰める。幅は常に 868 で拡大率 1 を保つ */
const PAD = 12;
const vb = computed(() => {
  const rects = shownNodes.value;
  if (!rects.length) return { y: 0, h: 400 };
  const minY = Math.min(
    ...rects.map((r) => r.y),
    ...shownEdges.value.filter((e) => edgeLabelOf(e.id)).map((e) => e.ty - 34),
  ) - PAD;
  const maxY = Math.max(...rects.map((r) => r.y + r.h)) + PAD;
  return { y: minY, h: maxY - minY };
});
const viewBox = computed(() => `0 ${vb.value.y} ${W} ${vb.value.h}`);
</script>

<template>
  <div class="ov">
    <svg
      :viewBox="viewBox"
      class="ov-svg"
      :style="{ width: `${W}px`, height: `${vb.h}px` }"
    >
      <defs>
        <marker
          v-for="m in [
            { id: 'ov-arrow', fill: '#9A90AC' },
            { id: 'ov-arrow-on', fill: '#BC52EE' },
            { id: 'ov-arrow-source', fill: '#0B7BC1' },
            { id: 'ov-arrow-output', fill: '#A36B09' },
            { id: 'ov-arrow-ecosystem', fill: '#198755' },
          ]"
          :key="m.id"
          :id="m.id"
          viewBox="0 0 10 10"
          refX="9"
          refY="5"
          markerUnits="userSpaceOnUse"
          markerWidth="12"
          markerHeight="12"
          orient="auto"
        >
          <path d="M0,0 L10,5 L0,10 z" :fill="m.fill" />
        </marker>
      </defs>

      <g
        v-for="e in shownEdges"
        :key="e.id"
        class="ov-edge"
        :class="[edgeState(e.id, e.from, e.to), { 'is-dashed': dashedEdges.has(e.id) }]"
      >
        <path
          :d="e.d"
          :stroke="contractOf(e.id)?.tone"
          :marker-end="`url(#${markerFor(e.id, edgeState(e.id, e.from, e.to))})`"
        />
        <line
          v-if="isBoundary(e.id)"
          class="ov-boundary"
          :x1="e.mx"
          :x2="e.mx"
          :y1="e.ty - 6"
          :y2="e.by + 6"
        />
        <text
          v-if="edgeLabelOf(e.id)"
          class="ov-edge-label"
          :x="e.mx"
          :y="e.ty - 14"
          text-anchor="middle"
        >
          {{ edgeLabelOf(e.id) }}
        </text>
      </g>

      <g v-for="n in shownNodes" :key="n.id" class="ov-node" :class="stateOf(n.id)">
        <rect
          v-if="n.id === 'compiler' && (hasGoSubs || isComparison)"
          class="ov-compiler-group"
          :x="n.x"
          :y="n.y"
          :width="n.w"
          :height="n.h"
          rx="12"
        />
        <rect
          v-if="n.tab"
          class="ov-tab-bar"
          :x="n.x + 12"
          :y="n.y + n.h - 3"
          :width="n.w - 24"
          height="3"
          rx="1.5"
        />
        <foreignObject
          :x="n.x"
          :y="n.y"
          :width="n.w"
          :height="n.id === 'compiler' && shownSubs.length ? compilerSubTop : n.h"
        >
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            class="ov-box"
            :class="{ 'ov-box-top': n.id === 'compiler' && shownSubs.length }"
          >
            <div class="ov-head" :class="{ 'ov-head-stack': n.stack }">
              <logos-astro-icon v-if="n.icon === 'astro'" class="ov-ico" />
              <logos-markdown v-else-if="n.icon === 'md'" class="ov-ico" />
              <logos-vitejs v-else-if="n.icon === 'vite'" class="ov-ico" />
              <logos-svelte-icon v-else-if="n.icon === 'svelte'" class="ov-ico" />
              <logos-snowpack v-else-if="n.icon === 'snowpack'" class="ov-ico" />
              <logos-visual-studio-code v-else-if="n.icon === 'editor'" class="ov-ico" />
              <carbon-code v-else-if="n.icon === 'compiler'" class="ov-ico ov-ico-mono" />
              <carbon-application-web v-else-if="n.icon === 'browser'" class="ov-ico ov-ico-mono" />
              <img v-else-if="n.icon === 'go'" :src="gopher" alt="" class="ov-ico ov-ico-go" />
              <div class="ov-label">
                <template v-for="(line, i) in labelLines(n.label)" :key="i">
                  <br v-if="i" />{{ line }}
                </template>
              </div>
            </div>
            <div v-if="n.note" class="ov-note">
              <template v-for="(line, i) in labelLines(n.note)" :key="i">
                <br v-if="i" />{{ line }}
              </template>
            </div>
          </div>
        </foreignObject>
      </g>

      <g v-for="s in shownSubs" :key="s.id" class="ov-sub" :class="subState(s.id)">
        <rect :x="s.x" :y="s.y" :width="s.w" :height="s.h" rx="8" />
        <foreignObject :x="s.x" :y="s.y" :width="s.w" :height="s.h">
          <div xmlns="http://www.w3.org/1999/xhtml" class="ov-box">
            <div class="ov-sublabel">{{ s.label }}</div>
          </div>
        </foreignObject>
      </g>
    </svg>

    <div v-if="hasLegend" class="ov-legend">
      <div v-for="c in activeContracts" :key="c.label" class="ov-legend-row">
        <span class="ov-swatch" :style="{ backgroundColor: c.tone }" />
        <span class="ov-legend-name" :style="{ color: c.tone }">{{ c.label }}</span>
        <span class="ov-legend-desc">{{ c.desc }}</span>
      </div>
      <div v-for="n in notes" :key="n.id" class="ov-legend-row">
        <span class="ov-legend-name">{{ n.target }}</span>
        <span class="ov-legend-desc">{{ n.text }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ov {
  width: 868px;
  max-width: 100%;
  align-self: stretch;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.ov-svg {
  flex: none;
}

/* The Go compiler frame groups its internal dependencies. */
.ov-compiler-group {
  fill: #fff;
  stroke: #d9d0e4;
  stroke-width: 1.2;
}

.ov-node.is-off,
.ov-edge.is-off,
.ov-sub.is-off {
  opacity: 0.32;
}

.ov-sub rect {
  fill: #f2eff8;
  stroke: #e0d9ea;
  stroke-width: 1.2;
}

.ov-sub.is-on rect {
  fill: rgba(188, 82, 238, 0.12);
  stroke: #bc52ee;
  stroke-width: 2;
}

.ov-edge path {
  fill: none;
  stroke: #9a90ab;
  stroke-width: 2;
}

.ov-edge.is-on path {
  stroke: #bc52ee;
  stroke-width: 3;
}

.ov-edge.is-contract path {
  stroke-width: 3.5;
}

/* 言語やランタイムの境界をまたぐ矢印 */
.ov-edge.is-dashed path {
  stroke-dasharray: 7 6;
}

.ov-edge-label {
  font-family: var(--font-body);
  font-size: 20px;
  fill: #7611a6;
}

.ov-boundary {
  stroke: #bc52ee;
  stroke-width: 2;
  stroke-dasharray: 6 6;
}

.ov-edge.is-off .ov-edge-label {
  fill: #9a90ab;
}

.ov-box {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 0 10px;
  color: var(--astro-body, #1f2328);
  font-family: var(--font-body);
}

.ov-box-top {
  justify-content: center;
}

.ov-head {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

/* 横並びだと 175px の枠に収まらないラベル用。アイコンを上に積んで 20px で置く */
.ov-head-stack {
  flex-direction: column;
  gap: 3px;
}

.ov-head-stack .ov-label {
  font-size: 20px;
  /* 空白を含む Vite と Rolldown を1行で表示し、図の高さに収める。 */
  white-space: nowrap;
}

/* アイコンは width/height を両方指定する（1em のままだと幅で頭打ちになる） */
.ov-ico {
  width: 26px;
  height: 26px;
  flex: none;
}

.ov-ico-mono {
  color: var(--astro-body, #6b7280);
}

/* Gopher は余白のない縦長の png。width を当てると潰れるので height だけにする */
.ov-ico-go {
  width: auto;
  height: 40px;
}

/* エディタのアクティブタブ風に、下辺をアクセント色で締める */
.ov-node .ov-tab-bar {
  fill: #bc52ee;
  stroke: none;
}

.ov-node.is-off .ov-tab-bar {
  fill: #9a90ab;
}

.ov-label {
  font-size: 24px;
  font-weight: 600;
  line-height: 1.2;
  color: var(--astro-body, #1f2328);
}

.is-on .ov-label {
  color: #7611a6;
  font-weight: 700;
}

.is-on .ov-note {
  color: #7611a6;
}

.ov-sublabel {
  font-size: 20px;
  line-height: 1.2;
  color: var(--astro-body, #3a3f47);
}

.ov-note {
  font-size: 20px;
  line-height: 1.2;
  margin-top: 3px;
  color: var(--astro-body, #6b7280);
}

.ov-legend {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  align-items: start;
  width: 100%;
}

.ov-legend-row {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  font-size: 20px;
  line-height: 1.4;
}

.ov-swatch {
  width: 0.65rem;
  height: 0.65rem;
  border-radius: 999px;
  flex: none;
  align-self: center;
}

.ov-legend-name {
  color: #7611a6;
  white-space: nowrap;
}

.ov-legend-desc {
  color: var(--astro-body, #1f2328);
}
</style>
