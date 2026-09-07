# 作例帳

Blender アドオン **Fabric 3D Texture Generator**（Stratasys J850 向けの
テキスタイル3Dプリント）で作った作例を並べたページ。

- 公開先: GitHub Pages
- 検索避け: `<meta name="robots" content="noindex,nofollow">` を入れてある。
  リンクを渡した人は見られるが、検索結果には出ない。

## このリポジトリの中身

    index.html   1枚だけ。作例の説明と絵の一覧
    img/         作例の絵（幅560px・JPEG）
    .nojekyll    GitHub Pages に Jekyll を通させない

**手で編集しない。** 組み立てるのは stratasys_addon 側の
`docs/away/tools/cards/build_cards.py` で、作例が増えたら

    python build_cards.py

を走らせて、ここで commit / push するだけでよい。
