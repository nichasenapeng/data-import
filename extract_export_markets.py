# -*- coding: utf-8 -*-
"""
extract_export_markets.py
สกัด "ปริมาณส่งออกไก่ไทยรายเดือน แยกตลาด/แยกไก่สด-ปรุงสุก" จากรายงานประชุมสมาคมฯ (Packer PDF)
→ export_markets.json  (ใช้ป้อน Tab 10 ของ index.html)

หลักการ:
- ตาราง "Table 2 : Thai Chicken Export Classified by Country" เป็น **ยอดสะสม YTD** (เช่น [Jan-Aug])
  และมี 2 ปีคู่กันเสมอ (ปีก่อน vs ปีนี้) → เก็บได้ทีละ 2 ปีต่อรายงาน 1 ฉบับ
- รายงานออกทุก ~2 สัปดาห์ และมีการ revise → **ใช้ฉบับที่ออกทีหลังสุดเสมอ** สำหรับงวดเดียวกัน
  (คอลัมน์ "ปีก่อน" ของรายงานปีถัดไป = ตัวเลขที่ revise แล้ว จึงชนะฉบับเก่า)
- ได้ YTD ครบแล้วค่อยหักลบเป็นรายเดือน โดยหักลบภายใน "ชุดข้อมูลเดียวกัน" ไม่ข้ามชุด

รัน: python3 extract_export_markets.py   (ต้องมี pdfplumber)
"""
import os, re, csv, json, glob, datetime as dt

PDF_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "ข้อมูลทำคาดการณ์", "02-ประชุมสมาคม (มีทั้งราคาและสถานการณ์)")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "export_markets.json")

MON = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}

# ชื่อตลาดในหน้าเว็บ -> ชื่อแถวในตาราง (ถ้ามีหลายแถว = รวมกัน เช่น มาเลเซีย KL + SABAH)
MARKETS = {
    "jp":  ["- JAPAN"],
    "eu":  ["THE EUROPEAN UNION"],
    "uk":  ["- UNITED KINGDOM"],
    "my":  ["- MALAYSIA KL", "- MALAYSIA SABAH"],
    "hk":  ["- HONG KONG"],
    "kr":  ["- S.KOREA"],
    "cn":  ["- CHINA"],
}


def report_date(path):
    """วันที่ออกรายงานจากชื่อไฟล์ เช่น Packer15_2569(9Sep2026).pdf"""
    m = re.search(r"\((\d{1,2})([A-Za-z]{3})(\d{4})\)", os.path.basename(path))
    if not m:
        return dt.date(1900, 1, 1)
    return dt.date(int(m.group(3)), MON[m.group(2).lower()], int(m.group(1)))


def merge_words(words, gap=5):
    """pdfplumber แตกตัวเลขเป็นหลายคำ ('1' + '34,142') เพราะช่องไฟในไฟล์ PDF
    → ต่อคำที่ห่างกันน้อยกว่า gap พิกเซลเข้าด้วยกัน (ช่องว่างระหว่างคอลัมน์จริง ~20px ขึ้นไป)"""
    out = []
    for w in sorted(words, key=lambda x: x["x0"]):
        if out and w["x0"] - out[-1]["x1"] < gap:
            out[-1] = {"text": out[-1]["text"] + w["text"], "x0": out[-1]["x0"], "x1": w["x1"]}
        else:
            out.append({"text": w["text"], "x0": w["x0"], "x1": w["x1"]})
    return out


def page_rows(page):
    """คืนรายการ (ข้อความทั้งแถว, [token ที่ต่อคำแล้ว]) เรียงจากบนลงล่าง"""
    buckets = {}
    for w in page.extract_words():
        buckets.setdefault(round(w["top"] / 3), []).append(w)
    rows = []
    for k in sorted(buckets):
        toks = [t["text"] for t in merge_words(buckets[k])]
        rows.append((" ".join(toks), toks))
    return rows


def row_values(toks):
    """ตัวเลขในแถว (ข้าม token ที่เป็นตัวอักษร) · '-' = 0 · 'NC' = ข้าม"""
    out = []
    for t in toks:
        if t in ("-", "\u2014"):
            out.append(0.0)
        elif t.upper() == "NC":
            out.append(None)
        else:
            v = t.replace(",", "")
            if re.fullmatch(r"-?\d+(\.\d+)?", v):
                out.append(float(v))
    return out


