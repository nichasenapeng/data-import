# Handoff Document — Japan Broiler Dashboard
**File:** `japan_broiler_v2.html`  
**Live:** https://nichasenapeng.github.io/data-import/ (GitHub Pages)  
**Access:** มี login gate (password 6 หลัก) — ดูหัวข้อ 9  
**Last Updated:** 31 May 2026  
**Data Cutoff:** May 2026 (ราคาจริง Tab 7 ถึง พ.ค. · ข้อมูล Import/Stock/Brazil Export ถึง เม.ย.)  
**Stack:** Single-file HTML · Chart.js 4.4.1 (cdnjs) · Google Fonts (IBM Plex Sans Thai, IBM Plex Sans)

---

## 1. Project Overview

Interactive single-page dashboard สำหรับติดตามข้อมูลตลาดไก่ระหว่างบราซิลและญี่ปุ่น  
ประกอบด้วย 7 แท็บ ครอบคลุมทั้ง import volumes, stock levels, export breakdown และคาดการณ์ราคาปี 2569

---

## 2. แหล่งข้อมูล (Data Sources)

> ✅ **อัปเดต (มิ.ย. 2026): ดึงข้อมูลสดจาก Google Sheet แบบ real-time แล้ว**
> Dashboard ดึงข้อมูล Tab 1–5 + ราคา Tab 7 (BLK/Souiku) สดจาก Google Sheet
> **"Data Import-Export 2025"** ทุกครั้งที่เปิดหน้า (และกดปุ่ม 🔄 "ดึงจาก Google Sheet" เพื่อรีเฟรช)
> — ฝ่ายขายแค่พิมพ์ตัวเลขลงชีตตามปกติ ไม่ต้องส่ง CSV มาให้แล้ว (ดูหัวข้อ 7.0)
> - Sheet ID: `1l33IeG1TGbGDglXOWMnhOt23hefHb0KrQvyADgTweTk` (ตัวแปร `GS_ID` ในไฟล์)
> - **เงื่อนไข:** ชีตต้องตั้งแชร์เป็น **"ทุกคนที่มีลิงก์ดูได้" (Anyone with the link · Viewer)**
>   มิฉะนั้น browser จะดึงไม่ได้ (จะขึ้น error สีแดง และคงข้อมูลเดิมไว้)
> - ปุ่ม "อัปเดต CSV" เดิมถูกเอาออกแล้ว (ฟังก์ชัน `loadCSV()`/`parseCSV()` ยังอยู่ในโค้ด — `gsLoad()` เรียกใช้ `parseCSV()` ภายใน)
>
> ⚠️ **ที่ยัง hardcode (ไม่ได้อยู่ในชีตนี้):** Tab 6 ทั้งหมด (Top-15, Japan Product, Heatmap รายรัฐ — มาจาก `BR_Raw_Chicken_Exports_*.xlsx`) และ Tab 7 ส่วน Karaage/SBB/BB/ค่าพยากรณ์ (มาจาก Packer PDF) — ยังต้องแก้ JS เหมือนเดิม
> ตาราง mapping ด้านล่างคือ "ที่มาของตัวเลข"

