# HANDOFF — Japan Broiler Dashboard (session ล่าสุด)
อัปเดต: 21 ก.ย. 2026 · ไฟล์หลัก: `data-import-main/index.html` · **backup: `index_backup_20260902_2107.html`**

> อ่านไฟล์นี้ก่อนแก้ต่อ · ไฟล์เดิม `handoff.md`/`README.md` ยังใช้ได้ (โครงพื้นฐาน) · ไฟล์นี้ = สิ่งที่ทำเพิ่ม session นี้

---

## 📌 สถานะปัจจุบัน — Dashboard 10 แท็บ
Single-file HTML · Chart.js 4.4.1 (CDN) · **login gate** (pw hash `_PWH=552165811300396`) · ดึงสด Google Sheet ทุกครั้งที่เปิด (`gsLoad`) · lazy-init `_iT1.._iT10`

| # | แท็บ | ที่มาข้อมูล | หมายเหตุ |
|---|---|---|---|
| 1 | ภาพรวม Import ญี่ปุ่น | Google Sheet (live) | **default ปุ่มปี = 2026** (แก้ session นี้) |
| 2 | Total Stock Japan | Google Sheet (live) | + **การ์ด supply-flow forecast** (ใหม่) |
| 3 | Port Brazil → Japan | Google Sheet (live) | + ปุ่มเลือกปี (setPtY) |
| 4 | Brazil Raw Meat Exports | Google Sheet (live) | |
| 5 | Total Qty Brazil Export | Google Sheet (live) | + ปุ่มเลือกปี (setTqY) |
| 6 | Brazil Export | **Excel `BR Raw Chicken Exports (JULY'26).xlsx`** | hardcode · อัปเดตจาก APR→JULY'26 |
| 7 | คาดการณ์ราคา | Google Sheet (BLK/Souiku) + Packer PDF | ปรับใหญ่ (ดูล่าง) |
| 8 | ในประเทศ vs ส่งออก | โฟลเดอร์ Data Domestic (hardcode) | **ใหม่** `_iT8` |
| 9 | ราคาในประเทศ | โฟลเดอร์ Data Domestic (hardcode) | **ใหม่** `_iT9` — รายเดือน + forecast |
| 10 | ตลาดส่งออกไทย | **Packer PDF** (hardcode) | **ใหม่** `_iT10` — ญี่ปุ่น/EU/UK/มาเลเซีย |

nav มี 10 ปุ่ม · แท็บ 1 ใช้ `class="tab on"`, ที่เหลือ `class="tab"`

---

## 🔧 สิ่งที่ทำ session นี้ (เรียงตามแท็บ)

### Tab 1 — ภาพรวม Import
- **default ปุ่มปีเป็น 2026** : `_iT1` เรียก `setOvY('2026')` · ปุ่ม `ovy-2026` มี class `on` · title default = "รายเดือน — 2026"
- (การ์ด "ไทย→ญี่ปุ่น สด/ปรุงสุก" ที่เคยอยู่ที่นี่ **ย้ายไป Tab 10 แล้ว**)

### Tab 2 — Stock : เพิ่ม 2 อย่าง
1. **เส้นคาดการณ์ Total 2026 + Import 2026** ในกราฟหลัก `c-st-mo` (เส้นทึบ=จริง, เส้นประ=คาด)
   - Total 2026 คาด = วิธีฤดูกาล (2025 shape × ratio) ผ่านทั้งปี
   - Import 2026 คาด = **supply-flow model** (ดูข้อ 2) ถึง ก.ย.
2. **การ์ดใหม่ `c-st-flow`** — คาดการณ์สต๊อกนำเข้าจากยอดบราซิลส่ง (lag 2 เดือน)
   - โมเดล: `สต๊อกนำเข้า = สต๊อกเดิม + ของเข้า(บราซิล port lag2 + non-Brazil ~14,200) − เบิกออก(~50k)`
   - พิสูจน์แล้ว: บราซิลส่งออก(M) ↔ ญี่ปุ่นนำเข้า(M+2) **corr 0.62** · เบิกออกนิ่ง SD~4k
   - `flowBase/flowHi/flowLo` คำนวณใน `_iT5` (ใช้ร่วมทั้งกราฟหลักและการ์ด flow) · `_brFC` = PORT26[4,5,6] (พ.ค.-ก.ค.)
   - ต.ค.+ ยังคาดไม่ได้ (ต้องรอ PORT บราซิล ส.ค.+)