def parse_pdf(path):
    """คืน (เดือนสุดท้ายของงวด, ปีก่อน, ปีนี้, {ตลาด: (สดปีก่อน, สดปีนี้, สุกปีก่อน, สุกปีนี้)})"""
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            if "Classified by Country" not in t or "JAPAN" not in t:
                continue
            head = re.search(r"Compare with (\d{4})/(\d{4})", t)
            if not head:
                continue
            prev_y, cur_y = int(head.group(1)), int(head.group(2))
            rows = page_rows(page)
            mon = None
            for txt, _ in rows:      # งวดจาก [Jan-Aug] / [Jan] (งวดเดือนแรก) / หัวคอลัมน์ 'Jan-Aug 25'
                if re.search(r"\[Jan\]", txt):
                    mon = 1
                    break
                m = re.search(r"\[Jan-(\w{3})\]", txt) or re.search(r"Jan-(\w{3})\s*\d{2}", txt)
                if m and m.group(1).lower() in MON:
                    mon = MON[m.group(1).lower()]
                    break
            if mon is None:
                return None
            vals = {}
            for key, names in MARKETS.items():
                acc, found = [0.0, 0.0, 0.0, 0.0], False
                for name in names:
                    # การต่อคำทำให้ '- JAPAN' กลายเป็น '-JAPAN' → เทียบแบบตัดช่องว่างทิ้ง
                    nm = name.replace(" ", "")
                    for txt, toks in rows:
                        if not txt.replace(" ", "").startswith(nm):
                            continue
                        n = row_values(toks)
                        if len(n) >= 8 and None not in n[:5]:
                            # [สดปีก่อน, สดปีนี้, %, สุกปีก่อน, สุกปีนี้, %, รวมปีก่อน, รวมปีนี้, %]
                            if abs((n[0] + n[3]) - n[6]) <= 2 and abs((n[1] + n[4]) - n[7]) <= 2:
                                acc[0] += n[0]; acc[1] += n[1]; acc[2] += n[3]; acc[3] += n[4]
                                found = True
                        break
                if found:
                    vals[key] = tuple(acc)
            return mon, prev_y, cur_y, vals
    return None


def main():
    files = sorted(glob.glob(os.path.join(PDF_ROOT, "**", "*.pdf"), recursive=True), key=report_date)
    print(f"อ่าน PDF {len(files)} ไฟล์ (เรียงตามวันที่ออกรายงาน)")
    # ytd[year][market][month] = (raw, cooked) · ฉบับที่ออกทีหลังทับของเดิม
    ytd, src = {}, {}
    for f in files:
        try:
            got = parse_pdf(f)
        except Exception as e:
            print(f"  [warn] {os.path.basename(f)}: {e}")
            continue
        if not got:
            continue
        mon, py, cy, vals = got
        for key, (rp, rc, cp, cc) in vals.items():
            for year, raw, ck in ((py, rp, cp), (cy, rc, cc)):
                ytd.setdefault(year, {}).setdefault(key, {})[mon] = (raw, ck)
                src.setdefault(year, {}).setdefault(key, {})[mon] = os.path.basename(f)

    data = {}
    for year in sorted(ytd):
        data[str(year)] = {}
        for key in MARKETS:
            months = ytd[year].get(key, {})
            fresh, cooked = [None] * 12, [None] * 12
            for mi in range(1, 13):
                if mi not in months:
                    continue
                prev = months.get(mi - 1) if mi > 1 else (0.0, 0.0)
                if prev is None:
                    continue                                   # เดือนก่อนหน้าไม่มี → หักลบไม่ได้
                fresh[mi - 1] = round(months[mi][0] - prev[0])
                cooked[mi - 1] = round(months[mi][1] - prev[1])
            data[str(year)][key] = {"fresh": fresh, "cooked": cooked,
                                    "ytd_last": max(months) if months else None}
    out = {"_source": "Table 2 รายงานประชุมสมาคมฯ (ยอดสะสม YTD → หักลบเป็นรายเดือน)",
           "_generated": dt.datetime.now().isoformat(timespec="seconds"),
           "markets": list(MARKETS), "data": data}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)

    for year in sorted(data):
        for key in MARKETS:
            d = data[year][key]
            n = sum(1 for v in d["fresh"] if v is not None)
            if n:
                tf = sum(v for v in d["fresh"] if v is not None)
                tc = sum(v for v in d["cooked"] if v is not None)
                print(f"  {year} {key:4s} {n:2d} เดือน · สด {tf:,.0f} · ปรุงสุก {tc:,.0f}")
    print("เขียน", OUT)


if __name__ == "__main__":
    main()
