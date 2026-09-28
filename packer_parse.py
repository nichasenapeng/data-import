# -*- coding: utf-8 -*-
"""สกัดตารางแยกบริษัท (Table 4 / 5.1) — ใช้แถว EST เป็นแกนคอลัมน์ แล้ว map คอลัมน์เข้าบริษัท"""
import re, sys, json
import pdfplumber

CID = re.compile(r"\(cid:(\d+)\)")
NAMES = ["CP", "Betagro", "CPP", "GFPT", "GFN", "TYSON", "LT", "PN", "SUN",
         "CMT", "TFG", "F&F", "NON-MEMBERS"]


def dec(s):
    return CID.sub(lambda m: chr(int(m.group(1)) + 29), s or "")


def rows_of(page, ytol=4):
    # ลายน้ำเป็นฟอนต์ AdobeThai ขนาด 160-270pt วางทับตาราง → กรองทิ้งก่อน (เหลือแต่ตัวหนังสือจริง ~4pt)
    p = page.filter(lambda o: o.get("size", 0) < 10 if o.get("object_type") == "char" else True)
    p = p.dedupe_chars(tolerance=2)
    buckets = {}
    for w in p.extract_words():
        t = dec(w["text"]).strip()
        if not t:
            continue
        buckets.setdefault(round(w["top"] / ytol), []).append(
            {"t": t, "c": (w["x0"] + w["x1"]) / 2, "x0": w["x0"], "x1": w["x1"]})
    out = []
    for _, v in sorted(buckets.items()):
        v = sorted(v, key=lambda w: w["x0"])
        merged = []                       # บางแถว (ญี่ปุ่น/สิงคโปร์) ตัวเลขแตกเป็นตัวอักษร → ต่อคำที่ห่าง <3px
        for w in v:
            if merged and w["x0"] - merged[-1]["x1"] < 3:
                merged[-1] = {"t": merged[-1]["t"] + w["t"], "x0": merged[-1]["x0"],
                              "x1": w["x1"], "c": (merged[-1]["x0"] + w["x1"]) / 2}
            else:
                merged.append(dict(w))
        out.append(merged)
    return out


def num(t):
    t = t.replace(",", "").strip()
    if t in ("-", "—", ""):
        return 0.0
    return float(t) if re.fullmatch(r"-?\d+(\.\d+)?", t) else None



def assign_cols(cols, comp):
    """แบ่งคอลัมน์ให้บริษัทแบบ "ต่อเนื่องซ้ายไปขวา" ด้วย DP
    (หัวตารางวางชื่อบริษัทไว้กึ่งกลางกลุ่มของตัวเอง → เลือกจุดตัดที่ทำให้
     กึ่งกลางของแต่ละกลุ่มใกล้ตำแหน่งชื่อบริษัทมากที่สุด)
    วิธี 'ใกล้ที่สุดทีละคอลัมน์' ใช้ไม่ได้ เพราะคอลัมน์ริมกลุ่มใหญ่ (เช่น CPF 139 ของ CP)
    จะไปตกกลุ่มข้างเคียงที่ชื่ออยู่ใกล้กว่า"""
    names = [n for n, _ in sorted(comp.items(), key=lambda kv: kv[1])]
    xs = [comp[n] for n in names]
    n, k = len(cols), len(names)
    if k == 0 or n < k:
        return [names[0] if names else "?" for _ in cols]
    INF = float("inf")
    best = [[INF] * (k + 1) for _ in range(n + 1)]
    back = [[0] * (k + 1) for _ in range(n + 1)]
    best[0][0] = 0
    for j in range(1, k + 1):
        for i in range(j, n - (k - j) + 1):
            for b in range(j - 1, i):
                if best[b][j - 1] == INF:
                    continue
                grp = cols[b:i]
                cost = best[b][j - 1] + abs(sum(grp) / len(grp) - xs[j - 1])
                if cost < best[i][j]:
                    best[i][j] = cost
                    back[i][j] = b
    out, i = [None] * n, n
    for j in range(k, 0, -1):
        b = back[i][j]
        for t in range(b, i):
            out[t] = names[j - 1]
        i = b
    return out


def parse(page):
    rows = rows_of(page)
    # 1) หัวตาราง: ชื่อบริษัท (อยู่ได้ 2 แถว) — หาแถวที่มี TOTAL
    hdr_i = next((i for i, r in enumerate(rows) if any(w["t"] == "TOTAL" for w in r)), None)
    if hdr_i is None:
        return None
    comp = {}
    for i in range(max(0, hdr_i - 2), hdr_i + 3):
        for w in rows[i]:
            if w["t"] in NAMES and w["t"] not in comp:
                comp[w["t"]] = w["c"]
    # 2) แถว EST = แกนคอลัมน์ (อยู่ใต้หัวตาราง ภายใน 4 แถว)
    est_i = next((i for i in range(hdr_i, min(hdr_i + 6, len(rows)))
                  if rows[i] and rows[i][0]["t"].upper().startswith("EST")), None)
    if est_i is None:
        return None
    if len(rows[est_i]) < 5 and est_i + 1 < len(rows):   # บางหน้า 'EST' อยู่คนละแถวกับรหัส
        est_i += 1
        cols = [w["c"] for w in rows[est_i]]
    else:
        cols = [w["c"] for w in rows[est_i][1:]]
    cols.sort()
    col_comp = assign_cols(cols, comp)

    out = []
    for r in rows[est_i + 1:]:
        if not r:
            continue
        label = r[0]["t"]
        vals = [(w["c"], num(w["t"])) for w in r[1:]]
        vals = [(c, v) for c, v in vals if v is not None]
        if len(vals) < 8:
            continue
        total = vals[-1][1]                      # คอลัมน์ขวาสุด = TOTAL
        agg = {}
        for c, v in vals[:-1]:
            k = col_comp[min(range(len(cols)), key=lambda i: abs(cols[i] - c))]
            agg[k] = agg.get(k, 0) + v
        out.append({"label": label, "by": agg, "total": total,
                    "sum": sum(agg.values())})
    return {"companies": comp, "cols": len(cols), "rows": out}


if __name__ == "__main__":
    f, pg = sys.argv[1], int(sys.argv[2])
    with pdfplumber.open(f) as pdf:
        res = parse(pdf.pages[pg - 1])
    print("คอลัมน์:", res["cols"], "· บริษัท:", len(res["companies"]))
    for r in res["rows"][:16]:
        ok = "OK " if abs(r["sum"] - r["total"]) <= 2 else "!!! "
        print(f"{ok}{r['label'][:18]:18s} รวม={r['sum']:>10,.0f} / TOTAL={r['total']:>10,.0f}"
              f" · SUN={r['by'].get('SUN',0):>8,.0f}")
