<script setup lang="ts">
import { computed } from "vue";
import { useSlideContext } from "@slidev/client";

/*
 * 第2章の紙芝居用の流れ図。
 *
 * Overview.vue と同じで、座標はスライドの内部座標の px と 1:1。
 * svg を width=868px（= 980 - px-14*2）で等倍に描くので、ここで書いた
 * font-size がそのまま px で出る。最小フォント 20px を図の中でも守るための作り。
 *
 * 列（cols）を左から並べ、列の中では縦に積む。x は列番号から、y は列の中で
 * 上下中央に揃えて自動で決める。エッジは id の組で指定する。
 */

type Tone = "gray" | "purple" | "yellow" | "blue" | "red";

type FlowNode = {
  id: string;
  /** "\n" で箱の中だけ改行する */
  label: string;
  tone?: Tone;
  /** 箱の中の小さな補足 */
  note?: string;
  noteTone?: Tone;
  /** 出現するクリック番号。省略すると最初から出る */
  at?: number;
};

type EdgeOpts = {
  at?: number;
  dashed?: boolean;
  label?: string;
  tone?: Tone;
};

type EdgeSpec = [string, string] | [string, string, EdgeOpts];

const props = withDefaults(
  defineProps<{
    cols: FlowNode[][];
    edges?: EdgeSpec[];
    /** svg の高さ。省略すると内容から決める */
    h?: number;
  }>(),
  { edges: () => [] },
);

const { $clicks } = useSlideContext();

/* 白地で 4.5:1 を満たす値。references/constraints.md を参照 */
const TONES: Record<Tone, string> = {
  gray: "#717781",
  purple: "#7611A6",
  yellow: "#A36B09",
  blue: "#0B7BC1",
  red: "#B42318",
};

const W = 868;
const COL_GAP = 38;
const ROW_GAP = 24;
const NH = 58; // 箱の高さの下限
const LINE_H = 26; // ラベル1行ぶん（22px × line-height 1.18）
const NOTE_H = 24; // note 1行ぶん（20px × 1.15 + 余白）
const BOX_PAD = 20; // 箱の上下の余白
const PAD_T = 14;
const PAD_B = 14;
const GAP = 9; // 矢印の先端と箱の間
/** 後ろ向きの矢印を回す帯。ラベルぶんを含む */
const BACK_H = 84;

type Placed = FlowNode & { col: number; x: number; y: number; w: number; h: number };

const colWidth = computed(
  () => (W - COL_GAP * (props.cols.length - 1)) / props.cols.length,
);

/*
 * 箱の高さは全ノードで揃える。いちばん背の高い中身に合わせておかないと、
 * ラベルが2行でさらに note の付くノードだけ字が枠からはみ出す。
 * note は1行に収まる長さで書く前提。
 */
const allNodes = computed(() => props.cols.flat());
const nodeH = computed(() =>
  Math.max(
    NH,
    ...allNodes.value.map(
      (n) => n.label.split("\n").length * LINE_H + (n.note ? NOTE_H : 0) + BOX_PAD,
    ),
  ),
);

const heightOf = (_n: FlowNode) => nodeH.value;

/** 列ごとの高さの最大値。これが図の本体の高さになる */
const contentH = computed(() =>
  Math.max(
    ...props.cols.map((col) =>
      col.reduce((sum, n) => sum + heightOf(n), 0) + ROW_GAP * (col.length - 1),
    ),
  ),
);

const hasBack = computed(() =>
  props.edges.some(([from, to]) => colOf(to) < colOf(from)),
);

const svgH = computed(
  () =>
    props.h ??
    PAD_T + contentH.value + PAD_B + (hasBack.value ? BACK_H : 0),
);

const centerY = computed(() => PAD_T + contentH.value / 2);

function colOf(id: string): number {
  return props.cols.findIndex((col) => col.some((n) => n.id === id));
}

const placed = computed<Placed[]>(() => {
  const out: Placed[] = [];
  props.cols.forEach((col, ci) => {
    const total =
      col.reduce((sum, n) => sum + heightOf(n), 0) + ROW_GAP * (col.length - 1);
    let y = centerY.value - total / 2;
    for (const n of col) {
      const h = heightOf(n);
      out.push({
        ...n,
        col: ci,
        x: ci * (colWidth.value + COL_GAP),
        y,
        w: colWidth.value,
        h,
      });
      y += h + ROW_GAP;
    }
  });
  return out;
});

const byId = computed(() => new Map(placed.value.map((n) => [n.id, n])));

const cx = (n: Placed) => n.x + n.w / 2;
const cy = (n: Placed) => n.y + n.h / 2;
const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));

const backY = computed(() => PAD_T + contentH.value + 32);

type Edge = {
  key: string;
  d: string;
  at: number;
  dashed: boolean;
  tone: Tone;
  label?: string;
  lx: number;
  ly: number;
};

