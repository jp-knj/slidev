---
theme: seriph
title: Astroの現在地と、Astro Japanが目指す多島海
author: jp-knj
duration: 30min
mdc: true
class: text-left
info: |
  30分で「Astroの事実・技術・コミュニティ」を一本の線にまとめる基調講演。
  各トピックに適用し、デモと行動指針まで落とし込みます。
---

## Astroの現在地と、
## Astro Japan Communityが
## 目指す多島海

---
layout: center
class: text-center
---

## Astroは“速い”だけの話じゃなくなった

- Server-first × Content-driven × Islands が同居する珍しいフレームワーク
- どの部分を動的にするかという設計の自由度が議論の主戦場に
- コミュニティも“中央集権”から“多島海”モデルへ

---

## 今日の地図
1. Astroの現在地
2. 何が変わったか
3. v6以降で観測するポイント
4. Astro Japan Communityとしての行動指針

---
layout: cover
class: text-center
---

## Astroの「今」

---

## Astroの定義を更新する
- **Claim**: Astro = コンテンツ駆動サイトのための Server-First フレームワーク
- **Evidence**: 公式も「Server-first / Content-driven / Island-driven」を併記
- **So what**: SSG vs SPAではなく、コンテンツとインタラクションの配分設計

---

## Astroの「今」を3つだけ

- GitHub Stars: 約54.9k（2025-12-14時点の定点観測）
- State of JS 2025
- Astro was one of the fastest growing languages on
- https://x.com/astrodotbuild/status/1983930731144343934

---

## だから議論の主戦場が変わった

- **Claim**: 速さの勝負ではなく「どの部分を動的にするか」「どのようにコンテンツを扱うか」
- **Evidence**: Astro 5.16で　Content Layer / Server-first / Islandsが統合テーマ化

- SSG → Content driven
 - Server Islands
 - Vite Enviroment

---
layout: cover
class: text-center
---

# Part 2
## コンテンツ駆動を支える技術の3本柱

---

## 1) Content Layer / Live Collections
- **Claim**: コンテンツの扱いが「ファイル」→「層（Layer）」へ
- **Evidence**: Live Content Collectionsで、実行時もASTレベルで型安全な参照ができます。
- **So what**: 更新・検証・統合まで含めてコンテンツ運用をAstro側で引き受ける

---

## 2) Islands → Server Islands

- **Claim**: 動的UIは必要な島だけを立てればいい
- **Evidence**: server:defer（Server Islands）がSSRレスポンスから部分的に遅延レンダリングを許容
- **So what**: 「速さを崩さずに動的要件を足す」ための現実解が日本の案件にも刺さる

---

## 3) Full-stack DX

- **Claim**: Astroは“薄い”まま、必要な分だけアプリ的振る舞いを足せる
- **Evidence**: Actions（型安全なバックエンド関数）、astro:env（厳格な環境変数）、Sessions API（5.7+）
- **So what**: BFF・フォーム・認証を「MPAの良さ」を保ちながら実装できる

---
layout: cover
class: text-center
---

# Part 3
## v6以降：確定と期待を切り分ける

---

## v6はいまα段階
- **Claim**: Astro v6.0.0-alpha.1（2025-12-12）が公開済み
- **Evidence**: 破壊的変更と足場固め（Adapters / Vite 6 / Node 22）に着手
- **So what**: 「確定情報 = αで触れる範囲」「期待値 = APIやルーティングの議論」を切り分けて語る

---
layout: cover
class: text-center
---

## Astro Japanの行動指針 = 「島」として集まる

---

## 「自分のために」作る

- **Claim**: コミュニティへの貢献だなんて思わなくていい。
- **Evidence**: ブログを書く。翻訳する。ツールを作る。これらはすべて「自分の実績（ポートフォリオ）」です。
- **So what**: みんなが自分のために何かを持ってくる。結果として、ここ（コミュニティ）に情報が集まる。それで十分です。

---

## バラバラのままでいる。でも共にいることができる。

- 会社とコミュニティは違う。組織は「共通のゴール」が必要ですが、私たちは違います。
- 目的は人それぞれ。「ブログを作りたい」「転職したい」「ただ流行りを追いたい」。
- 無理に合わせない。全員で同じ方向を向く必要はありません。バラバラな目的を持った人たちが、同じ場所にいる。その「ゆるさ」こそが、長く続く秘訣です。

---

## 点と点を線にする

- 巨大な本部を作るのではなく、横のつながりを増やす。
- 誰かの記事を紹介する。一緒にコードを書く。
- 中央がなくなっても、誰かと誰かが繋がっていれば、このコミュニティは止まりません。

---

## 私たちが目指す多島海

- 全員一致は不要。大事なのは「互いの島が見えている」状態。同意を得なくても、一緒にいることができる。
- 技術・思想・コミュニティの話題で繋がっている
- Astroは島を増やしやすい設計なので、国内でも“分散した航路”を標準化できる

---

1. 1つ作る — 自分のために記事やコードを書く
2. 違いを知る — 自分と違う使い方も「それもアリ」と面白がる
3. 繋がる — 今日の感想を、誰かに伝える

---
layout: center
class: text-center
---

# 多島海で会いましょう
### Questions / Feedback / Demo follow-up

---