| ไฟล์ | Sheet / Section | นำไปใช้ใน Tab |
|------|----------------|--------------|
| `Data_ImportExport_20252026.xlsx` | `Import-Export` rows 4–17 | Tab 1 — Import volumes (USA, Thai, BRA, Other) ปี 2022–2026 |
| `Data_ImportExport_20252026.xlsx` | `Import-Export` rows 311–338 | Tab 7 — ราคาจริง BLK/Cooked ม.ค.–เม.ย. 2026 |
| `Data_ImportExport_20252026.xlsx` | `Import-Export` rows 348–350 | Tab 7 — AVE.2024/2025/2026 (Brazil BL 200g = 3,575 USD/ตัน) |
| `Data_ImportExport_20252026.xlsx` | `Import-Export` rows 237–290+ | Tab 5 — Total Stock Japan (Import + Domestic) |
| `Data_ImportExport_20252026.xlsx` | `จำนวนแต่ละรัฐของ Brazil` | Tab 2 — Port Brazil → Japan by State |
| `Data_ImportExport_20252026.xlsx` | `CURRENCY` | (ref) อัตราแลกเปลี่ยนปัจจุบัน |
| `BR_Raw_Chicken_Exports_APRIL26.xlsx` | `APR'26 X YEAR (Accumulated)` | Tab 6 — Top 15 Importers APR 2026 vs Y2026 |
| `BR_Raw_Chicken_Exports_APRIL26.xlsx` | `APR'26 Exports By Product` | Tab 6 — Japan Product Breakdown |
| `BR_Raw_Chicken_Exports_APRIL26.xlsx` | `Japan by State (SEP'25~APR'26)` | Tab 6 — Shipping by State heatmap |
| `Packer1_256914Jan2026.pdf` … `Packer8_256913May2026.pdf` | รายงานการประชุม Packer 1–8/2569 (ม.ค.–พ.ค. 2569) | Tab 7 — ราคาตลาด BLK/Karaage/SBB รายงวด, ปัจจัยเสี่ยง, ค่าเงิน, ค่าระวาง Reefer |

> 📌 **หมายเหตุไฟล์ Packer PDF:** ไฟล์ที่ฝ่ายขายส่งมาเป็นนามสกุล `.pdf` แต่จริง ๆ เป็น **ZIP ของภาพถ่ายสไลด์ (.jpeg) + ไฟล์ OCR text (.txt) ต่องวด** — อ่านราคาได้จากไฟล์ `.txt` ที่แนบมาในแต่ละภาพ (ค้นคำว่า `BLK ของไทย`, `คาราเกะ`, `SBB หมักเกลือ`, `Reefer`, `อัตราแลกเปลี่ยน`)

---

## 3. โครงสร้าง Tab

### Tab 1 — ภาพรวม Import ญี่ปุ่น
- **KPI:** ยอด Import 2024/2025/2026 YTD แยก USA / Thailand / Brazil / Other
- **Charts:** ยอดรวมรายปี, Heatmap %YoY รายเดือน, รายเดือนแยกประเทศ
- **ปุ่ม Year:** เปลี่ยน Heatmap ระหว่าง 2023/2024/2025

### Tab 2 — Total Stock Japan *(ย้ายมาจากตำแหน่งที่ 5)*
- **KPI:** Total Stock ม.ค. 2025 / ธ.ค. 2025 / ม.ค. 2026 / ก.พ. 2026
- **Safety Line:** เส้นอ้างอิง 130,000 MT (เส้นแบ่ง stock เพียงพอ/ขาด)
- **Charts:** เฉลี่ยรายปี, รายเดือน 2025 vs 2026 พร้อมเส้น safety

### Tab 3 — Port Brazil → Japan
- **KPI:** Port Qty รวม 2024 / 2025 / 2026 JAN–APR
- **Charts:** ยอดรวมรายปี, Heatmap %YoY, รายเดือน 3 ปีเปรียบเทียบ

### Tab 4 — Brazil Raw Meat Exports
- **KPI:** ยอดส่งออกไป Japan / China / UAE / S.Korea ปี 2025
- **Charts:** ยอดรวมรายปีแยกตลาด, Heatmap %YoY (Japan/China/UAE), รายเดือน

### Tab 5 — Total Qty Brazil Export
- **KPI:** Total Export 2024/2025/2026 JAN–APR, Brazil Global Share ~35%
- **Charts:** ยอดรวมรายปี, รายเดือน 3 ปีเปรียบเทียบ

### Tab 6 — Brazil Export *(ข้อมูลจาก BR_Raw_Chicken_Exports_APRIL26.xlsx)*
- **KPI:** APR 2026 Total / Y2026 Accum. / Japan APR / Japan Accum.
- **Charts:**
  - Top 15 Importers — Grouped bar APR 2026 vs Y2026 (หน่วย: thousand MT)
  - Japan Product Breakdown — Horizontal bar แยก product (Boneless Thighs ครอง 37,828 MT)
