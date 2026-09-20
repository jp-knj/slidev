---
theme: ./theme
author: jp-knj
title: Astro Meetup Japan v1 — Opening
duration: 4min
mdc: true
transition: fade
colorSchema: dark
themeConfig:
  primary: "#e8c4f9"
layout: center-vertical
---

<div class="flex flex-col items-center justify-center gap-8">
  <img src="./images/icon.png" class="w-48" alt="Astro Meetup Japan" />
  <div class="text-center">
    <div class="text-2xl text-white text-opacity-60 font-light">Astro Meetup Japan</div>
    <div class="text-7xl font-black tracking-tight mt-2">v1</div>
  </div>
</div>

<!--
（開幕）こんばんは。Astro Meetup Japan v1 へお越しいただき、ありがとうございます。本日 司会を務めます、ケンジ と申します。今夜は3時間ほど、よろしくお願いします。
-->

---
class: flex items-center justify-center h-full
---

<div class="grid grid-cols-2 gap-8">
    <div>
        <div class="flex items-center gap-4 mt-4">
            <img src="./images/profile.jpeg" class="w-24 rounded-full" alt="profile" />
            <div class="flex flex-col justify-center gap-0">
                <p class="text-2xl !my-0">ケンジ</p>
                <p class="text-xl !my-0">GitHub: <a href="https://github.com/jp-knj">jp-knj</a></p>
            </div>
        </div>
    </div>
    <div>
        <h3>今夜のながれ</h3>
        <ol class="text-xl font-bold">
            <li>立ち上げの想い</li>
            <li>今夜のテーマ</li>
            <li>会場・ルール</li>
        </ol>
    </div>
</div>

<!--
（自己紹介）GitHub では jp-knj として活動しています。最近は Astro 本体へのコントリビュートが増えてきました。今夜は、この Meetup を立ち上げた想い、今夜のテーマ、会場とルール、この3つを駆け足でお伝えします。
-->

---
layout: cover
class: center
---

<div class="mt-8">
  <div class="text-5xl font-black text-white filter drop-shadow-lg leading-tight">
    専門性の内側で、強くなる<br/>
    専門性の外側で、変わっていく
  </div>
</div>

<!--
まず、方向性の話から。ずっと頭にあることなんですが——専門性やセンスは、人を強くする一方で、自分が通用する場所に閉じ込めてもしまう。だからこそ、自分の専門性がまだ通用しない場所に踏み込むことには、価値がある。

そこでは評価も不安定で、うまく話せないし、判断も鈍る。でも、その場所に入ることでしか、自分の専門性は次の形に変わらない——そう思っています。
-->

---
class: flex items-center justify-center h-full
---

<div class="grid grid-cols-2 grid-rows-2 gap-6 items-center h-full">
    <div>
        <img src="./images/astro_meetup_combined.png" class="rounded-lg shadow-2xl w-full" alt="Matt Kane (Astro core maintainer) liked the tweet" />
    </div>
    <div class="pl-4">
        <h3 class="!mt-0">Astro Core への往復</h3>
        <p class="text-lg leading-relaxed !my-0">
          Princesseuh / ematipico / matthewp ——<br/>
          英語のニュアンスも議論の作法も、<br/>
          自分のセンスが通用しない場所。
        </p>
    </div>
    <div class="pr-4 text-right">
        <p class="text-2xl font-bold leading-relaxed !my-0">
          Astroをキッカケに<br/>日本にきてもらう
        </p>
    </div>
    <div class="relative">
        <img src="./images/fec_invite_slide.png" class="rounded-lg shadow-2xl w-full" alt="FEC Fukuoka invite — Lou's reply on Discord" />
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
            <span class="text-7xl drop-shadow-lg">🎉</span>
        </div>
    </div>
</div>

<!--
個人的な話で恐縮ですが、私自身、ここ最近 Astro 本体へのコントリビュートを通じて、Princesseuh さん、ematipico さん、matthewp といった海外のチームメンバーとやり取りする機会が増えてきました。

英語のニュアンスに自信がない、議論の作法もまだ慣れない——まさに、自分のセンスが通用しない場所です。

でも、やってみて分かったのは、距離は思ったほど遠くないということ。Issue、PR、Discord での雑談——その一つひとつが、確かに本体に届いていく感覚があります。