### Tab 6 — Brazil Export : APR'26 → **JULY'26**
- อัปเดตจากไฟล์ `ข้อมูลบราซิล/ข้อมูลบราซิล 2026/BR Raw Chicken Exports (JULY'26).xlsx`
- ตัวแปร: `EX_TOP15_NAMES` (Angola แทน Guinea), `EX_APR26` (ยอดเดือน JUL), `EX_ACC26` (สะสม), `JPROD_LABELS/KG`, `STATE_*` (DEC'25–JUL'26)
- KPI + หัวข้อ + label "APR"→"JUL" ทั้งหมด
- ⚠️ **ชื่อตัวแปรยังเป็น `EX_APR26` แต่เก็บข้อมูล JUL** (ไม่ rename กันพัง) — งวดหน้าแก้ค่าในตัวแปรเดิม

### Tab 7 — คาดการณ์ราคา : ปรับใหญ่
- **ลบ 2 แถว**: Japan Cooked (Souiku), Brazil BL 200g (ตัวแปร `JP_COOK`/`BR_BL` ยังอยู่ แต่ไม่ใช้ในตาราง)
- **ราคาจริง BLK ถึง ก.ย.** : `ACTUAL_UPTO=9` · `JP_BLK` = [...4050,3900,3950,3900, 3880,3860,3840] (ก.ค.-ก.ย.=3900/3950/3900 จริง, ต.ค.-ธ.ค.=คาด)
- **การ์ด offer BL ลูกค้า** (`c-offer`+`tbl-offer`) : ราคาเสนอจริง 14 พ.ค.–2 ก.ย. ร่วง 3,500→2,000-2,100
- **เส้น "ฉากทัศน์อ่อนตัว"** (`AI_BLK`=3700/3600/3550 ต.ค.-ธ.ค.) = ถ้า BLK ตาม offer ลง
- **ราคา Packer อัปเดตถึง Packer 14** : Karaage 5,050 นิ่ง · SBB Salted **ลดเป็น 3,500** (จาก 3,700-3,900) · Steam Dice 4,750
- การ์ด Q1-Q4 + banner + footnote = Packer 1-14

### Tab 8 — ในประเทศ vs ส่งออก (`_iT8`)
- ราคาชิ้นส่วนในประเทศ (leg/bb/live/kron) + กราฟเทียบส่งออกญี่ปุ่น (บาท/กก. = USD/ตัน×เรตบาท÷1000) · ส่วนต่าง ~64%
- ข้อมูล `domestic_parts` hardcode (15 จุด biweekly Jan-Aug)

### Tab 9 — ราคาในประเทศ (`_iT9`)
- **time series รายเดือน** (aggregate จาก 16 รายงานรายสัปดาห์ ม.ค.–ส.ค. เป็น 8 เดือน) — `RAW` (biweekly) → aggregate ใน JS
- 2 กราฟ (ต้นน้ำ: ไก่มีชีวิต/ลูกไก่/ไก่ปลด · ชิ้นส่วน: น่อง/BB/โครง) — **มี forecast เส้นประในกราฟเลย** (ก.ย.-พ.ย.)
- กราฟไก่เป็นรายภูมิภาค 9 เขต — **ปัจจุบัน vs คาดการณ์** (grouped bar)

### Tab 10 — ตลาดส่งออกไทย (`_iT10`) — ใหม่
- 4 การ์ด: ญี่ปุ่น/EU/UK/มาเลเซีย · ไก่สด vs ปรุงสุก รายเดือน 2569
- **ไทยเน้นปรุงสุกมากขึ้น ไก่สดหด −18~20% YoY · UK ~95% ปรุงสุก · มาเลเซียไก่สดล้วน**
- ข้อมูล hardcode (`JPF/JPC/EUF/EUC/UKF/UKC/MYF`) จาก Packer