- **Table:** Shipping Volume by State (SEP 2025–APR 2026) แบบ Heatmap intensity

### Tab 7 — คาดการณ์ราคา *(ข้อมูลจาก Excel + Packer PDF 1–8/2569)*
- **ราคาจริง 🔵:** ม.ค.–พ.ค. 2026 (ม.ค.–เม.ย. Japan BLK/Cooked จาก Excel · พ.ค. จากราคาตลาดที่ประชุม Packer 8 — 13 พ.ค.)
- **คาดการณ์ 📊:** มิ.ย.–ธ.ค. 2026 (อ้างอิงฤดูกาล + คำขอปรับราคา Q3 จากต้นทุนค่าระวาง/Packaging)
- **Q-Cards:** Q1–Q2 = ราคาจริง · Q3–Q4 = คาดการณ์
- **Main Chart:** Japan BLK / Japan Karaage (ปรุงสุก) / EU SBB Salted — เส้นทึบ=จริง (ม.ค.–พ.ค.), เส้นประ=คาดการณ์
- **Price Table:** 7 แถว × 12 เดือน (highlight น้ำเงิน = ข้อมูลจริง ม.ค.–พ.ค.) — เพิ่มแถว Japan Karaage แยกจาก Cooked/Souiku
- **Brazil WOG Chart:** Trend + Corn price dual-axis (ข้อมูลจริงถึง เม.ย. — ใช้ `WOG_UPTO=4`)
- **Risk Factors:** 7 ปัจจัยจาก Packer Meeting 8/2569 (พ.ค.)

---

## 4. ราคาจริงในระบบ (Tab 7)

ดึงจาก Excel `Import-Export` sheet — Price(Normal) = BLK, Price(Souiku) = Cooked · ราคาตลาด BLK/Karaage จากรายงานการประชุม Packer (PDF)

| เดือน | Japan BLK (USD/ตัน) | Japan Cooked/Souiku (USD/ตัน) |
|-------|---------------------|----------------------|
| ม.ค. 2569 | **3,300** | **3,450** |
| ก.พ. 2569 | **3,400** | **3,550** |
| มี.ค. 2569 | **3,600** | **3,750** |
| เม.ย. 2569 | **4,000** | 3,900 (interpolate) |
| พ.ค. 2569 | **4,050** (ราคาตลาด Packer 8 = 4,000–4,100) | — |
| AVE.2024 | 2,729 | 2,879 |
| AVE.2025 | 2,785 | 2,935 |
| AVE.2026 (ม.ค.–เม.ย.) | **3,575** | **3,583** |

**ราคาตลาด BLK (สด) รายงวด Packer** — ม.ค. 2,900–3,000 → ก.พ. 3,200–3,400 → มี.ค. 3,400–3,600 → เม.ย. 3,600–3,800 → **พ.ค. 4,000–4,100** USD/ตัน  
**Japan Karaage (ปรุงสุก พรีเมียม)** — ม.ค. 4,700–5,200 → ก.พ.–พ.ค. คงที่ **4,800–5,300** USD/ตัน (คนละสเปกกับ Souiku/Excel ~3,500–3,900)  
**Japan BB Fresh** (23 เม.ย. 2569) = 1,950–2,100 USD/ตัน (midpoint 2,025)

---

## 5. Design System

| Element | Value |
|---------|-------|
| Font หลัก (`--font`) | IBM Plex Sans Thai (Google Fonts) — ข้อความ |
| Font ตัวเลข (`--num`) | IBM Plex Sans (Google Fonts) — ตัวเลข/KPI |
| พื้นหลัง | Misty blue fog gradient — `#c8dff4` → `#f8fbff` (diagonal + radial layered) |
| Card background | `rgba(255,255,255,.82)` + `backdrop-filter: blur(8px)` |
| Shadow | `0 6px 24px rgba(26,58,92,.22), 0 2px 8px rgba(26,58,92,.14)` |
| Nav border | `border-right: 1px solid rgba(37,99,168,.12)` แต่ละแท็บ |
| Active tab | `border-bottom: 3px solid var(--blue)` + `background: rgba(37,99,168,.06)` |
| Primary blue | `#2563a8` |
| Navy | `#1a3a5c` |
| Text muted | `#5a7090` |

