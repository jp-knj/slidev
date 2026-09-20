#!/usr/bin/env bash
# スライドの下端からはみ出している枚を機械検出する。
#
#   bash check-overflow.sh <deck>.md [range]
#   例: bash check-overflow.sh slides.md "7,26,35"
#
# 全枚を PNG に出し、各画像の下端 8px を切り出して、ファイルサイズで判定する。
# 背景だけの帯は全枚で同じサイズに圧縮されるので、その最頻値を基準にし、
# それを超えた枚＝下端に何か描かれている＝はみ出し、とみなす。
#
# 目視より速く、枚数が増えても一定時間で終わる。
# ただし検出できるのは「下端の突き抜け」だけ。横方向の食い込みや、
# アイコンが潰れている・字が小さすぎる、は PNG を開いて見ないと分からない。
#
# 依存: macOS の sips
set -euo pipefail

DECK="${1:?使い方: bash check-overflow.sh <deck>.md [range]}"
RANGE="${2:-}"
OUT=$(mktemp -d)
CROP=$(mktemp -d)
trap 'rm -rf "$OUT" "$CROP"' EXIT

echo "==> export: $DECK ${RANGE:+(range: $RANGE)}"
if [ -n "$RANGE" ]; then
  npx slidev export "$DECK" --format png --range "$RANGE" --output "$OUT" >/dev/null
else
  npx slidev export "$DECK" --format png --output "$OUT" >/dev/null
fi

shopt -s nullglob
pngs=("$OUT"/*.png)
if [ ${#pngs[@]} -eq 0 ]; then
  echo "PNG が出力されませんでした" >&2
  exit 1
fi

H=$(sips -g pixelHeight "${pngs[0]}" | awk '/pixelHeight/{print $2}')
W=$(sips -g pixelWidth  "${pngs[0]}" | awk '/pixelWidth/{print $2}')

# 帯を取る位置。下端ぴったりではなく、そこから約3%上を見る。
# - 最下部には export が付ける外周の余白があり、そこは全枚同じで何も写らない
# - Ref.vue の脚注は bottom:1.5rem（内部座標24px ≒ 画像48px）に居るので、
#   それより下を見ないと脚注のある枚が全部ひっかかる
# 1104px の出力で offset 1072（= 下から32px）になる。
OFFSET=$(( H - (H * 29 / 1000) ))

for f in "${pngs[@]}"; do
  sips -c 8 "$W" --cropOffset "$OFFSET" 0 "$f" --out "$CROP/$(basename "$f")" >/dev/null 2>&1
done

# 背景だけの帯のサイズ（最頻値）を基準にする
BASE=$(for f in "$CROP"/*.png; do stat -f%z "$f"; done | sort -n | uniq -c | sort -rn | head -1 | awk '{print $2}')

echo "==> ${#pngs[@]}枚を検査（y=${OFFSET} から8px / 基準 ${BASE}B）"
found=0
for f in "$CROP"/*.png; do
  s=$(stat -f%z "$f")
  if [ "$s" -gt "$BASE" ]; then
    echo "  はみ出し: $(basename "$f" .png)枚目  (${s}B)"
    found=$((found + 1))
  fi
done

if [ "$found" -eq 0 ]; then
  echo "==> はみ出しなし"
else
  echo "==> ${found}枚ではみ出しを検出。PNG を開いて原因を確認すること"
  exit 1
fi
