# -*- coding: utf-8 -*-
"""สร้างชุดคาดการณ์ราคาในประเทศ + ผลทดสอบย้อนหลัง → /tmp/dfc_blob.js (var DFC=...) แปะใน index.html\nรัน: python3 domestic_forecast_build.py  (ต้องมี data/series.json + domestic_parts.json ของโปรเจกต์คาดการณ์)"""
import json, statistics as st, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from domestic_forecast import (series, seasonal_index, fc_seasonal, fc_naive, backtest, band, dom, parts)

H = 15                      # ต.ค. 2569 → ธ.ค. 2570
HP = 6                      # ชิ้นส่วน: ต.ค. 2569 → มี.ค. 2570 (ข้อมูลสั้น ไม่ยืดไกล)

out = {"h": H, "hp": HP, "start": "2026-10", "series": {}, "parts": {}}

for field, name, unit in [("live", "ไก่เป็น (ไก่ใหญ่)", "บาท/กก."), ("chick", "ลูกไก่", "บาท/ตัว"),
                          ("corn", "ข้าวโพด", "บาท/กก."), ("soymeal", "กากถั่วเหลือง", "บาท/กก."),
                          ("pork", "สุกรขุน", "บาท/กก."), ("egg", "ไข่ไก่คละ", "บาท/ฟอง")]:
    s = series(field)
    ys = [a for a, _ in s]
    vals = [b for _, b in s]
    bt = backtest(ys, vals)
    fs, has_season = fc_seasonal(ys, vals, H)
    use_season = bool(bt and has_season and bt[0] < bt[1])
    fc = fs if use_season else fc_naive(vals, H)
    bd = band(vals, H)
    out["series"][field] = {
        "name": name, "unit": unit, "n": len(vals), "last": vals[-1], "last_ym": ys[-1],
        "hist": [{"ym": y, "v": v} for y, v in s if y >= "2024-01"],
        "fc": [round(v, 2) for v in fc],
        "lo": [round(v * (1 - b), 2) for v, b in zip(fc, bd)],
        "hi": [round(v * (1 + b), 2) for v, b in zip(fc, bd)],
        "method": "seasonal" if use_season else "naive",
        "mape": round(bt[0] if use_season else bt[1], 1) if bt else None,
        "mape_other": round(bt[1] if use_season else bt[0], 1) if bt else None,
    }

# ---- ชิ้นส่วน: มีแต่ปี 2569 (รายงาน ~2 สัปดาห์) → เฉลี่ยรายเดือนแล้ว naive + กรอบกว้าง ----
for field, name in [("leg", "น่องติดสะโพก"), ("bb", "เนื้อ BB"), ("kron", "โครงเต็ม")]:
    m = {}
    for r in parts:
        if r.get(field) is None:
            continue
        m.setdefault(r["date"][:7], []).append(r[field])
    ms = sorted(m)
    vals = [sum(m[k]) / len(m[k]) for k in ms]
    bd = band(vals, HP)
    last = vals[-1]
    out["parts"][field] = {
        "name": name, "unit": "บาท/กก.", "n": len(vals), "last": round(last, 1), "last_ym": ms[-1],
        "hist": [{"ym": k, "v": round(v, 1)} for k, v in zip(ms, vals)],
        "fc": [round(last, 1)] * HP,
        "lo": [round(last * (1 - b), 1) for b in bd],
        "hi": [round(last * (1 + b), 1) for b in bd],
        "method": "naive", "mape": None,
    }

io.open("/tmp/dom_fc2.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False))
blob = "var DFC=" + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";"
io.open("/tmp/dfc_blob.js", "w", encoding="utf-8").write(blob)

print("ซีรีส์ยาว (5 ปี):")
for k, v in out["series"].items():
    print(f"  {v['name']:18s} n={v['n']:3d} ล่าสุด {v['last']:>6.2f} → ธ.ค.69 {v['fc'][2]:>6.2f} "
          f"(กรอบ {v['lo'][2]:.1f}–{v['hi'][2]:.1f}) · {v['method']} MAPE {v['mape']}% (อีกวิธี {v['mape_other']}%)")
print("ชิ้นส่วน (ปี 2569 เท่านั้น):")
for k, v in out["parts"].items():
    print(f"  {v['name']:18s} n={v['n']} เดือน ล่าสุด {v['last']:>5.1f} → กรอบ มี.ค.70 {v['lo'][-1]:.0f}–{v['hi'][-1]:.0f}")
print("blob:", len(blob), "ตัวอักษร")