---

## 6. โครงสร้างโค้ด

```
japan_broiler_v2.html
├── <head>  Google Fonts (IBM Plex Sans Thai, IBM Plex Sans via fonts.googleapis.com)
│           Chart.js CDN
├── <style> CSS Variables + Layout + Component styles (~140 lines)
├── <body>
│   ├── .hdr  — Header bar (sticky)
│   ├── .nav  — Tab navigation (t1–t7)
│   ├── #t1   — ภาพรวม Import ญี่ปุ่น
│   ├── #t7   — คาดการณ์ราคา  ← แทรกก่อน t2 ในลำดับ HTML
│   ├── #t2   — Port Brazil → Japan
│   ├── #t3   — Brazil Raw Meat Exports
│   ├── #t4   — Total Qty Brazil Export
│   ├── #t5   — Total Stock Japan
│   └── #t6   — Brazil Export
└── <script>
    ├── var _charts = {}           — Chart instance registry
    ├── var _tabInited = {}        — Lazy init flags (t1–t7)
    ├── function goTab(id)         — Tab switcher
    ├── function hmTog()           — Heatmap accordion toggle
    ├── function _lblPlugin        — Chart.js bar label plugin
    ├── function _iT1()–_iT7()    — Tab initializers (lazy, called once)
    ├── DATA variables             — Hardcoded per-tab (EX_TOP15, STATE_DATA, etc.)
    ├── CSV upload logic           — updateFromCSV(), csvMsg()
    └── BOOT: _tabInited['t1']=true; _iT1();
```

**หมายเหตุลำดับ HTML vs Nav:**  
Nav ลำดับ: t1 → t5 → t2 → t3 → t4 → t6 → t7  
HTML body ลำดับ: t1 → t7 → t2 → t3 → t4 → t5 → t6  
(ไม่กระทบการทำงาน — `goTab()` ใช้ CSS `display:none/block`)

---

## 7. การอัปเดตข้อมูล

มี 2 ทาง: **(7.0)** Google Sheet — วิธีหลัก (real-time) · **(7.2)** แก้ JavaScript variable — สำหรับ Tab 6 และส่วน Packer ของ Tab 7
(ปุ่ม "อัปเดต CSV" หัวข้อ 7.1 เดิมถูกเอาออกจากหน้าแล้ว — โค้ด `loadCSV()`/`parseCSV()` ยังอยู่และถูกใช้ภายในโดย `gsLoad()`)

### 7.0 อัปเดตผ่าน Google Sheet (วิธีหลัก — real-time)

ฝ่ายขายพิมพ์ตัวเลขลงชีต **"Data Import-Export 2025"** ตามตำแหน่งเดิมที่ใช้อยู่ → dashboard ดึงสดเมื่อเปิดหน้า/กดปุ่ม 🔄
ไม่ต้องส่งไฟล์ ไม่ต้องแก้โค้ด ครอบคลุม **Tab 1–5 + ราคา BLK/Souiku ของ Tab 7**

| Tab | ตารางในชีต (แท็บ Import-Export) ที่ระบบอ่าน — anchor ด้วย "ข้อความหัวตาราง" |
|-----|------------------------------------------------------------------|
| Tab 1 | ตารางใหญ่หัว `USA 2022 … OTHER 2026` (12 เดือน) |
| Tab 2 (Stock) | `TOTAL STOCK JAPAN 2025` / `… 2026` (คอลัมน์ Total/Import/Domestic) |
| Tab 3 (Port) | `Port Brazil to Japan 2024/2025/2026` (เริ่มอ่านที่แถวเดือน JAN — กันป้ายเดือนที่พิมพ์ผิดปี) |
| Tab 4 (Raw) | `RAW MEAT EXPORTS 2024/2025/2026` (CHINA/JAPAN/UAE/Saudi/S.Korea) |
| Tab 5 (Qty) | `Total Quantity Brazilian Export 2024/2025/2026` |
| Tab 7 (ราคา) | ตาราง SUNFOOD price หัว `Price (Souiku)` → BLK=Price(Normal), Cooked=Price(Souiku) ปี 2026 |

