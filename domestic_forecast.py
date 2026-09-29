# -*- coding: utf-8 -*-
"""
คาดการณ์ราคาตลาดในประเทศ — วิธี seasonal-naive + ทดสอบย้อนหลัง (walk-forward) เทียบ naive
ทำตามกฎโปรเจกต์: ราคารายเดือน = near-random-walk → ห้ามอ้างแม่นถ้าไม่ผ่าน out-of-sample
"""
import json, statistics as st, io, os

BASE = "/Users/nicha/Library/Mobile Documents/com~apple~CloudDocs/claude/Data Import-Export/ข้อมูลทำคาดการณ์"
D = json.load(io.open(os.path.join(BASE, "data/series.json"), encoding="utf-8"))
dom = D["domestic"]
parts = json.load(io.open(os.path.join(BASE, "data/domestic_parts.json"), encoding="utf-8"))["points"]


def series(field, src=dom, key="ym"):
    return [(r[key], r[field]) for r in src if r.get(field) is not None]


def seasonal_index(vals, period=12, minyears=3):
    """ดัชนีฤดูกาลแบบ centered MA — คืน None ถ้าข้อมูลสั้นเกินไป"""
    if len(vals) < period * minyears:
        return None
    ma = []
    h = period // 2
    for i in range(len(vals)):
        if i - h < 0 or i + h >= len(vals):
            ma.append(None); continue
        w = vals[i - h:i + h + 1]
        ma.append((sum(w) - (w[0] + w[-1]) / 2) / period)
    ratio = {}
    for i, m in enumerate(ma):
        if m:
            ratio.setdefault(i % period, []).append(vals[i] / m)
    if len(ratio) < period:
        return None
    idx = {k: st.median(v) for k, v in ratio.items()}
    mean = sum(idx.values()) / period
    return {k: v / mean for k, v in idx.items()}


def fc_seasonal(ys, vals, h, anchor_w=(0.7, 0.3)):
    """anchor = 0.7*ค่าล่าสุด + 0.3*ค่าเฉลี่ย 3 เดือน แล้วคูณดัชนีฤดูกาล"""
    si = seasonal_index(vals)
    last_m = int(ys[-1][5:7]) - 1
    base = anchor_w[0] * vals[-1] + anchor_w[1] * (sum(vals[-3:]) / 3)
    if si:
        base /= si[last_m]
    out = []
    for k in range(1, h + 1):
        m = (last_m + k) % 12
        out.append(base * (si[m] if si else 1.0))
    return out, (si is not None)


def fc_naive(vals, h):
    return [vals[-1]] * h


def backtest(ys, vals, horizon=3, start=24):
    """walk-forward: ทำนาย h เดือนข้างหน้าจากข้อมูลถึงเวลานั้น เทียบ naive"""
    errs_s, errs_n = [], []
    for t in range(start, len(vals) - horizon):
        fs, _ = fc_seasonal(ys[:t + 1], vals[:t + 1], horizon)
        fn = fc_naive(vals[:t + 1], horizon)
        for k in range(horizon):
            a = vals[t + 1 + k]
            errs_s.append(abs(fs[k] - a) / a)
            errs_n.append(abs(fn[k] - a) / a)
    if not errs_s:
        return None
    return (sum(errs_s) / len(errs_s) * 100, sum(errs_n) / len(errs_n) * 100, len(errs_s))


def band(vals, h):
    """กรอบจากความผันผวนของ %เปลี่ยนรายเดือนในอดีต (สะสมตามราก h)"""
    ch = [abs(vals[i] / vals[i - 1] - 1) for i in range(1, len(vals))]
    sd = st.pstdev(ch) if len(ch) > 2 else 0.05
    return [1.28 * sd * (k ** 0.5) for k in range(1, h + 1)]     # ~80%


H = 15                     # ต.ค. 2569 → ธ.ค. 2570
out = {}
print("=" * 72)
print(f"{'ซีรีส์':16s} {'n':>3s}  {'ฤดูกาล':>6s}  {'MAPE seasonal':>13s} {'MAPE naive':>10s}  ใช้วิธี")
print("-" * 72)

for field, name in [("live", "ไก่ใหญ่ (ไก่เป็น)"), ("chick", "ลูกไก่"),
                    ("pork", "สุกร"), ("egg", "ไข่ไก่"),
                    ("corn", "ข้าวโพด"), ("soymeal", "กากถั่วเหลือง")]:
    s = series(field)
    ys = [a for a, _ in s]; vals = [b for a, b in s]
    bt = backtest(ys, vals)
    fs, has_season = fc_seasonal(ys, vals, H)
    fn = fc_naive(vals, H)
    use_season = bool(bt and has_season and bt[0] < bt[1])       # ใช้ฤดูกาลเฉพาะตอนชนะ naive จริง
    fc = fs if use_season else fn
    bd = band(vals, H)
    out[field] = {"name": name, "last_ym": ys[-1], "last": vals[-1],
                  "fc": [round(v, 2) for v in fc],
                  "lo": [round(v * (1 - b), 2) for v, b in zip(fc, bd)],
                  "hi": [round(v * (1 + b), 2) for v, b in zip(fc, bd)],
                  "method": "seasonal" if use_season else "naive",
                  "mape_s": round(bt[0], 1) if bt else None,
                  "mape_n": round(bt[1], 1) if bt else None,
                  "n": len(vals)}
    print(f"{name:16s} {len(vals):3d}  {'มี' if has_season else 'ไม่มี':>6s}  "
          f"{bt[0]:12.1f}% {bt[1]:9.1f}%  {'ฤดูกาล' if use_season else 'naive (ค่าล่าสุด)'}")

json.dump(out, io.open("/tmp/dom_fc.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nพยากรณ์ 3 เดือนแรก (ต.ค./พ.ย./ธ.ค. 69):")
for f, o in out.items():
    print(f"  {o['name']:16s} ล่าสุด {o['last']:>6.2f} → " +
          " · ".join(f"{v:.1f}" for v in o["fc"][:3]) +
          f"   (กรอบ ธ.ค. {o['lo'][2]:.1f}–{o['hi'][2]:.1f})")