逆方向も、ちゃんと作りたいと思っています。いつか Core のメンバーが日本に来てくれたとき、ちゃんとサポートできるコミュニティでありたい。

日本と Astro 本体の間に 双方向の往復 が生まれたら、もっと面白いことが起きるはずです。この Meetup を、その往復の入口にしたい——というのが、立ち上げの一番の想いです。
-->

---
layout: section
---

# 今夜のテーマ
## Astro で自作したものを見せ合う

<div class="mt-12 text-xl text-white text-opacity-70 leading-relaxed">
  デザイナーがコードに踏み込む。<br/>
  エンジニアがデザインを覗き込む。<br/>
  ノンコードの人がフレームワークの世界に入る。
</div>

<div class="mt-8 text-2xl font-bold">
  Astro は、そういう敷居を低くしてくれる道具。
</div>

<!--
今夜のテーマは「Astro で自作したものを見せ合う」。パネリストがそれぞれ作ったもの、考え方を持ち寄って、みんなで話していく時間です。

デザイナーがコードに踏み込む、エンジニアがデザインを覗き込む、ノンコードの人がフレームワークの世界に入る——Astro はそういう敷居を、わりと低くしてくれる道具だと思っています。

今夜、自分の専門の外側に一歩はみ出す何かを、持ち帰っていただけたら本望です。
-->

---
layout: default
---

## 会場のご案内

<div class="mt-8 text-xl leading-loose">
  <p>会場：<span class="font-bold">サイボウズ株式会社 日本橋オフィス</span></p>
  <p class="text-base text-white text-opacity-70 !mt-0">スポンサーいただきありがとうございます 🙏</p>
</div>

<div class="mt-10 grid grid-cols-2 gap-6">
  <div class="p-4 rounded-xl border border-white/30">
    <h3 class="!mt-0 !mb-2">Wi-Fi</h3>
    <p class="!my-0">SSID: <code>{{TODO_SSID}}</code></p>
    <p class="!my-0">Password: <code>{{TODO_PW}}</code></p>
  </div>
  <div class="p-4 rounded-xl border border-white/30">
    <h3 class="!mt-0 !mb-2">設備</h3>
    <p class="!my-0">お手洗い：{{TODO_TOILET}}</p>
    <p class="!my-0">非常時：{{TODO_EVAC}}</p>
  </div>
</div>

<!--
TODO（当日埋める）:
- Wi-Fi SSID / パスワード
- お手洗いの場所
- 非常時の避難経路

会場は サイボウズ株式会社さんの日本橋オフィスをお借りしています。改めて、ありがとうございます。

Wi-Fi は SSID が [SSID]、パスワードが [PW] です。後ろのスライドにも出しておきます。お手洗いは [場所] にあります。非常時は [避難経路] でお願いします。
-->

---
layout: default
class: flex flex-col items-center justify-center h-full
---

<div class="text-center">
  <div class="text-xl text-white text-opacity-60 mb-4">実況・感想は</div>
  <div class="text-8xl font-black tracking-tight">#AstroJP</div>
</div>

<div class="mt-16 text-lg text-white text-opacity-80 text-center">
  <p>{{TODO_PHOTO_NOTE}}</p>
  <p class="mt-4">困ったことがあれば、運営スタッフまで。</p>
</div>

<!--
TODO（当日埋める）:
- 写真撮影の配慮事項（一言）

最後に、お願いを2つだけ。実況・感想は #AstroJP でお願いします。[写真撮影の配慮事項を一言]。困ったことがあれば、運営スタッフまでお声がけください。
-->

---
layout: center
---

<div class="text-center">
  <div class="text-3xl font-light text-white text-opacity-70">それでは、</div>
  <div class="text-6xl font-black mt-4 leading-tight">Astro Meetup Japan v1<br/>楽しんでいきましょう</div>
  <div class="mt-12 text-xl text-white text-opacity-80">
    モデレーター <span class="font-bold">@yuheiy</span> さんへ
  </div>
</div>

<!--
それでは、Astro Meetup Japan v1、楽しんでいきましょう。

最初のセッションは、パネルディスカッション 『Astro で自作したものを見せ合う』。ここからは、モデレーターの _yuhey さん にバトンをお渡しします。よろしくお願いします。
-->