const drawnEdges = computed<Edge[]>(() => {
  const out: Edge[] = [];
  props.edges.forEach(([from, to, opts], i) => {
    const a = byId.value.get(from);
    const b = byId.value.get(to);
    if (!a || !b) return;
    const o = opts ?? {};
    const back = b.col < a.col;
    // 矢印は行き先の色を引き継ぐ。同じ要素が枚をまたいで同じ色で出るようにする
    const tone = o.tone ?? b.tone ?? "gray";

    let d: string;
    let lx: number;
    let ly: number;
    if (back) {
      // 前向きの矢印と重ねないよう、箱の列の下側を回して戻す
      const sx = cx(a);
      const sy = a.y + a.h;
      const ex = cx(b);
      const ey = b.y + b.h + GAP;
      d = `M${sx},${sy} C${sx},${backY.value} ${ex},${backY.value} ${ex},${ey}`;
      lx = (sx + ex) / 2;
      ly = backY.value + 24;
    } else {
      const sx = a.x + a.w;
      const ex = b.x - GAP;
      const dy = cy(b) - cy(a);
      const sy = cy(a) + clamp(dy, -a.h * 0.3, a.h * 0.3);
      const ey = cy(b);
      if (Math.abs(dy) < 1) {
        d = `M${sx},${sy} L${ex},${ey}`;
      } else {
        const mid = sx + (ex - sx) * 0.55;
        d = `M${sx},${sy} C${mid},${sy} ${mid},${ey} ${ex},${ey}`;
      }
      lx = (sx + ex) / 2;
      ly = Math.min(sy, ey) - 10;
    }

    out.push({
      key: `${from}->${to}-${i}`,
      d,
      at: o.at ?? 0,
      dashed: !!o.dashed,
      tone,
      label: o.label,
      lx,
      ly,
    });
  });
  return out;
});

const shown = (at?: number) => $clicks.value >= (at ?? 0);

/** ラベルの "\n" は箱の中だけで改行として扱う */
const labelLines = (label: string) => label.split("\n");

const toneOf = (t?: Tone) => TONES[t ?? "gray"];
/* 箱の地。枠と同じ色を薄く敷いて、色だけでなく面でも役割を区別する */
const tintOf = (t?: Tone) => `${toneOf(t)}14`;
</script>

<template>
  <div class="flow">
    <svg
      :viewBox="`0 0 ${W} ${svgH}`"
      class="flow-svg"
      :style="{ width: `${W}px`, height: `${svgH}px` }"
    >
      <defs>
        <marker
          v-for="(color, key) in TONES"
          :id="`flow-arrow-${key}`"
          :key="key"
          viewBox="0 0 10 10"
          refX="9"
          refY="5"
          markerUnits="userSpaceOnUse"
          markerWidth="11"
          markerHeight="11"
          orient="auto"
        >
          <path d="M0,0 L10,5 L0,10 z" :fill="color" />
        </marker>
      </defs>

      <g
        v-for="e in drawnEdges"
        :key="e.key"
        class="flow-edge"
        :class="{ 'is-hidden': !shown(e.at), 'is-dashed': e.dashed }"
      >
        <path
          :d="e.d"
          :stroke="toneOf(e.tone)"
          :marker-end="`url(#flow-arrow-${e.tone})`"
        />
        <text
          v-if="e.label"
          class="flow-edge-label"
          :x="e.lx"
          :y="e.ly"
          :fill="toneOf(e.tone)"
          text-anchor="middle"
        >
          {{ e.label }}
        </text>
      </g>

      <g
        v-for="n in placed"
        :key="n.id"
        class="flow-node"
        :class="{ 'is-hidden': !shown(n.at) }"
      >
        <rect
          :x="n.x"
          :y="n.y"
          :width="n.w"
          :height="n.h"
          rx="10"
          :fill="tintOf(n.tone)"
          :stroke="toneOf(n.tone)"
        />
        <foreignObject :x="n.x" :y="n.y" :width="n.w" :height="n.h">
          <div xmlns="http://www.w3.org/1999/xhtml" class="flow-box">
            <div class="flow-label" :style="{ color: toneOf(n.tone) }">
              <template v-for="(line, i) in labelLines(n.label)" :key="i">
                <br v-if="i" />{{ line }}
              </template>
            </div>
            <div
              v-if="n.note"
              class="flow-note"
              :style="{ color: toneOf(n.noteTone ?? 'gray') }"
            >
              {{ n.note }}
            </div>
          </div>
        </foreignObject>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.flow {
  width: 868px;
  max-width: 100%;
  align-self: stretch;
  display: flex;
  justify-content: center;
}

.flow-svg {
  flex: none;
}

/*
 * 出し入れで位置が動くと「同じ要素は同じ位置」を破るので、
 * 隠すときも描画したまま不透明度だけを落とす。
 */
.flow-node,
.flow-edge {
  transition: opacity 0.3s ease;
}

.flow-node.is-hidden,
.flow-edge.is-hidden {
  opacity: 0;
}

.flow-node rect {
  stroke-width: 2;
}

.flow-edge path {
  fill: none;
  stroke-width: 2.5;
}

.flow-edge.is-dashed path {
  stroke-dasharray: 7 6;
}

.flow-edge-label {
  font-family: var(--font-body);
  font-size: 20px;
}

.flow-box {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 0 8px;
  font-family: var(--font-body);
}

.flow-label {
  font-size: 22px;
  font-weight: 600;
  line-height: 1.18;
}

.flow-note {
  font-size: 20px;
  line-height: 1.15;
  margin-top: 4px;
}
</style>
