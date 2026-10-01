# xmdx の自作とベンチマークで分かったこと

38 枚目から 40 枚目の発話の補足資料。2026 年 10 月 1 日に、xmdx の実装と既存の記録を確認した。新しいベンチマークは実行していない。

単体の Compiler の速さだけでは、サイトへ導入したときの効果は分からない。必要な機能と互換性をそろえ、Astro のビルド全体でも比べる。この経験を、自作して学んだこととして話す。

## 3 枚で話すこと

| ページ | 話の中心 | 次につながること |
| --- | --- | --- |
| 38 の初期表示 | mdxjs-rs と markdown-rs に提案した機能と配布方法 | JavaScript から Rust を呼ぶ仕組みへ進む |
| 38 のクリック 1 | NAPI-RS で Rust を呼べても、対応環境ごとのビルドとテストと配布を続ける必要がある | 速さに加えて、保守できる範囲も採用の条件になる |
| 38 のクリック 2 | 紹介と助けを受け、MDX の編集支援へ貢献した経験 | 提案の採否だけでは終わらず、学んだことを次へ渡せる |
| 39 | xmdx を Astro と Starlight に組み込んだ全体像と、公式ドキュメントでの検証 | 本文のコードと、サイトに必要な付随情報をどう受け渡すか |
| 40 | 本文と frontmatter と見出し情報、既存の機能への対応 | 同じ機能と条件で比較して初めて、採用の判断に使える |

bindings の定義は 38 枚目で説明する。39 枚目では呼び出し関係を短く話し、40 枚目では返す情報と、対応が必要だった例へ進む。

## ベンチマークでは、何を測ったかをそろえる

ベンチマークは不毛だったよりも、数字だけでは採用を判断できなかったと話すほうが、経験の内容を伝えられる。特定の関数の改善を調べる計測と、サイトへの導入効果を調べる計測には、それぞれ目的がある。

| 計測の範囲 | 分かること | そろえたい条件 |
| --- | --- | --- |
| Parser や Compiler の単体の呼び出し | 特定の入力をパースして変換する速さ | 入力と出力の範囲、初期化、JavaScript との受け渡しを含むか |
| MDX の変換とプラグイン | 必要な変換を組み合わせた時間 | プラグインと実行順、コードの色付け、見出し情報、キャッシュ |
| Astro のビルド全体 | 実際のサイトが完成するまでの時間 | サイトと設定、バージョン、マシン、キャッシュ、ページ数、同時に動く仕事 |

