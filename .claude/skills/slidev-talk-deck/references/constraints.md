# Slidev の制約（実測）

すべて実際に動かして確かめた値。**推測で書き換えない。** 迷ったら再測定する。

## 座標系 — `vh` は使えない

Slidev は **980×551 の内部座標**でレイアウトしてから、`transform: scale()` で画面サイズへ拡大する。

| 項目 | 値 | 根拠 |
|---|---|---|
| キャンバス幅 | 980px | `@slidev/parser` の `canvasWidth` 既定 |
| アスペクト比 | 16/9 → 高さ 551px | 同 `aspectRatio` 既定 |
| 本文に使える幅 | **868px**（`px-14` = 56px を左右で引く） | テーマの `.slidev-layout` |
| 本文に使える高さ | **約471px**（`py-10` = 40px を上下で引く） | 同上 |

`vh` はビューポート基準なので、この拡大と噛み合わない。
`max-height: 50vh` を指定した図がはみ出したのはこれが原因だった。

**px で書く。** ここでの 1px は「1920幅で投影したときの約2px」に相当する。

## アイコン — `h-*` だけでは大きくならない

unplugin-icons が出す SVG は `<svg width="1em" height="1em" viewBox="...">`。
CSS の `height` は **height 属性しか上書きしない**。`width` が `1em`（≒本文フォントサイズ）のまま残り、
`preserveAspectRatio="xMidYMid meet"` で絵は幅に頭打ちされる。**箱だけが縦に伸びる。**

`h-32`（128px）にしても絵の大きさが変わらず、列のレイアウトだけ下にずれたことで確定した。

| アイコンの形 | 指定 | 理由 |
|---|---|---|
| 正方形に近いシンボル（vitejs / astro-icon / eslint） | `text-*` | font-size が 1em の幅・高さを同時に動かす |
| 横長のワードマーク（swc / biomejs / oxc / rolldown） | `w-* h-*` の**両方** | 幅の箱に meet で収める。`text-*` だと幅が伸びて隣の列へ食い込む |
| `<img>` のロゴ | `h-*` だけでよい | width 属性の競合がないので固有比が効く |

多くのロゴには**シンボルのみの別名**がある（`logos:oxc-icon` / `logos:biomejs-icon` /
`logos:astro-icon` / `logos:parcel-icon` / `logos:rome-icon` / `logos:rolldown-icon`）。
ワードマークが邪魔なときはそちらを探す。

コレクションは**明示的にインストール**する。Slidev の `createIconsPlugin` は `autoInstall` していない。

## コードブロック — CSS変数を上書きする

`@slidev/client/styles/code.css` が `.slidev-code` に `!important` で当てている。
`font-size` を直接書いても効かない。既定値は `@slidev/client/styles/vars.css`:

```
--slidev-code-font-size: 12px;
--slidev-code-line-height: 18px;
--slidev-code-padding: 8px;
--slidev-code-margin: 4px 0;
```

**全体の既定を変える**なら `:root` で変数を上書きする。
**スライド単位で変える**なら `.slidev-layout.<class> .slidev-code` の詳細度で `!important` を上回る。

## スライド単位のクラスは frontmatter の `class:`

ラッパー `<div class="xxx">` でコードブロックを囲んでも、そのクラスは届かない。
frontmatter の `class:` は `.slidev-layout` に付くので、こちらを使う。

```md
---
layout: default
class: code-compact
---
```

## レイアウトの落とし穴

- **`layout: center` は shrink-to-fit。** 中身が `grid place-content-center` に入るため、
  子の `width: 100%` が解決しない。**px で幅を決める**（本文幅なら 868px）
- **grid の子には `min-w-0`。** grid item の既定は `min-width: auto` なので、
  コードブロックが列幅を押し広げてスライドの右端を突き抜ける
- **下端に固定する要素**（脚注など）を `position: absolute; bottom: *` で置くには、
  `.slidev-layout` に `position: relative; min-height: 100%` が要る
- **`li { line-height: 2.2em }`** のようなテーマ既定は高さの罠。
  密度の高い枚では `ul` をやめて `div` を並べるほうが収まる

## 最小フォントサイズ

20px を下限にする場合、UnoCSS の `text-sm`(14) / `text-base`(16) / `text-lg`(18) は下回るので、
テーマ側で床を敷く:

```css
.slidev-layout .text-sm,
.slidev-layout .text-base,
.slidev-layout .text-lg { font-size: 20px; }
```