> 🔑 **กลไก:** อ่าน CSV จาก endpoint `…/export?format=csv&gid=0` (gid=0 = แท็บ Import-Export) แล้ว parse โดย **อ้างอิงข้อความหัวตาราง** ไม่ใช่เลขแถวตายตัว → ทนต่อการที่ชีตยาวขึ้นเรื่อย ๆ ทุกเดือน
> โค้ดอยู่ในฟังก์ชัน `gsLoad()` / `_gsApply()` แล้ว reuse `parseCSV()` เดิมสำหรับ Tab 1–5
> ⚠️ ถ้าฝ่ายขาย **เปลี่ยนข้อความหัวตาราง / สลับคอลัมน์** ในชีต ต้องแก้ marker ใน `_gsApply()` ตาม



| Variable | Tab | คำอธิบาย |
|----------|-----|----------|
| `EX_APR26`, `EX_ACC26` | T6 | Brazil export APR 2026 & accumulated (หน่วย KG) |
| `JPROD_KG` | T6 | Japan product breakdown (KG) |
| `STATE_DATA`, `STATE_TOTALS` | T6 | Shipping by state (Tons) |
| `JP_BLK`, `JP_KARA` | T7 | ราคา Japan BLK / Karaage (ปรุงสุก) รายเดือน — `JP_KARA` ใช้เป็นเส้นเขียวในกราฟหลัก |
| `JP_COOK` | T7 | Japan Cooked/Souiku (Excel) — แสดงเป็นแถวในตาราง ไม่อยู่ในกราฟ |
| `EU_SBB`, `EU_DICE` | T7 | EU/UK SBB Salted / Steam Dice รายเดือน (จาก Packer) |
| `ACTUAL_UPTO` | T7 | จำนวนเดือนที่เป็นข้อมูลจริง (**ปัจจุบัน = 5** : ม.ค.–พ.ค.) |
| `WOG_UPTO` | T7 | จำนวนเดือนจริงของ Brazil WOG แยกต่างหาก (**= 4** : ม.ค.–เม.ย.) |
| `BR_WOG`, `BR_BL` | T7 | Brazil WOG Frozen (USD/กก.) · Brazil BL 200g (USD/ตัน) |

### 7.1 อัปเดตผ่านปุ่ม CSV (วิธีหลัก — ไม่ต้องแก้โค้ด)

ฝ่ายขายส่ง **CSV** มาให้ → กดปุ่ม **"อัปเดต CSV"** ที่ header → เลือกไฟล์ → ระบบ parse และ re-render กราฟทันที
(ฟังก์ชัน `loadCSV()` → `parseCSV()` ในไฟล์ HTML; อ่านด้วย `FileReader` แบบ UTF-8, ไม่ส่งข้อมูลออกที่ไหน)

**กติกาไฟล์:** แถวแรกต้องเป็น header, ต้องมีคอลัมน์ `month` (jan/feb/…), ค่าที่ว่างจะถูกข้าม
ระบบดูจากชื่อคอลัมน์ว่าตรงกับ format ไหน แล้วอัปเดต tab ที่เกี่ยวข้องอัตโนมัติ (ใส่หลาย format ในไฟล์เดียวได้)

| Format | คอลัมน์ที่ trigger | คอลัมน์ข้อมูล | อัปเดต Tab |
|--------|-------------------|---------------|-----------|
| **A** Import Japan | `bra_*` | `month`, `bra_2022..2026`, `thai_2022..2026`, `usa_2022..2026`, `oth_2022..2026` | Tab 1 |
| **B** Port Brazil | `port_*` | `month`, `port_2024`, `port_2025`, `port_2026` | Tab 3 |
| **C** Raw Meat | `japan_*` หรือ `china_*` | `month`, `japan_2024..2026`, `china_2024..2026`, `uae_2024..2026`, `saudi_2024..2026` | Tab 4 |
| **D** Total Qty | `qty_*` | `month`, `qty_2024`, `qty_2025`, `qty_2026` | Tab 5 |
| **E** Stock Japan | `tot_2025` หรือ `imp_2025` | `month`, `tot_2025/imp_2025/dom_2025`, `tot_2026/imp_2026/dom_2026` | Tab 2 |