トラバースは、木の node をたどること。プラグインが AST をたどる回数や担当範囲も時間に影響する。unified はパースと木の変換と出力を組み合わせる設計である。どの工程まで含めたかを示せば比較できる。[unified のガイド](https://unifiedjs.com/learn/guide/using-unified/)

Vite 全体を一つのトラバースとして説明するのは適切ではない。Vite plugin の呼び出し、モジュールの変換、バンドルなど、別の工程がある。非同期の仕事もあるため、関数の時間を単純に合計してビルドの経過時間と同じ値になるとは限らない。[Vite の性能ガイド](https://vite.dev/guide/performance.html#audit-configured-vite-plugins)

## xmdx の計測名にも確認が必要だった

参照するのは [xmdx の固定コミット](https://github.com/jp-knj/xmdx/tree/7a89fdb17140e2b710e40d52d26338d978bc5c13)。現在の比較条件をそろえる資料であり、2025 年 7 月の提案時点と同じ実装という意味ではない。

`load-handler.ts` にある `compile` の計測は、Rust の関数だけを測っていない。bindings の呼び出しに加え、JavaScript で frontmatter の JSON をオブジェクトにし、Astro のモジュールを作る範囲も含む。ファイルの取得や入力の事前の調整は、この区間の外にある。[load-handler.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/load-handler.ts)

同じ実装では、変換結果がキャッシュにあると Compiler を呼ばずに結果を返すこともある。コードの色付けに必要な準備も、`transform-pipeline` の計測区間の外で行われる。キャッシュがない状態とある状態を分け、初期化をどこに含めたかも説明する必要がある。[load-handler.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/load-handler.ts)

`load-profiler.ts` の `totalMs` は、ファイルごとの時間を加算する値である。また、記録した工程の合計とその値の差を `overhead` としている。この差をすべて Vite の時間と呼ぶことはできない。サイト全体の経過時間は、別に測る必要がある。[load-profiler.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/vite/src/vite-plugin/load-profiler.ts)

## 互換性は、何を保てるかで説明する

| 確認する対象 | 比べる例 |
| --- | --- |
| 入力 | 今ある Markdown と MDX の記述を扱えるか |
| 出力 | 本文、見出しの ID、目次、frontmatter、コードの色付けが必要な結果になるか |
| プラグイン | 既存の remark と rehype のプラグインや設定を変更せず使えるか |
| 実行環境 | 必要な OS と CPU、Node.js、ビルド環境で導入して動かせるか |

同じ機能を実装できることと、既存のプラグインをそのまま使えることは区別する。独自の API で同じ結果を作れても、プラグインの移行作業が必要な場合がある。

xmdx には、扱えない入力を検出したときに既存の JavaScript の MDX Compiler を使う fallback がある。ただし、この仕組みがあるだけで、すべての入力とプラグインの互換性を保証するわけではない。fallback が動いた件数も、性能を比べる際の条件になる。[fallback の実装](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/fallback/compile.ts)

## 自作で必要になった対応

### 本文に加えて、サイトが使う情報も正しく返す

Rust からは、本文のコード、frontmatter、見出し情報を受け取る。JavaScript はそれを Astro のモジュールに変換し、Starlight のコンポーネント、コードの色付け、JSX の変換を組み合わせる。[load-handler.ts](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/src/vite-plugin/load-handler.ts)

変更履歴には、MDX のインデントしたコードブロックで終了を判定できず、その後の見出しを取得できなかった不具合がある。本文を変換できても、目次や見出しへのリンクが正しいとは限らない。この例なら、速い Compiler を呼ぶ以外にも何を検証したのか説明できる。今回、その不具合を再実行して確認したわけではない。[astro-xmdx の変更履歴](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/packages/astro-xmdx/CHANGELOG.md)

### bindings を作った後も、配布を保守する

NAPI-RS は、Rust の関数を JavaScript から呼ぶコードや型定義、ビルドと配布の仕組みを用意する。ネイティブのバイナリは、対応する環境に合わせてビルドする。Node-API の互換性と、OS と CPU をまたぐ実行形式の互換性は別の話である。[NAPI-RS のパッケージ作成ガイド](https://napi.rs/docs/introduction/simple-package) と [クロスビルドのガイド](https://napi.rs/docs/cross-build)

参照コミットの xmdx は、macOS の x64 と arm64、Windows の x64、Linux の x64 と arm64 について glibc と musl の組み合わせを含む、7 種類のネイティブパッケージを記載している。CI にも Rust、Node.js の bindings、WASM と TypeScript の検証がある。ただし、この記録だけで 7 種類すべての実機テストが成功したとは言えない。[bindings の README](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/crates/napi/README.md) と [CI の設定](https://github.com/jp-knj/xmdx/blob/7a89fdb17140e2b710e40d52d26338d978bc5c13/.github/workflows/ci.yml)

JavaScript から呼べて便利だと思ったけれど、ビルドとテストと配布まで保守する範囲に驚いたは、発表者が練習で話した経験として使う。NAPI-RS 自体が採用しにくいと一般化せず、自分たちが支えられる環境を決める必要があった、とつなげる。

## 口頭で話すなら

ベンチマークの数字を追っても、そのまま採用を決められるわけではなかったんですね。Compiler だけを測るのか、プラグインまで含めるのか、Astro のビルド全体を測るのかで、比べているものが違います。

必要なプラグインが動いて、本文や目次の結果も保てる。その条件をそろえたうえで、サイト全体がどれだけ速くなるかを確かめる必要がある。自作して、そこまで考える必要があると分かったんですね。

## OSS の話へのつなぎ方

発表者の経験では、提案がすぐ採用されず、しんどいこともあった。その後、MDX に貢献したいと話し、Astro のメンバーから Remco を紹介してもらった。助けを受けて編集支援の改善に取り組み、試作で得た知識を別のプロジェクトへ渡せた。

配布の難しさが直接その紹介を生んだ、という因果関係は付け加えない。提案のやり取りで終わらず、人とのつながりもできたと話を移す。xmdx の自作と MDX への貢献には時期の重なりがあり、スライドの順番を厳密な時系列とはしない。

## 数字を発表へ入れる前に確認すること

Pooya Parsa が 2026 年 3 月 13 日に紹介した Astro と md4x の試作は、比較する機能を確認する具体例になる。投稿は Markdown の変換について 50 倍から 70 倍と述べ、コードの色付けは未実装としている。参照した README も remark と rehype のプラグインの実行を未実装に挙げている。速さの可能性を示す数字として紹介できるが、Astro のビルド全体の結果や、既存の機能をすべて含む比較としては使わない。[Pooya の投稿](https://bsky.app/profile/pi0.io/post/3mgwljerlik2h) と [試作の README](https://github.com/pi0/astro-md4x/blob/9ef1c52c8fdcdc964d847ee1642a1af32da65463/README.md)

練習中にビルド時間を半分にできたと本人が話している。比較元と変更後の構成、対象サイト、計測した工程、キャッシュとマシンの条件は未確認。そのため、現時点の原稿には具体的な倍率を追加していない。

Astro への AST Bridge の提案にも性能の数字はあるが、提案の本文に記載された測定である。サイト全体のビルド時間の半減や、既存プラグインとの完全な互換性を裏付ける数字として使わない。[AST Bridge の提案](https://github.com/withastro/astro/pull/14181)

Oxc の Content に関する実装と Sätteri の比較は、対象のパッケージとバージョンと計測条件を特定してから扱う。現時点でどちらが速いかという順位は記載しない。