**床を敷くと既存スライドが縦に伸びてはみ出す。** 敷いた直後に必ず溢れ検出を回す。

## コントラスト（白地のとき）

文字は 4.5:1、図の線など非テキストは 3:1 が目安（WCAG AA）。
プロジェクターは実効コントラストがモニタより落ちるので、4.0 前後の色は会場でさらに弱くなる。

白地で 4.5:1 を満たす下限の例: 灰色文字 `#717781`、青 `#0B7BC1`、橙 `#A36B09`、緑 `#198755`。
淡い色地のバッジは、**地の色も文字色から合成される**なら両方を含めて計算する。

色だけで区別させない（WCAG 1.4.1）。凡例やラベルを必ず添える。

## スライドの数え方 — フェンスの長さを見る

`---` でスライドを分けるとき、**コードフェンスの中の `---` を数えてはいけない**。
`.astro` の Component script はまさに `---` で囲まれている。

さらに厄介なのが `magic-move`。4連バッククォートの中に3連が入る:

````md
`````md magic-move
```astro
---
const products = await getProducts();
---
```
```astro
...
```
`````
````

「``` で始まる行が来たら開閉を反転」という実装だと、内側の ```astro で閉じたと誤判定し、
`.astro` の `---` をスライド区切りとして数えてしまう。**実際に81枚と数えて、export は75枚だった。**

CommonMark どおり、**開いた記号の種類と長さを覚えて、同じ記号・同じ長さ以上・情報文字列なし
の行でだけ閉じる**。`scripts/slide-stats.py` の `split_slides()` がその実装。

数えたら **export した枚数と一致するか必ず突き合わせる。** ずれていたら分割が間違っている。

## はみ出し検出の帯の位置

export した PNG は **1960×1104**（1920×1080 ではない）。周囲に余白が付く。

下端ぴったりを見ると、全枚で同じ余白しか写らず**永久に検出できない**。
逆に下から5%ほど広く取ると、`bottom: 1.5rem` に固定した脚注を拾って**全枚が誤検出**になる。

**下端から約3%上（1104px の出力なら y=1072）の8px帯**が正しい。脚注より下で、余白より上。
`scripts/check-overflow.sh` はこれを画像の高さから計算している。

## 縦の余白をどう配るか

使える高さは約471px しかない。**余白は「余ったもの」ではなく、配るもの**として扱う。

### 上下のパディング

`.slidev-layout` の `py-10`（上下40px）は、上を削るのが効く。
見出しは上端寄りにあるほうが自然で、削った分そのまま本文の高さになる。

```css
@apply px-14 pt-6 pb-10;   /* 上24px / 下40px */
```

下は残す。`Ref` の脚注が `bottom: 1.5rem`（24px）に居るため、詰めすぎると本文と当たる。

**上を削っても何も壊れない。** 内容が上へ動くだけで、下の余裕がその分増える。

### 見出しと本文の距離

本文を上下中央に寄せたいときは、**余りを auto マージンで折半させる**:

```css
.slidev-layout.body-center { display: flex; flex-direction: column; min-height: 100%; }
.slidev-layout.body-center > h2 + *      { margin-top: auto !important; }
.slidev-layout.body-center > :last-child { margin-bottom: auto !important; }
```

見出しの直後に `margin-top: auto`、本文の末尾に `margin-bottom: auto` を置くと、
余った高さが上下で等分される。本文が詰まっていれば auto は 0 になるので、**溢れない**。

`Ref` は `absolute` で行送りに関わらないが `:last-child` には当たる。
末尾が `Ref` のスライドでは、ひとつ手前を本文の末尾として扱う必要がある。

### 詰める順番

スライドが入らないとき、**コードを縮めるのは最後**。読ませたいものから削ることになる。

1. 見出しを1行に収める（2行折り返しは約47px、いちばん効く）
2. 小見出し・キャプションを1行に収める
3. 説明文をノートへ逃がす
4. `mt-8` → `mt-6` のような刻みで詰める
5. それでも入らなければ、コードの行数を減らす（**桁数の上限に注意**）

2カラムでコードを縮めるときは、行数を減らすと1行が長くなりがちで、
今度は**横にはみ出す**。縦と横はトレードオフになる。列幅から桁数の上限を先に出す:

```
桁数 = (列幅 - パディング) / (フォントサイズ × 0.6)
```

21px・列幅422px・パディング36px なら 30桁が上限。
