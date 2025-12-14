---
theme: seriph
title: Astroの現在地と、Astro Japanが目指す多島海
author: Astro Japan
duration: 30min
mdc: true
class: text-left
info: |
  30分で「Astroの事実・技術・コミュニティ」を一本の線にまとめる基調講演。
  型 = Claim / Evidence / So what を各トピックに適用し、デモと行動指針まで落とし込みます。
---

# Astroの現在地と、Astro Japanが目指す多島海
### コンテンツ駆動の“今”から、分散型コミュニティの“次”へ
- Hook: Astroは“速いSSG”の話では終わらない
- 30 min / 18-22 slides / Claim→Evidence→So what の反復

<!-- Opening note -->
<!-- 今回のキーメッセージと、聴衆に期待すること（アップデートを持ち帰り、行動する）を先に言う -->

---
layout: center
class: text-center
---

# Hook
## 「Astroは“速い”だけの話じゃなくなった」
- Server-first × Content-driven × Islands が同居する珍しいフレームワーク
- 「どの部分を動的にするか？」という設計の自由度が議論の主戦場に
- コミュニティも“中央集権”から“多島海”モデルへ

<!-- 強調: 速さから「動的要件をどこまで許可するか」への議論シフト -->

---

## 今日の地図
1. Astroの現在地（事実）
2. 何が変わったか（技術の3本柱）
3. v6以降で観測するポイント
4. Astro Japanとしての行動指針とCall to Action

---
layout: cover
class: text-center
---

# Part 1
## Astroの「今」

---

## Astroの定義を更新する
- **Claim**: Astro = コンテンツ駆動サイトのための Server-First フレームワーク
- **Evidence**: 公式も「Server-first / Content-driven / Island-driven」を併記
- **So what**: 論点は「SSG vs SPA」ではなく、コンテンツとインタラクションの“配分”設計

---

## Astroの「今」を3つだけ
- GitHub Stars: 約54.9k（2025-12-14時点の定点観測）
- State of JS 2024: Meta-Frameworksカテゴリで「利用者満足度の高さ」が明確に言及
- 現行安定版: Astro 5.16系（最新は5.16.5）でContent LayerやServer Islandsが実戦投入段階

---

## だから議論の主戦場が変わった
- **Claim**: 速さの勝負ではなく「どの部分を動的にするか」「どのようにコンテンツを扱うか」
- **Evidence**: Astro 5.16でContent Layer / server-first / Islandsが統合テーマ化
- **So what**: 「動的条件を足した瞬間に崩れるSSG」論争から解放され、運用・分散チームの会話に移行

---
layout: cover
class: text-center
---

# Part 2
## コンテンツ駆動を支える技術の3本柱

---

## 1) Content Layer / Live Collections
- **Claim**: コンテンツの扱いが「ファイル」から「層（Layer）」へ
- **Evidence**: Live Content Collections（5.10の実験機能）で、実行時もASTレベルで型安全な参照が可能
- **So what**: 更新・検証・統合まで含めてコンテンツ運用をAstro側で引き受ける

---

## 2) Islands → Server Islands
- **Claim**: 動的UIは必要な島だけを立てればいい
- **Evidence**: server:defer（Server Islands）がSSRレスポンスから部分的に遅延レンダリングを許容
- **So what**: 「速さを崩さずに動的要件を足す」ための現実解が日本の案件にも刺さる

---

## 3) Full-stack DX (Actions / Env / Sessions)
- **Claim**: Astroは“薄い”まま、必要な分だけアプリ的振る舞いを足せる
- **Evidence**: Actions（型安全なバックエンド関数）、astro:env（厳格な環境変数）、Sessions API（5.7+）
- **So what**: BFF・フォーム・認証を「MPAの良さ」を保ちながら実装できる

---
layout: center
class: text-center
---

# Demo Slot
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

# Part 4
## Astro Japanの行動指針 = 多島海を育てる

---

## 行動指針 (1) 収穫を奨励 (Harvest)
- **Claim**: 知見を「共有」だけで終わらせず、自分の成果として収穫する
- **Evidence**: 記事・実装メモ・プラグイン・翻訳など、Astroのエコシステム事例が増えている
- **So what**: 「収穫物」を持ってくる人がいるから多島海に新しい島が生まれる

---

## 行動指針 (2) 剪定を祝う (Prune)
- **Claim**: 情報の“死”を恐れず、剪定を祝う
- **Evidence**: 古い資料に日付と注釈を残すと、次のアップデートが追いやすい
- **So what**: 情報の層が見えることで、新規参入者も過去→現在の流れを把握できる

---

## 行動指針 (3) 結節点を作る (Connect)
- **Claim**: Astro Japanは巨大な本島ではなく、島同士の航路を増やす
- **Evidence**: コラボ記事、相互レビュー、登壇リレーなど“小さな航路”がコミュニティを太くする
- **So what**: 1つの中心に依存せず、分散した島々が互いに見える状態を維持できる

---

## 私たちが目指す多島海
- 全員一致は不要。大事なのは「互いの島が見えている」状態
- 技術・思想・コミュニティの話題がClaim/Evidence/So whatで繋がっている
- Astroは島を増やしやすい設計なので、国内でも“分散した航路”を標準化できる

---

## Call to Action
1. **1つ作る** — 記事 / コード / プラグイン / 翻訳
2. **1つ剪定する** — 古いページに日付や注釈を追加
3. **1つ繋ぐ** — 誰かと共同でアウトプット or 次の登壇者を紹介

---
layout: center
class: text-center
---

# 多島海で会いましょう
### Questions / Feedback / Demo follow-up
- (Update contact links here)