---

## 📂 แหล่งข้อมูล + วิธีอัปเดต

| ข้อมูล | ที่มา | วิธีอัปเดต |
|---|---|---|
| Tab 1-5 + BLK/Souiku ราคา | Google Sheet `1l33IeG1TGbGDglXOWMnhOt23hefHb0KrQvyADgTweTk` | **ดึงสดเอง** ทุกครั้งที่เปิด (ปุ่ม 🔄) · ค่า hardcode = fallback |
| Tab 6 (Brazil export detail) | Excel `BR Raw Chicken Exports (เดือน'26).xlsx` | แก้ `EX_*/JPROD_*/STATE_*` ใน JS |
| Tab 7 ราคา Karaage/SBB/BB | รายงาน Packer PDF (โฟลเดอร์ `02-ประชุมสมาคม/ประชุมสมาคม 2026/`) | แก้ `JP_KARA/EU_SBB/EU_DICE/JP_BB` |
| Tab 8/9 domestic | โฟลเดอร์ `Data Domestic/2569/*.jpg` (รูปสไลด์) | อ่านรูป → แก้ `domestic_parts`/`RAW` |
| Tab 10 ส่งออกไทย | Packer PDF หน้า "ปริมาณส่งออกไทยไป[ตลาด]" | แก้ arrays ใน `_iT10` |

**Packer PDF** = PDF จริง 37 หน้า · อ่านด้วย `pdfplumber` (มีติดตั้งแล้ว) · ราคาส่งออกอยู่วาระ 3.2 (หน้า ~5,15-18) · **ยอดส่งออกไทยเป็นยอดสะสม YTD** ต้องหักลบเป็นรายเดือน + ใช้ค่าจากฉบับล่าสุดของแต่ละงวด (มี revise)
- Packer 2026 ที่มี: 1,3-12,14 (ขาด 2,13) · ล่าสุด Packer14 (26 ส.ค.)

---

## ⚠️ กับดัก / วิธีทดสอบ (สำคัญ)
- **preview tool / กรอบพรีวิว render ไม่ได้** (ไฟล์นอก project = static snapshot, JS ไม่รัน)
- **ทดสอบจริง = headless Chrome** + bypass login gate:
  ```bash
  # ใส่ก่อน </head>: <style>#login-gate{display:none!important}</style>
  # ใส่ก่อน </body>: <script>window.addEventListener("load",function(){setTimeout(function(){goTab("tN")},500)});</script>
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
    --window-size=1400,2100 --virtual-time-budget=13000 --screenshot=out.png "file://.../test.html"
  ```
  (sessionStorage bypass ไม่ทำงานใน headless — ใช้ CSS ซ่อน gate แทน)
- **`mkBar`/`mkLine` destroy chart เดิมอัตโนมัติ** (เรียกซ้ำ id เดิมได้)
- **`mkBar` ไม่มี stacked** (grouped เท่านั้น) · legend เป็น manual `.leg` div (mkOpts ปิด legend)
- **แก้แล้ว assert ทุกจุด**: ใช้ Python script `sub(old,new,label)` ที่ count==1 กันแก้ผิดตำแหน่ง
- ปีพุทธในไฟล์: 67=2024, 68=2025, **69=2026**

---

## 🚀 งานต่อได้ (ถ้าจะทำ)
1. Packer 15/16 ออก → อัปเดต Tab 7 (ราคา) + Tab 10 (ยอดส่งออก) + Tab 8/9 (domestic ถ้ามีรูปใหม่)
2. เมื่อ Google Sheet มี BLK ต.ค.+ / สต๊อก ก.ค.+ / PORT บราซิล ส.ค.+ → forecast จะยืด anchor เองบางส่วน แต่ค่า Packer/domestic hardcode ต้องแก้มือ
3. Tab 6 งวดใหม่ = เปลี่ยนไฟล์ Excel บราซิล → แก้ `EX_*/JPROD_*/STATE_*`
4. supply-flow forecast (Tab 2) ขยาย ต.ค.-ธ.ค. ได้เมื่อมี PORT บราซิล ส.ค.-ต.ค.

