# -*- coding: utf-8 -*-
"""
extract_packer.py
สกัด "ยอดส่งออกแยกรายบริษัท (packer)" จากไฟล์ในโฟลเดอร์ `ราคาแยก packer`
→ packer_data.json   (ใช้ป้อนแท็บ "แยก packer" ของ index.html)

ที่มา: รายงานสมาคมฯ ฉบับที่มีตารางแยกบริษัท (เดือน ก.พ./เม.ย./พ.ค./ก.ค. 2569)
  Table 4   = ยอดรายเดือนแยกบริษัท (ไก่สด+ปรุงสุก)
  Table 4.1 = เฉพาะไก่สด · Table 4.2 = เฉพาะปรุงสุก
  Table 5.1 = ยอด "เดือนนั้น" แยกประเทศ × บริษัท

⚠️ ตัวเลขประเทศใน Table 5 ไม่เท่ากับ Table 2 (ที่แท็บ "ตลาดส่งออกไทย" ใช้)
   Table 2 = ประมาณการจากศุลกากร · Table 5 = รวบรวมจากบริษัท → ห้ามเอามาหารข้ามตาราง
   ทุก % ในไฟล์นี้คิดจากตารางเดียวกันเสมอ

รัน: python3 extract_packer.py
"""
import os, re, glob, json, datetime as dt
import pdfplumber
import packer_parse as PP

BASE = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE, "..", "ข้อมูลทำคาดการณ์",
                       "02-ประชุมสมาคม (มีทั้งราคาและสถานการณ์)", "ราคาแยก packer")
OUT = os.path.join(BASE, "packer_data.json")
MON3 = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
MONTH_ROWS = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]


def file_month(path):
    m = re.search(r"([A-Z][a-z]{2})(\d{2})SUN", os.path.basename(path))
    return MON3.get(m.group(1), 0) if m else 0


def find_page(pdf, key):
    """หน้าที่ขึ้นต้นด้วยหัวตารางที่ต้องการ (เทียบแบบตัดช่องว่าง)"""
    want = key.lower().replace(" ", "")
    for i, pg in enumerate(pdf.pages):
        t = PP.dec(pg.dedupe_chars(tolerance=2).extract_text() or "")
        if want in re.sub(r"\s+", " ", t).lower().replace(" ", ""):
            return i
    return None


def rows_by_label(parsed):
    out = {}
    if not parsed:
        return out
    for r in parsed["rows"]:
        lab = r["label"].strip("- ").upper()
        if abs(r["sum"] - r["total"]) > 2:      # แถวที่ตรวจไม่ผ่าน (ผลรวมบริษัท != TOTAL) ทิ้ง
            continue
        out[lab] = {"total": r["total"], "by": {k: v for k, v in r["by"].items() if v}}
    return out


def main():
    files = sorted(glob.glob(os.path.join(PDF_DIR, "DATA EXPORT *SUN.pdf")), key=file_month)
    if not files:
        print("  [warn] ไม่พบไฟล์ในโฟลเดอร์ 'ราคาแยก packer'")
        return
    latest = files[-1]
    print(f"ไฟล์ล่าสุด: {os.path.basename(latest)} · ทั้งหมด {len(files)} ไฟล์")

    data = {"_source": "รายงานสมาคมฯ ตารางแยกบริษัท (Table 4 / 5.1) โฟลเดอร์ 'ราคาแยก packer'",
            "_generated": dt.datetime.now().isoformat(timespec="seconds"),
            "_note": "% ทุกตัวคิดจากตารางเดียวกัน · Table 5 ไม่เท่ากับ Table 2 ของแท็บตลาดส่งออกไทย"}

    # ---- รายเดือนแยกบริษัท (เอาจากไฟล์ล่าสุด ซึ่งครอบคลุมเดือนมากที่สุด) ----
    with pdfplumber.open(latest) as pdf:
        for key, name in (("Table4 :", "all"), ("Table4.1", "raw"), ("Table4.2", "cooked")):
            i = find_page(pdf, key)
            if i is None:
                continue
            rows = rows_by_label(PP.parse(pdf.pages[i]))
            months, total = {}, {}
            for mi, mlabel in enumerate(MONTH_ROWS, start=1):
                r = rows.get(mlabel.upper())
                if r and r["total"]:
                    months[mi] = {"total": r["total"], "by": r["by"]}
            if "TOTAL" in rows:
                total = rows["TOTAL"]
            data.setdefault("monthly", {})[name] = {"months": months, "ytd": total}
            print(f"  {key:9s} → {len(months)} เดือน · รวม {total.get('total',0):,.0f} ตัน")

    # ---- ประเทศ × บริษัท (เดือนของแต่ละไฟล์) ----
    by_country = {}
    for f in files:
        mon = file_month(f)
        with pdfplumber.open(f) as pdf:
            i = find_page(pdf, "TABLE 5.1")
            if i is None:
                continue
            rows = rows_by_label(PP.parse(pdf.pages[i]))
        keep = {}
        for lab, r in rows.items():
            if r["total"] > 0 or r["by"].get("SUN"):
                # เก็บครบทุกบริษัท ไม่ใช่แค่ SUN → ใช้ทำตาราง "ใครส่งไปตลาดไหน"
                keep[lab] = {"total": r["total"], "sun": r["by"].get("SUN", 0),
                             "by": {k: round(v) for k, v in r["by"].items() if v}}
        by_country[mon] = keep
        print(f"  Table 5.1 เดือน {mon}: {len(keep)} แถว · SUN รวม {keep.get('TOTAL',{}).get('sun',0):,.0f} ตัน")
    data["by_country"] = by_country

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print("เขียน", OUT)


if __name__ == "__main__":
    main()