ตัวอย่าง header Format A: `month,bra_2022,bra_2023,bra_2024,bra_2025,bra_2026,thai_2022,...`
ถ้าไม่พบคอลัมน์ที่รู้จักจะขึ้น error "ไม่พบ column ที่รู้จัก"

> ⚠️ **Tab 6 (Brazil Export) และ Tab 7 (คาดการณ์ราคา) ยังไม่รองรับ CSV upload** — ต้องแก้ตัวแปรใน JS ตามหัวข้อ 7.2

### 7.2 อัปเดตด้วยการแก้โค้ด (เฉพาะ Tab 6 / Tab 7)

ค้นหา JavaScript variable ในไฟล์แล้วแก้ตรง:

### 7.3 ข้อมูลที่ต้อง update ทุกเดือน (วันที่ 18)

1. **Import Japan** — CSV Format A → Tab 1
2. **Total Stock** — CSV Format E → Tab 2
3. **Brazil Export** — แก้ JS (`EX_APR26`, `EX_ACC26`, `JPROD_KG`, `STATE_DATA`) → Tab 6
4. **ราคา BLK/Karaage/SBB** — แก้ JS (`JP_BLK`, `JP_KARA`, `JP_COOK`, `EU_SBB`, `EU_DICE`, `ACTUAL_UPTO`) → Tab 7 · อ่านราคาจาก `.txt` ในไฟล์ Packer PDF งวดล่าสุด

---

## 8. Known Issues / Notes

- **Tab 7 ราคาจริง 5 เดือน** (ม.ค.–พ.ค. 2569) — ม.ค.–เม.ย. จาก Excel (settled), พ.ค. ใช้ราคาตลาดจาก Packer Meeting 8 (4,000–4,100 → midpoint 4,050) เพราะยังไม่มีราคา settled ใน Excel งวด พ.ค. · ระบุที่มาในเชิงอรรถตารางแล้ว
- **Japan Karaage ≠ Souiku** — กราฟหลักใช้เส้น Karaage (PDF ~4,800–5,300) ส่วน Souiku/Excel (~3,500–3,900) เป็นคนละสเปกสินค้า เก็บเป็นแถวแยกในตาราง
- **Japan Cooked/Souiku เม.ย.** — Excel ไม่มีค่า Souiku สำหรับเม.ย. 2026 จึงใช้ interpolated 3,900 · พ.ค. เป็น `null` (แสดง "—")
- **CSV Upload feature** — ปุ่ม "อัปเดต CSV" ที่ header รองรับ **5 รูปแบบ (A–E)** อัปเดต Tab 1–5 แบบ real-time (ดูหัวข้อ 7.1) — **Tab 6 และ Tab 7 ยังไม่รองรับ CSV** ต้องแก้ใน JavaScript เอง
- **Lazy Tab Init** — Chart จะ render เมื่อกดแท็บครั้งแรก ทำให้โหลดหน้าเร็ว
- **No external API** — ข้อมูลทั้งหมด hardcode ใน JavaScript ไม่มี backend

---

## 9. Login Gate (ระบบรหัสผ่าน)

หน้า dashboard มี **login gate** บังก่อนเข้าดูข้อมูล (เพิ่มเข้ามาเพื่อจำกัดการเข้าถึง "ข้อมูลภายใน")

| ส่วน | รายละเอียด |
|------|-----------|
| UI | `#login-gate` (บรรทัด ~169–203) — การ์ดกรอกรหัส 6 หลัก, ปุ่ม "เข้าสู่ระบบ" |
| Logic | `tryLogin()` / `_h()` / `_PWH` (บรรทัด ~619–623) |
| วิธีตรวจ | hash ค่าที่กรอกด้วย `_h()` แล้วเทียบกับ `_PWH` (ค่า hash คงที่ฝังในไฟล์) |
| จำสถานะ | `sessionStorage['jbd_auth']='1'` — ผ่านแล้วไม่ต้องกรอกซ้ำใน session เดิม (ปิดแท็บ/เปิดใหม่ = กรอกใหม่) |