## หมายเหตุผู้ใช้
คนไทย ทำธุรกิจส่งออกไก่ · อธิบายภาษาคนทั่วไป · ชอบดูง่าย/สดใส · ซื่อสัตย์เรื่องขีดจำกัดของการคาดการณ์ (ไม่อ้างแม่นเกินจริง) · ราค��รายเดือน = near-random-walk (คาดการณ์ = ยึดค่าล่าสุด + ทิศทางจากปัจจัย ไม่ใช่โมเดลที่ backtest)

---

## 🔄 อัปเดต 21 ก.ย. 2569 (รอบข้อมูลใหม่ + Packer 15)

### Tab 6 — Brazil Export : JULY'26 → **AUGUST'26**
ไฟล์ `BR Raw Chicken Exports (AUGUST'26).xlsx` (โฟลเดอร์ `ข้อมูลบราซิล/ข้อมูลบราซิล 2026/`)
- KPI: ส่งออกรวม ส.ค. **451,928 MT / US$891M** · สะสม ม.ค.–ส.ค. **3,582,600 MT / US$6,758M** (pace +14.8% vs 2025)
- ญี่ปุ่น ส.ค. **41,182 MT / US$107.0M** (+36.7% vs ส.ค.2025 = 30,120 MT) · สะสม **319,401 MT** (+18.4%)
- `EX_TOP15_NAMES` เรียงใหม่ตามยอดสะสม: UAE แซง Saudi · **Kuwait เข้า top15 แทน Chile** · Angola ขึ้นอันดับ 12
- `JPROD_*`: Boneless Thighs 37.5M kg · อันดับ 10 เปลี่ยนจาก Chicken Feet เป็น **Chicken Livers**
- `STATE_MONTHS` เลื่อนเป็น **JAN'26–AUG'26** (ตัด DEC'25 ออก ตามไฟล์ใหม่ที่ให้ JAN~AUG) · SC แซง PR ในเดือน ส.ค.
- ⚠️ ชื่อตัวแปรยังเป็น `EX_APR26` (เก็บค่าเดือน AUG) — ไม่ rename กันพัง เหมือนเดิม

### Tab 7 — ราคา : Packer 15 (9 ก.ย. 2569)
- **SBB หมักเกลือขึ้น** 3,400–3,600 → **3,500–3,800** (mid 3,650) → `EU_SBB` ก.ย.–ธ.ค. = 3,650 · การ์ด Q3/Q4 แก้ตาม
- Karaage 4,800–5,300 นิ่ง · Steam Dice 4,500–5,000 นิ่ง · BLK ตลาด (Packer15) = 3,700–3,800
- `JP_BLK` ก.ย. 3,900 → **3,850** (ค่าจากชีต · ค่าจริงถูก overwrite ด้วย `GS_PRICE` ตอนเปิดหน้าอยู่แล้ว ค่านี้คือ fallback)
- แก้ข้อความที่ค้าง: "Packer 1–14" → 1–15 · subtitle กราฟ/ตาราง "ม.ค.–พ.ค." → "ม.ค.–ก.ย."

### ยังไม่ได้ทำ (รอตัดสินใจ)
- **จุด offer BLK 18 ก.ย.** (ลูกค้าแจ้งว่ามี packer รายอื่นเสนอ ~$3,650 ขณะเราเสนอ $3,900) — ยังไม่ได้ใส่ลงหน้า เพราะเป็นข้อมูลราคาคู่แข่ง/ราคาเสนอของเราบนเว็บสาธารณะ (มี login gate ฝั่ง client เท่านั้น) ถ้าจะใส่ต้องยืนยันก่อน
- Tab 10 (ยอดส่งออกไทย) ยังเป็นตัวเลขจาก Packer 14 — Packer 15 มีตารางใหม่ แต่ยังไม่ได้สกัด
- Tab 8/9 domestic: จุดล่าสุด 2 ก.ย. — ถ้ามีรูปสไลด์ใหม่ค่อยเติม

### Tab 10 — เพิ่มตลาด **ฮ่องกง** (21 ก.ย. 2569)
- `HKF/HKC` รายเดือน ม.ค.–ส.ค. หักลบจากยอดสะสม Table 2 ของ Packer 4,6,7,9,11,12,14,15 (ฉบับล่าสุดของแต่ละงวด)
  - สด: 975 / 806 / 905 / 948 / 915 / 769 / 1,228 / 898 (รวม 7,444)
  - ปรุงสุก: 541 / 423 / 456 / 715 / 592 / 439 / 833 / 702 (รวม 4,701)
- ตรวจวิธีแล้ว: คำนวณ JAPAN ด้วยวิธีเดียวกันได้ตรงกับ `JPF/JPC` เดิมทุกเดือน ✓
- KPI row ของแท็บนี้เป็น 5 ช่อง (`.kpi-row.k5` · มือถือยังเป็น 2 ช่อง) · การ์ดกราฟฮ่องกงเต็มความกว้างใต้ UK/มาเลเซีย
- **ฮ่องกงสวนทางตลาดอื่น**: ไก่สด +13.7% YoY แต่ปรุงสุก −9.7% (ตลาดอื่นไก่สดหด ปรุงสุกโต) · ยอดรวม 12,145 ตัน +3.3%

### 🐛 "Brazil AUG ไม่ขึ้น" — สาเหตุและวิธีแก้ (21 ก.ย. 2569)
**ไม่ใช่บั๊กของหน้าเว็บ** — Tab 1–5 ดึงสดจาก Google Sheet (gid=0) และ**ชีตยังไม่ได้กรอกเดือน ส.ค.** (และ มิ.ย. ก็ขาดบางประเทศ)
- บล็อก `Port Brazil to Japan 2026` : มีถึง JUL · แถว AUG ว่าง
- บล็อก `RAW MEAT EXPORTS 2026` : JUN มีแต่ Japan · AUG ว่างทั้งแถว
**แก้โดยเติมค่า fallback ใน index.html จากไฟล์ Excel บราซิล** (`fillArr` ข้าม null อยู่แล้ว → ค่าจากชีตจะทับให้เองเมื่อกรอกทีหลัง ไม่ต้องมาแก้โค้ดซ้ำ)
- `PORT26[7]=41182` · `RAW_JAPAN/CHINA/UAE/SAUDI` เติม มิ.ย.+ส.ค. (China 50,120/50,988 · UAE 46,022/44,133 · Saudi 33,051/35,195)
- **ยอดรายปีเคยถูกทับด้วยผลรวม "เฉพาะที่ชีตมี"** ทุกครั้งที่ดึงชีต → ย้ายไปคิดหลัง merge จากอาร์เรย์รายเดือนจริง (`_sumMo`) แล้ววาด `_iT3()` ใหม่ · บาร์รายปีของ Port (`c-pt-ann`) ก็เปลี่ยนจากเลขตายตัวเป็นผลรวม `PORT26`
- KPI: PORT 2026 JAN–JUL 278,219 → **JAN–AUG 319,401** (Ave. 39,925)
- ⚠️ **China ไม่สอดคล้อง**: ยอดสะสมในไฟล์ AUG'26 (379,756 ตัน) ต่ำกว่าผลรวมรายเดือน (402,427) ~23k ตัน — น่าจะเป็นการ revise ของ Comex Stat · บาร์รายปีใช้ผลรวมรายเดือนเพื่อให้ตรงกับกราฟรายเดือน
- **ถ้าอยากให้ถูกต้องที่ต้นทาง: กรอกเดือน ส.ค. ลงชีต** (Port 2026 = 41,182 · Raw Meat AUG: China 50,988 / Japan 41,182 / UAE 44,133 / Saudi 35,195 / S.Korea 17,328 · และเติม มิ.ย. ที่ขาด)
