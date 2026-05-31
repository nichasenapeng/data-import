[README.md](https://github.com/user-attachments/files/28431985/README.md)
# Japan Broiler Dashboard 🐔

Interactive single-page dashboard ติดตามข้อมูลตลาดไก่ระหว่าง **บราซิล → ญี่ปุ่น**
ครอบคลุม import volumes, stock levels, export breakdown และคาดการณ์ราคาปี 2569

**ไฟล์หลัก:** [`japan_broiler_v2.html`](japan_broiler_v2.html) (single-file — ไม่ต้อง build, ไม่มี backend)
**Data cutoff:** เมษายน 2026 (เม.ย. 2569)

---

## 🚀 วิธีใช้งาน

เปิดไฟล์ `japan_broiler_v2.html` ด้วยเบราว์เซอร์ได้เลย — ไม่ต้องติดตั้งอะไร

```bash
open japan_broiler_v2.html        # macOS
```

ข้อมูลทั้งหมด hardcode อยู่ใน JavaScript และโหลด Chart.js + Google Fonts ผ่าน CDN
(ต้องต่ออินเทอร์เน็ตเพื่อโหลด chart library และ fonts)

---

## 📊 7 แท็บ

| Tab | หัวข้อ | เนื้อหา |
|-----|--------|---------|
| 1 | ภาพรวม Import ญี่ปุ่น | ยอด import 2024–2026 แยก USA / Thailand / Brazil / Other + Heatmap %YoY |
| 2 | Total Stock Japan | สต็อกรวม (Import + Domestic) พร้อมเส้น safety 130,000 MT |
| 3 | Port Brazil → Japan | Port quantity รายปี/รายเดือน + รองรับ CSV upload สดที่ header |
| 4 | Brazil Raw Meat Exports | ส่งออกไป Japan / China / UAE / S.Korea |
| 5 | Total Qty Brazil Export | ยอดส่งออกรวม + Brazil global share ~35% |
| 6 | Brazil Export (APR'26) | Top 15 importers, Japan product breakdown, shipping by state heatmap |
| 7 | คาดการณ์ราคา | ราคาจริง ม.ค.–เม.ย. 2569 + คาดการณ์ พ.ค.–ธ.ค. + risk factors |

> หมายเหตุ: ลำดับใน nav (t1→t5→t2→t3→t4→t6→t7) ต่างจากลำดับใน HTML — ไม่กระทบการทำงาน

---

## 📂 ไฟล์ในโปรเจกต์

| ไฟล์ | คำอธิบาย |
|------|----------|
| `japan_broiler_v2.html` | ตัว dashboard ทั้งหมด (HTML + CSS + JS + data) |
| `handoff.md` | เอกสารส่งต่องาน — แหล่งข้อมูล, โครงสร้างโค้ด, วิธี update |
| `IMG_7939.jpeg`, `image-1780197382543.png` | ภาพอ้างอิง/ภาพประกอบ |

---

## 🔄 การอัปเดตข้อมูล (ทุกวันที่ 18 ของเดือน)

### วิธีที่ 1 — ปุ่มอัปเดต CSV (วิธีหลัก, Tab 1–5) ✅

ฝ่ายขายส่ง **CSV** มา → กดปุ่ม **"อัปเดต CSV"** ที่มุมขวาบน → เลือกไฟล์ → กราฟอัปเดตทันที
(ทำงานในเบราว์เซอร์ล้วน ๆ ไม่อัปโหลดไป server ที่ไหน)

ไฟล์ CSV: แถวแรกเป็น header, ต้องมีคอลัมน์ `month` (jan/feb/…) ระบบจะดูชื่อคอลัมน์แล้วอัปเดต tab ที่ตรงให้เอง:

| Format | คอลัมน์ที่ใช้ตัดสิน | อัปเดต Tab |
|--------|--------------------|-----------|
| A — Import Japan | `bra_*`, `thai_*`, `usa_*`, `oth_*` | 1 |
| B — Port Brazil | `port_2024/25/26` | 3 |
| C — Raw Meat | `japan_*`, `china_*`, `uae_*`, `saudi_*` | 4 |
| D — Total Qty | `qty_2024/25/26` | 5 |
| E — Stock Japan | `tot_/imp_/dom_2025/26` | 2 |

> รายละเอียดชื่อคอลัมน์ครบ ๆ ดูหัวข้อ 7.1 ใน [handoff.md](handoff.md)

### วิธีที่ 2 — แก้ JavaScript (เฉพาะ Tab 6 / 7 ที่ยังไม่รองรับ CSV)

| Variable | Tab | ความหมาย |
|----------|-----|----------|
| `EX_APR26`, `EX_ACC26` | 6 | Brazil export APR 2026 & accumulated (KG) |
| `JPROD_KG` | 6 | Japan product breakdown (KG) |
| `STATE_DATA`, `STATE_TOTALS` | 6 | Shipping by state (Tons) |
| `JP_BLK`, `JP_COOK` | 7 | ราคา Japan BLK / Cooked รายเดือน |
| `ACTUAL_UPTO` | 7 | จำนวนเดือนที่เป็นข้อมูลจริง (ปัจจุบัน = 4) |
| `BR_WOG` | 7 | Brazil WOG Frozen USD/กก. |

**แหล่งข้อมูล:** มาจาก **CSV/Excel ที่ฝ่ายขายอัปเดตและส่งมาให้ทุกเดือน**
ไฟล์ต้นทาง (`Data_ImportExport_20252026.xlsx`, `BR_Raw_Chicken_Exports_APRIL26.xlsx`, `Packer1_256914Jan2026.pdf`)
> ⚠️ ยัง**ไม่ได้เก็บไว้ในโฟลเดอร์นี้** — ต้องขอไฟล์ล่าสุดจากฝ่ายขายก่อน update ทุกครั้ง
> แนะนำให้สร้างโฟลเดอร์ `data/` เก็บไฟล์ต้นทางแต่ละงวดไว้ย้อนรอย

รายละเอียด mapping sheet → tab ดูที่ [handoff.md](handoff.md)

---

## 🎨 Tech / Design

- **Stack:** Single-file HTML · Chart.js (CDN) · No backend / No build step
- **Fonts:** Kanit, Sarabun (ข้อความ), Bebas Neue (ตัวเลข) — Google Fonts
- **Theme:** Misty blue fog gradient, frosted-glass cards (`backdrop-filter: blur`)
- **Primary:** `#2563a8` · **Navy:** `#1a3a5c`
- **Lazy init:** chart ของแต่ละแท็บ render เมื่อกดเข้าแท็บครั้งแรก → โหลดหน้าเร็ว

---

## ⚠️ ข้อควรรู้

- ราคาจริงใน Tab 7 มีถึง **เม.ย. 2569** เท่านั้น ที่เหลือเป็นการคาดการณ์ — ต้อง update เมื่อมีข้อมูลใหม่
- Japan Cooked เดือน เม.ย. ใช้ค่า interpolated (Excel ไม่มีค่า Souiku)
- ไม่มี API / database — ข้อมูลทั้งหมดอยู่ในไฟล์ HTML

📄 รายละเอียดเชิงลึกทั้งหมดดูที่ **[handoff.md](handoff.md)**
