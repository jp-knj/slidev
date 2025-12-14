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

# Astroの現在地と、
# Astro Japan Communityが目指す多島海
### コンテンツ駆動の“今”から、分散型コミュニティの“次”へ

---
layout: center
class: text-center
---

## 「Astroは“速い”だけの話じゃなくなった」
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
layout: center
class: text-center
---

## server:defer + Actions をまとめて見せる
- View Transitions か Server Islands どちらかを実機確認
- 成功基準: コンテンツ基盤を崩さず、動的要求を足せることを直感で理解してもらう

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

## 何を観測し、どこにフィードバックするか
- Route Groupsなど大規模運用向けの課題はRoadmap Discussionで継続議論中
- α版で見つけたフィードバックはIssueよりもDiscussion/Discordで先に共有すると開発が速い
- Astro Japanは“翻訳屋”ではなく“観測所”として振る舞う

---
layout: cover
class: text-center
---

## Astro Japanの行動指針 = 多島海を育てる

---

## 行動指針 (1) 収穫を奨励 (Harvest)
- **Claim**: 知見を「共有」だけで終わらせず、自分の成果として収穫する
- **Evidence**: 記事・実装メモ・プラグイン・翻訳など、Astroのエコシステム事例が増えている
- **So what**: 「収穫物」を持ってくる人がいるから多島海に新しい島が生まれる

---

## 行動指針 (2) 剪定を祝う (Prune)

- 企業組織は「共通のゴール」に向かって進む必要がありますが、コミュニティはそうではありません。

- コミュニティの中でどう立ち回るか、どう評価されるか。
- 我々はバラバラの方向を向いたまま、共にいることができる。
- 全員の意見を一致させる必要はない。異なる意見のクラスターが可視化され、互いの存在を認知している状態こそが健全です。

Astroを使う理由は「ブログを作りたい」「転職したい」「ただ流行りを追いたい」とバラバラでいい。その目的の不一致こそが、コミュニティの強靭さを生みます。単一障害点（共通のゴール）がないからです。

---

## Connect
- **Claim**: Astro Japanは巨大な本島ではなく、島同士の航路を増やす
- **Evidence**: コラボ記事、相互レビュー、登壇リレーなど“小さな航路”がコミュニティを太くする
- **So what**: 1つの中心に依存せず、分散した島々が互いに見える状態を維持できる

---

## 私たちが目指す多島海
- 全員一致は不要。大事なのは「互いの島が見えている」状態
- 技術・思想・コミュニティの話題で繋がっている
- Astroは島を増やしやすい設計なので、国内でも“分散した航路”を標準化できる

---

1. **1つ作る** — 記事 / コード / プラグイン / 翻訳
2. **1つ剪定する** — 古いページに日付や注釈を追加
3. **1つ繋ぐ** — 誰かと共同でアウトプット or 次の登壇者を紹介

---
layout: center
class: text-center
---

# 多島海で会いましょう
### Questions / Feedback / Demo follow-up
