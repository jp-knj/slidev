# この repo の構成

1つの Slidev プロジェクトに**複数のデッキが同居**している。共有物と専用物の線引きを間違えない。

## デッキ

| ファイル | テーマ | 用途 |
|---|---|---|
| `slides.md` | `./theme`（ダーク） | Astroの現在地 / 30分 |
| `slides-v1.md` | `./theme`（ダーク） | Astro Meetup v1 オープニング |
| `slides-compiler-rs.md` | `./theme-light`（白） | Go→Rust コンパイラの講演 |

`package.json` の素の `dev` / `build` / `export` は引数なし＝**`slides.md` 固定**。
`slides-compiler-rs.md` を見たいときは `dev:compiler` を使う。

## 触ってよいもの・いけないもの

| | 扱い |
|---|---|
| `theme/` | **編集しない。** ダークの共有テーマで、`slides.md` と `slides-v1.md` が使っている |
| `theme-light/` | `slides-compiler-rs.md` 専用。`theme/` を vendor コピーして白地に書き換えたもの。自由に触ってよい |
| `package.json` | **全デッキ共有。追加のみ。** 既存 script と依存は変えない |
| `setup/shiki.ts` | **全デッキ共有。** `themes.light` を足しても、既存デッキは `colorSchema: dark` なので影響しない |
| `components/` | 全デッキから見える。新規追加は安全 |
| `images/` | 共有。ロゴは `images/logos/` に置く |

共有ファイルを触ったら、**既存デッキのビルドが通るか必ず確認する**:

```bash
npx slidev build            # slides.md
npx slidev build slides-v1.md --out dist/v1
```

## 自作コンポーネント

### `Overview.vue` — 全体図

講演を通して同じ図に戻ってくるための部品。props で見せ方を切り替える。

| prop | 役割 |
|---|---|
| `visible` | 描画するノード（カンマ区切り）。省略で全部 |
| `highlight` | 強調するノード。指定すると他は淡くなる |
| `subs` | Compiler の内側に出すサブ枠（`parser` / `oxc` / `astro-syntax`） |
| `annotate` | 図の下の凡例。キーはノードid、または `"compiler->editor"` のエッジid |
| `roles` | 各ノードの責務。`annotate` と同じ凡例に並ぶ |
| `contract` | 契約の帯（`source` / `output` / `ecosystem`、カンマ区切り可） |

座標はコンポーネント内に固定してあり、**内部座標の px と 1:1**（`W = 868`）。
svg を等倍で描くので、ここで書いた `font-size` がそのまま px で出る。

責務ラベルを箱の中に入れない設計になっている。20px を下回らせずに箱へ収めるのが無理だったため、
凡例へ逃がしている。

### `Ref.vue` — 出典脚注

スライド下端に固定。1枚に1つが前提（複数置くと重なる）。`inline` で流し込みにもできる。

### `Status.vue` — 状態バッジ

`adopted` / `wip` / `proposed` / `poc`。`version` で対象バージョンを添えられる。
提案したことと採用されたことを**混同させない**ために使う。

## ロゴ素材

`images/logos/` に置く。Iconify に無いもの、ワードマークしか無いものはここへ。

| ファイル | 出どころ | ライセンス |
|---|---|---|
| `ferris.svg` | rustacean.net `rustacean-flat-happy.svg` | CC0 |
| `gopher.svg` | MariaLetta/free-gophers-pack `characters/svg/71.svg` | CC0 |

絵文字のアイコンコレクション（`noto` / `twemoji` / `openmoji`）は1アイコンのために 10〜40MB の
依存を増やすことになり、ライセンスも CC-BY や CC BY-SA が混ざる。
**公式のマスコットが CC0 で配られているならそちらを取る。**
