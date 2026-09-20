// 和文は M PLUS 2（可変フォント）を npm 同梱で配る。
// Astro のブランド書体（Obviously / Inter / MDIO）は fonts.css 経由で
// fonts-cdn.astro.build から読み込む。
import '@fontsource-variable/m-plus-2'
import './fonts.css'
import './layout.css'
