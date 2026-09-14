# 作例帳

Blender アドオン **Fabric 3D Texture Generator**（Stratasys J850 向けの
テキスタイル3Dプリント）で作った作例を並べたページ。

- 公開先: GitHub Pages
- 検索避け: `<meta name="robots" content="noindex,nofollow">` を入れてある。
  リンクを渡した人は見られるが、検索結果には出ない。

## このリポジトリの中身

    index.html   1枚だけ。作例の説明と絵の一覧
    img/         作例の絵（幅900px・JPEG）
    help/        アドオンのヘルプ（ja.html / en.html）とスライド資料 PDF
    .nojekyll    GitHub Pages に Jekyll を通させない

**手で編集しない。どちらも道具が組み立てる。**

作例帳（`index.html` と `img/`）は stratasys_addon 側の
`docs/away/tools/cards/build_cards.py`。作例が増えたら

    python build_cards.py

ヘルプ（`help/`）は同じく stratasys_addon 側の
`docs/away/tools/publish_share.py`。**先に配布フォルダのヘルプを
作り直しておくこと**（`tests/build_help_html.py`）。

    python docs\away\tools\publish_share.py

公開する側のヘルプにだけ検索避け（`noindex,nofollow`）を差し込むのが
この道具の役目で、配る ZIP の中のヘルプには入れない。スライド資料の
PDF を `help/` へ一緒に置くのは、ヘルプがそれを**同じ階層への相対
リンク**で指しているため。

どちらの場合も、走らせたあと、ここで commit / push するだけでよい。