### วิธีเปลี่ยนรหัสผ่าน

1. คำนวณ hash ใหม่: เปิด console แล้วเรียก `_h('รหัสใหม่')`
2. นำค่าที่ได้ไปแทนใน `var _PWH=...;` (บรรทัด ~620)
3. รหัสปัจจุบันเป็นตัวเลข 6 หลัก (input เป็น `inputmode="numeric"`)

> ⚠️ **ข้อจำกัดด้านความปลอดภัย:** เป็น **client-side password** — hash และ logic ทั้งหมดอยู่ในไฟล์ HTML
> ใครเปิด source/console ก็ bypass ได้ เหมาะกับ "กันคนทั่วไป" เท่านั้น ไม่ใช่การป้องกันระดับ server
> ถ้าข้อมูลอ่อนไหวมาก ควรย้ายไปใช้ auth ฝั่ง server / repo แบบ private

---

## 10. Key Market Insights (จาก Packer Meeting 8/2569 — 13 พ.ค. 2569)

| ตลาด | ราคา (พ.ค. 2569) | แนวโน้ม |
|------|-------------|--------|
| Japan BLK (Fresh) | 4,000–4,100 USD/ตัน | ▲ Demand แข็ง บราซิลส่งญี่ปุ่นลดลง · ปมจีน-ไต้หวันโอนคำสั่งมาไทย |
| Japan Karaage (ปรุงสุก) | 4,800–5,300 USD/ตัน | ▲ นักท่องเที่ยวหนุน Food Service · จีนแข่งราคาถูก |
| EU/UK SBB Salted | 3,700–3,900 USD/ตัน | → ทรงตัว · บราซิลเสนอราคาตํ่ากดดัน |
| EU/UK SBB Steam Dice | 4,400–4,500 USD/ตัน | ▲ ปรับขึ้นจาก Q1 |
| China (ปีกกลาง / ขาซี 30up) | 4,400–4,500 / 4,300–4,400 USD/ตัน | ▲ จีนต้องการนำเข้าจากไทยมากขึ้น |
| Malaysia (BB / น่องติดสะโพก) | 2,400–2,600 / 2,700–2,800 USD/ตัน | ▲ Demand ดีขึ้นต่อเนื่อง |
| Reefer (Japan) | 20ft = 800 / 40ft = 1,000 USD | — |
| Reefer (EU/UK) | 20ft = 3,700 / 40ft = 4,500 USD | ▲ สูงขึ้นจากสงครามตะวันออกกลาง |
| USD/THB · Yuan · Real | 32.37 · 6.80 · 4.90 (12 พ.ค. 2569) | บาทอ่อนเล็กน้อย หนุนผู้ส่งออก |

**ปัจจัยสำคัญที่ต้องติดตาม:**
- **สงครามตะวันออกกลาง (อิหร่าน/อิสราเอล)** — ดันค่าเฟด & Packaging ผู้ส่งออกไทยขอปรับราคา Q3/69 (ผู้ซื้อส่วนใหญ่ยอมรับ) · ส่งออกตะวันออกกลาง −18.5%
- **FTA ไทย–EU** — เจรจารอบ 9 มิ.ย. 69 ที่บรัสเซลส์ ตั้งเป้าปิดดีลภายในปี 69 · ไทยขอยกเลิกโควต้า/ภาษี 0% · เวียดนาม-เกาหลีใต้เปิดช่องไก่แปรรูป
- **ไข้หวัดนก H5N1** — เคสชายแดนไทย-กัมพูชา (29 มี.ค. 69) ยกระดับคัดกรอง · บราซิลต่ออายุภาวะฉุกเฉินอีก 180 วัน
- **Saudi-GAP** — เลื่อนบังคับใช้ไปอีก 1 ปี มีผล 17 มี.ค. 2570
