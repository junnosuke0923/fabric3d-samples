# -*- coding: utf-8 -*-
"""作例帳の閲覧数を GoatCounter から取って counts.json に書く。

公開サイト（fabric3d-samples）の GitHub Actions が 1 日 1 回走らせる。
**このファイルはサイトで直さないこと**——原本はプロジェクト側の
`docs/away/tools/cards/site_extra/fetch_counts.py` にあり、build_cards.py が
組み直すたびに上書きする（サイト名 __CODE__ もそのとき埋まる）。

- 使うのは標準ライブラリだけ（Actions で pip を回さない）
- トークンはリポジトリの Secret `GOATCOUNTER_TOKEN`。**無ければ何もせず
  正常に終わる**——登録前から毎日失敗の通知が飛ばないように
- 取れなかったときは counts.json を**書き換えない**。ページは前日の数で
  並べるか、counts.json が無ければ［閲覧数順］を出さない
"""
import datetime, json, os, re, sys, time, urllib.parse, urllib.request

CODE = "fabric3d-samples"
# 数え始め。閲覧数は「この日から今日まで」の合計（GoatCounter の visitors）。
START = "2026-09-01T00:00:00Z"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "counts.json")
RE_PATH = re.compile(r"^/s(\d+)$")


def main():
    tok = os.environ.get("GOATCOUNTER_TOKEN", "").strip()
    if not tok:
        print("GOATCOUNTER_TOKEN が登録されていないので、何もしない")
        return 0
    if not re.match(r"^[a-z0-9-]+$", CODE):
        print("サイト名が埋まっていない（build_cards.py の GOATCOUNTER）: %r" % CODE)
        return 1
    end = (datetime.datetime.now(datetime.timezone.utc)
           .replace(minute=0, second=0, microsecond=0)
           + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    counts, seen = {}, []
    for _page in range(100):
        q = [("start", START), ("end", end), ("limit", "100")]
        q += [("exclude_paths", str(i)) for i in seen]
        url = ("https://%s.goatcounter.com/api/v0/stats/hits?" % CODE
               + urllib.parse.urlencode(q))
        req = urllib.request.Request(url, headers={
            "Authorization": "Bearer " + tok,
            "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as res:
            data = json.load(res)
        hits = data.get("hits") if isinstance(data, dict) else data
        hits = hits or []
        new = 0
        for h in hits:
            pid = h.get("path_id")
            if pid in seen:
                continue
            seen.append(pid)
            new += 1
            m = RE_PATH.match(h.get("path") or "")
            if m and not h.get("event"):
                n = m.group(1)
                counts[n] = counts.get(n, 0) + int(h.get("count") or 0)
        more = isinstance(data, dict) and data.get("more")
        # 続きが無い・新しい行が来ない（続きの取り方が効いていない）なら止める。
        if not more or not new:
            break
        time.sleep(0.5)   # 上限は 1 秒 4 回
    out = {"updated": end, "since": START,
           "counts": dict(sorted(counts.items(), key=lambda kv: int(kv[0])))}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=0, sort_keys=False)
        f.write("\n")
    print("作例 %d 件ぶんの閲覧数を書いた（%d パスを読んだ）" % (len(counts), len(seen)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
