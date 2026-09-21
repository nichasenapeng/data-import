# Handoff — Japan Broiler Import Dashboard (SUNFOOD)

> **อ่านไฟล์นี้ก่อนเริ่มงานทุกครั้ง** · อัปเดตล่าสุด **17 ก.ย. 2569 (2026)**
> ผู้ใช้: คนไทย ทำธุรกิจส่งออกไก่ (ไม่ใช่สาย tech) → อธิบายภาษาคนทั่วไป, ซื่อสัตย์เรื่องข้อจำกัด, ชอบดูง่าย/สดใส, ต้องการความแม่นจริง ไม่ใช่ตัวเลขสวยหลอกตา

---

## 0. สถานะด่วน (อ่านตรงนี้ก่อน)

### ⚠️ มีงานแก้ในเครื่องที่ **ยังไม่ commit / ยังไม่ push**
`index.html` ใน `data-import-main/` มี 3 อย่างที่แก้ + ทดสอบแล้ว แต่ **รอผู้ใช้ตัดสินใจเรื่องรูปก่อน push**:
1. **เปลี่ยนรหัสผ่าน login** → รหัสใหม่ (ผู้ใช้รู้ · ไม่เขียนไว้ที่นี่เพราะ repo เป็น public) · `_PWH=8506142273434222` · ช่องกรอกเปลี่ยน `inputmode="numeric"` → `"text"`, placeholder → "รหัสผ่าน"
2. **เพิ่มจุดข้อมูลในประเทศ 2 ก.ย. 2569** ใน `DP` (แท็บ t8) → รวม 17 จุด
3. (ยังไม่ทำ) **เปลี่ยนรูปพื้นหลังหน้า login** เป็นรูปไก่การ์ตูน — ดูหัวข้อ 11 ข้อ 2

ดู diff: `git diff` · เมื่อพร้อม: ดูหัวข้อ 8 (git)

### 📋 งานค้างเรียงตามลำดับ → หัวข้อ 11

---

## 1. ภาพรวม

| | |
|---|---|
| ไฟล์หลัก (ตัวจริง/deploy) | `Data Import-Export/data-import-main/index.html` (~274 KB, 1,791 บรรทัด) |
| Repo | https://github.com/nichasenapeng/data-import (public · branch `main`) |
| Live | https://nichasenapeng.github.io/data-import/ (GitHub Pages) |
| Stack | HTML ไฟล์เดียว · Chart.js 4.4.1 จาก **cdnjs (ต้องมีเน็ต)** · Google Fonts IBM Plex Sans Thai / IBM Plex Sans |
| ข้อมูลสด | ดึง CSV จาก Google Sheet ตอนเปิดหน้า + ปุ่ม 🔄 "ดึงจาก Google Sheet" (`GS_ID=1l33IeG1TGbGDglXOWMnhOt23hefHb0KrQvyADgTweTk`, gid=0) |
| ป้องกัน | login gate ฝั่ง client (hash) — กันคนทั่วไปเท่านั้น |

> ❗ **อย่าสับสนไฟล์** — session ก่อนหน้าเคยแก้ผิดไฟล์ 2 รอบ ไฟล์ที่ต้องแก้คือ **`data-import-main/index.html` เท่านั้น**
> - `ข้อมูลทำคาดการณ์/dashboard.html` = โปรเจกต์ forecast แยก (build จาก `build_dashboard.py` + `template.html`, มี CLAUDE.md/HANDOFF.md ของตัวเอง) — **ไม่ใช่ตัว deploy**
> - `รายงานสรุป_ราคาไก่ส่งออก.html`, `chicken-dashboard-site/`, `อันเดิม/`, `index_backup_*.html` → ย้ายไป Trash แล้ว (9 ก.ย.)

---

## 2. โครงโฟลเดอร์ในเครื่อง

```
/Users/nicha/Library/Mobile Documents/com~apple~CloudDocs/claude/Data Import-Export/
├── data-import-main/                 ← ⭐ git repo (remote = nichasenapeng/data-import)
│   ├── index.html                    ← ไฟล์ที่แก้
│   ├── handoff.md                    ← ไฟล์นี้
│   ├── README.md, IMG_7939.jpeg, image-1780197382543.png
│   └── .gitignore                    (.DS_Store)
├── Data Import-Export 2025-2026.xlsx ← master data (สำเนาในเครื่อง — เก่ากว่า Google Sheet!)
├── Data Domestic/                    ← รูปรายงานสถานการณ์สมาคมฯ (JPG) แยกปี 2565–2569
│   └── 2569/LINE_ALBUM_packer_YYMMDD_n.jpg
└── ข้อมูลทำคาดการณ์/                  ← โปรเจกต์ forecast (git แยก) + ข้อมูลดิบ
    ├── 02-ประชุมสมาคม (มีทั้งราคาและสถานการณ์)/ประชุมสมาคม 2026/PackerNN_2569(DDMonYYYY).pdf
    ├── ข้อมูลบราซิล/ข้อมูลบราซิล 2026/BR Raw Chicken Exports (MMM'26).xlsx
    └── ข้อมูลญี่ปุ่น/ (01-stock, 03-ราคา + โฟลเดอร์ "ข้อมูลญี่ปุ่น update JUN 2026")
```

---

## 3. แท็บทั้ง 10 (ลำดับบนเมนู)

| id | ชื่อ | ข้อมูล / ที่มา | init |
|---|---|---|---|
| t1 | ภาพรวม Import ญี่ปุ่น | `BRA/THAI/USA/OTH`, `ANN_*` (Google Sheet) · KPI 4 ใบ `#kpi1` | `_iT1` L1040 |
| t5 | Total Stock Japan | `ST_TOT25/26`, `ST_IMP25/26`, `ST_DOM*` (ถึง มิ.ย.26) · `ST_TOT26_FC` · กราฟ `c-st-ann`, `c-st-mo` (+แถบกรอบความไม่แน่นอน `flowHi/flowLo`) · กล่องวิธีคาด+บทวิเคราะห์ | `_iT5` L1070 |
| t2 | Port Brazil → Japan | `PORT24/25/26` | `_iT2` |
| t3 | Brazil Raw Meat Exports | `RAW_JAPAN/CHINA/UAE/SAUDI` (JAPAN 2026 ถึง ก.ค. = 38,255) | `_iT3` |
| t4 | Total Qty Brazil Export | `TQ24/25/26` | `_iT4` |
| t6 | Brazil Export | `EX_APR26`, `EX_ACC26`, `JPROD_KG`, `STATE_*` (hardcode จาก BR xlsx) | `_iT6` L1401 |
| t7 | คาดการณ์ราคา | `JP_BLK`, `JP_KARA`, `JP_COOK`, `JP_BB`, `EU_SBB`, `EU_DICE`, `BR_BL`, `AI_BLK` · `ACTUAL_UPTO=9` · `WOG_UPTO=4` · Google Sheet overlay ผ่าน `GS_PRICE` | `_iT7` L1494 |
| t8 | ในประเทศ vs ส่งออก | **`DP`** (L1674) รายปักษ์ 14 ม.ค.–2 ก.ย. 69 (17 จุด*) · กราฟ `c-dom-parts`, `c-dom-exp` | `_iT8` L1672 |
| t9 | ราคาในประเทศ | **`RAW`** (L1718, แยกจาก DP!) 16 จุด ถึง 26 ส.ค. · เฉลี่ยรายเดือน `MO9`(ม.ค.–ส.ค.) + คาด `FCL`(ก.ย.–พ.ย.) · `REG` ราคารายภาค · `#kpi9` | `_iT9` L1717 |
| t10 | ตลาดส่งออกไทย | `JPF/JPC, UKF/UKC, EUF/EUC, MYF` (ม.ค.–ส.ค. 69) · KPI `#kpi10` (YTD ส.ค.) | `_iT10` L1769 |

\* จุด 2 ก.ย. ยังไม่ commit

- Lazy init: `goTab(id)` เรียก `_initTab` ครั้งแรกเท่านั้น (`_tabInited` ประกาศไว้แค่ t1–t7 แต่ t8–t10 ก็ทำงานได้เพราะ `!undefined`)
- helper: `mkLine(id,labels,ds)`, `mkBar`, `mkOpts()` (**legend ของ Chart.js ปิด** — legend ที่เห็นเป็น HTML `.leg` แยก), `lds(label,data,color,dash)`, `bds(...)`
- ลำดับใน HTML ≠ ลำดับเมนู (ไม่มีผล)

---

## 4. แหล่งข้อมูล → ตัวแปร

| แหล่ง | ไปที่ | หมายเหตุ |
|---|---|---|
| Google Sheet (gid=0 แท็บ Import-Export) | t1–t5 + ราคา BLK/Souiku t7 | parse ด้วย "ข้อความหัวตาราง" ใน `_gsApply()` · ชีตต้องแชร์ Anyone-with-link |
| `Data Domestic/2569/*.jpg` (รูปรายงานสมาคมฯ) | `DP` (t8) + `RAW` (t9) | **ต้องอ่านรูปด้วยตา** — ตารางราคาชิ้นส่วนในประเทศ (บาท/กก.) **ไม่มีใน PDF** |
| Packer PDF (minutes ประชุม) | t10 (Table 1/2 ปริมาณส่งออก YTD), ราคาส่งออก t7 | PDF มีข้อความ (pdfplumber อ่านได้) แต่ **ไม่มี**ตารางราคาในประเทศ · ไก่เป็นอยู่ในบรรยาย "มีชีวิต…เสนอขาย N บาท" |
| `BR Raw Chicken Exports (MMM'26).xlsx` | t3 `RAW_JAPAN`, t6 | ชีต "Japan by State" แถว TOTAL TO JAPAN = ปริมาณรายเดือน |
| `ข้อมูลญี่ปุ่น/…update JUN 2026/Stock ญี่ปุ่น.xlsx` | t5 `ST_*` | col9 = total ending stock, col11 = imported stock |

> ชื่อไฟล์รูป `LINE_ALBUM_packer_YYMMDD` = **วันอัปโหลด ไม่ใช่วันที่รายงาน** — ดูวันที่จริงที่หัวรูป (เช่น 260910 = รายงาน 2 ก.ย., 260902 = รายงาน 26 ส.ค.)

---

## 5. สูตรอัปเดตข้อมูล (ทำซ้ำได้)

### 5.1 รูปรายงานในประเทศใหม่ → t8 + t9
อ่านจากรูป: วันที่หัวรายงาน · ราคาชิ้นส่วนในประเทศ (โครงเต็ม / เนื้อ BB / น่องติดสะโพก — **ใช้ค่ากลางของช่วง**) · ไก่มีชีวิต (ฟาร์มเสนอขาย) · ลูกไก่ · ไก่พันธุ์ปลด เมีย/ผู้ · ราคาส่งออกญี่ปุ่น ไก่สด (ค่ากลาง USD/ตัน) · THB/USD คอลัมน์วันรายงาน · ราคารายภาค
- **t8 `DP`** เพิ่ม `{date:'YYYY-MM-DD',kron,bb,leg,live,jp,thb}` ท้าย array (ราคาส่งออกบาท/กก. คำนวณในโค้ด = jp×thb/1000)
- **t9 `RAW`** เพิ่ม `{d:'D เดือนย่อ',chick,live,sf,sm,kron,bb,leg}` · ถ้าขึ้นเดือนใหม่ → เพิ่มเดือนใน `MO9`, เลื่อน `FCL` + ค่าคาด `fLive/fChick/fSf/fSm/fLeg/fBb/fKron` (3 ค่า), แก้ index `[7]` ใน `#kpi9` และป้าย "(ส.ค. เฉลี่ย)", อัปเดต `REG` + ป้าย "ปัจจุบัน (26 ส.ค.)"
- ⚠️ **ต้องแก้ทั้ง 2 ที่** (เคยลืม t9 มาแล้ว)

### 5.2 Packer PDF ใหม่ → t10
1. หน้า Table 1/2 "Estimated Chicken Meat Exports of Thailand [Jan–Mmm]" ได้ **YTD** แยก Raw/Cooked ต่อตลาด (Japan, UNITED KINGDOM, THE EUROPEAN UNION) · มาเลเซียอยู่หน้า "ตลาดมาเลเซีย" (สดล้วน, KL+Sabah)
2. เดือนใหม่ = **YTD ใหม่ − ผลรวมเดือนก่อนหน้าใน array** (แยกสด/สุก) → ใส่ index ถัดไปของ `JPF/JPC/UKF/UKC/EUF/EUC/MYF`
3. ตรวจ: ผลรวมต้อง = YTD ในรายงานเป๊ะ
4. แก้ KPI `#kpi10` (ค่า YTD, % สุก, เทรนด์ YoY จากคอลัมน์ Change 25/26), ป้าย `(YTD ส.ค.)`, และข้อความที่มา "Packer 1–15/2569 · ม.ค.–ส.ค."

### 5.3 สต๊อก / บราซิล / ราคา
- สต๊อก: เติม `ST_TOT26` / `ST_IMP26` (หน่วยตัน) · ข้อความบทวิเคราะห์ใน t5 มีตัวเลขเดือนอ้างอิง ถ้าเปลี่ยนมากให้ทบทวน
- บราซิล: `RAW_JAPAN['2026'][เดือน]`
- ราคา BLK/Souiku: ให้ผู้ใช้กรอกใน Google Sheet (ไฟล์ xlsx ในเครื่อง**เก่ากว่า**ชีต — อย่าใช้เป็นแหล่งจริง) · ราคา Karaage/SBB/BB/คาดการณ์ ต้องแก้ JS ใน `_iT7`
- เมื่อมีข้อมูลใหม่ แก้ meta "อัปเดตล่าสุด …" ในหัวหน้า

---

## 6. Login gate
- UI `#login-gate` (พื้นหลังเป็นรูป JPEG base64 ขนาดใหญ่ใน CSS `#login-gate{background:url("data:image/jpeg;base64,…")}`)
- `tryLogin()` → `_h(inp.value)===_PWH` → `_unlock()` · จำสถานะใน `sessionStorage['jbd_auth']`
- **เปลี่ยนรหัส:** คำนวณ `_h('รหัสใหม่')` ด้วยฟังก์ชันในหน้าเว็บ (console / javascript_tool) → แทน `var _PWH=…;` (L812) — อย่าเขียนฟังก์ชัน hash ใหม่เอง
- **ห้ามใส่รหัส plaintext ใน repo** (public)
- client-side ล้วน → ใครเปิด source ก็ bypass ได้

---

## 7. วิธี verify (สำคัญ)
1. เสิร์ฟสำเนาที่ `/tmp` (โฟลเดอร์ iCloud ใช้ `python3 -m http.server` ตรง ๆ ไม่ได้ — `os.getcwd()` error):
   ```bash
   mkdir -p /tmp/idx && cp ".../data-import-main/index.html" /tmp/idx/index.html
   cat > /tmp/serve3.py <<'PY'
   import http.server, socketserver, os
   os.chdir("/tmp/idx")
   socketserver.TCPServer(("127.0.0.1", 8790), http.server.SimpleHTTPRequestHandler).serve_forever()
   PY
   python3 /tmp/serve3.py &
   ```
   แล้วเปิด Browser pane ที่ `http://127.0.0.1:8790/`
2. ผ่าน login ใน JS: `document.getElementById('login-pw').value='<รหัส>'; tryLogin();` แล้ว `goTab('t8')` ฯลฯ
3. ตรวจด้วยข้อมูล: `Chart.getChart('c-dom-parts').data` · นับการ์ด `querySelectorAll('.kpi')` · `read_console_messages(onlyErrors)`
4. ⚠️ **Browser pane screenshot มักได้ภาพว่าง / กราฟ width 0** — เป็นข้อจำกัดของ pane ไม่ใช่บั๊ก อย่าสรุปว่ากราฟพัง · ภาพจริงใช้ Chrome headless:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --window-size=1300,4200 --virtual-time-budget=8000 --screenshot=/tmp/x.png URL` (ติด login gate — ต้อง bypass ก่อนถ้าจะดูข้างใน)
5. แก้ไฟล์ด้วย Python + `assert s.count(old)==1` ทุกครั้ง · สำรองก่อนแก้ `cp index.html /tmp/index_before_xxx.html`
6. ไม่มี `node`, `timeout`, `gh` ในเครื่อง · macOS

---

## 8. Git
- `data-import-main` เป็น git repo แล้ว (ตั้ง 9 ก.ย.) · identity: `nicha <nichasenapeng13@gmail.com>` · `credential.helper=osxkeychain` (token อยู่ใน Keychain — push ได้โดยไม่ต้องขอรหัส)
- **ผู้ใช้บางครั้งอัปโหลด index.html ผ่านหน้าเว็บ GitHub เอง** → `git fetch` + ดู `git rev-list --left-right --count HEAD...origin/main` ก่อน push ทุกครั้ง
- ขั้นตอน:
  ```bash
  cd ".../data-import-main"
  git fetch origin && git merge --ff-only origin/main   # ถ้า remote ล้ำ
  git add index.html && git commit -m "..." && GIT_TERMINAL_PROMPT=0 git push origin main
  ```
- ท้าย commit message ใส่ `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`
- ประวัติล่าสุดบน remote: `f31c871` แก้การ์ด KPI ซ้อน · `6235825`/`62ef5c3` ผู้ใช้อัปผ่านเว็บ (เนื้อไฟล์เท่าเดิม) · `4fddf7c` .gitignore · `ad67ff6` อัปเดต ส.ค. + Packer 15

---

## 9. กับดัก / บทเรียน
- **แก้ผิดไฟล์** — ยืนยัน path `data-import-main/index.html` ก่อนแก้ทุกครั้ง
- **innerHTML +=** ในฟังก์ชัน init ทำให้ข้อมูลซ้อนเมื่อถูกเรียกซ้ำ → เคลียร์ container ก่อนเสมอ (แก้ที่ `_iT1` แล้ว)
- **ข้อมูลในประเทศมี 2 ชุด** (`DP` t8, `RAW` t9) — อัปเดตคู่กัน
- **หน่วยบราซิลไม่คงที่** ในไฟล์ xlsx บางเดือน (พัน-USD / ตัน แทน KG) — ตรวจสเกลก่อนใช้
- **สต๊อกญี่ปุ่น (MAFF 鶏肉需給表)** แยกได้แค่นำเข้า/ในประเทศ ไม่แยกสด-สุก (นิยามแหล่ง = ไก่ดิบแช่แข็ง)
- **ตัวเลข "ไทย→ญี่ปุ่น" 2 ชุดไม่เท่ากัน**: t10 ≈ 41k ตัน/เดือน (ศุลกากรไทย รวมปรุงสุก) vs `THAI` t1 ≈ 14.8k (ฝั่งญี่ปุ่น นับเฉพาะไก่ดิบ) — คนละมาตรวัด
- ราคารายเดือน ≈ random walk → อย่าอ้างความแม่นของคาดการณ์โดยไม่ backtest

---

## 10. สิ่งที่ทำใน session ก่อนหน้า (ส.ค.–ก.ย. 2569)
- t8/t9: เพิ่มข้อมูลในประเทศ 26 ส.ค. (DP + RAW) · 2 ก.ย. (DP เท่านั้น — ยังไม่ commit)
- t10: เพิ่มเดือน ส.ค. จาก Packer 15 (YTD ญี่ปุ่น 329,264 · UK 132,282 · EU 115,782 · มาเลเซีย 67,386) + KPI/เทรนด์/ที่มา
- t5: กล่อง "🔍 บทวิเคราะห์: สต๊อกญี่ปุ่นทำนายอะไรได้" + **รวบ 2 กราฟเป็นอันเดียว** (ลบ `c-st-flow` ย้ายแถบกรอบเข้า `c-st-mo`; โค้ด `c-st-flow` ยังอยู่แต่ข้ามเพราะไม่มี canvas)
- t1: แก้บั๊กการ์ด KPI ซ้อน 2 แถว
- ตั้ง git repo · ล้างไฟล์ซ้ำ · เปลี่ยนรหัสผ่าน (ยังไม่ push)

### ผลวิเคราะห์ที่ได้ (ใช้ตอบคำถามต่อได้)
- ค่าเฉลี่ยส่งออกไทย/เดือน (ม.ค.–ส.ค. 69): ญี่ปุ่น 41,158 (สด 16,575 + สุก 24,583) · UK 16,535 (สุก ~95%) · EU 14,473 · มาเลเซีย 8,423 (สดล้วน)
- สต๊อกนำเข้าญี่ปุ่น **นำ** ปริมาณบราซิล→ญี่ปุ่น 2–3 เดือน (corr −0.53 ที่ lag 2) = วงจรเติมสต๊อก
- ไทย→ญี่ปุ่น vs สต๊อก ≈ 0 (ทั้งรวมสุก และดิบต่อดิบ) · vs เยน ≈ 0.08
- ดีมานด์ไทยมีฤดูกาล: ต.ค. +12%, ธ.ค. +9% / พ.ค. −16%, ส.ค. −11% · โตจาก 136k (2022) → 180k (2025)
- ข้าวโพด vs ดีมานด์ไทย −0.67 แต่น่าจะเป็นผลของเทรนด์ (ยังไม่ได้ทดสอบแบบหักเทรนด์)
- ส่งออกญี่ปุ่น (ไก่สด) แพงกว่าน่องติดสะโพกในประเทศเฉลี่ย ~64%

---

## 11. งานค้าง / ถัดไป
1. **ตัดสินใจเรื่องรูป login** → ผู้ใช้แนบรูปไก่การ์ตูน (ตัวไข่สีครีม หงอน/เหนียง/ปีกแดง ปาก-เท้าเหลือง ขอบน้ำตาล) ให้ใช้แทนรูปดอกไม้เดิม แต่ไฟล์**ไม่อยู่บนดิสก์** · ตัวเลือก: (ก) ใช้ SVG ที่ Claude วาดไว้ (สีหลัก ครีม `#FCF6DC`, ขอบ `#8B5A3C`, แดง `#D42A1E`, เหลือง `#F5C518`) (ข) ผู้ใช้เซฟไฟล์ลง `data-import-main/` แล้วฝังเป็น base64 · ต้องตัดสินว่าจะเป็น **พื้นหลังเต็มจอ** หรือ **โลโก้ในการ์ด login** (ถามผู้ใช้)
2. **Push** การแก้ที่ค้าง (รหัส + DP 2 ก.ย. + รูป) ทีเดียว
3. **t9 ยังขาด 2 ก.ย.** — เพิ่มใน `RAW`: `{d:'2 ก.ย.',chick:20.5,live:45,sf:24,sm:16,kron:14,bb:75,leg:83}` + เพิ่ม ก.ย. ใน `MO9` + เลื่อนคาดการณ์ (ดู 5.1) · ราคารายภาค 2 ก.ย.: เหนือบน 48–50, เหนือล่าง 45–48, อีสานบน 48–50, อีสานล่าง 47–48, ภาคกลาง 45–46, ตะวันออก 46–48, ตะวันตก 45–46, ใต้บน 48–50, ใต้ล่าง 47–50
4. **รูปใหม่ยังไม่ได้อ่าน:** `Data Domestic/2569/LINE_ALBUM_packer_260915_1.jpg` (ตรวจวันที่รายงานก่อน) → t8 + t9
5. เมื่อมี Packer 16 → เพิ่มเดือน ก.ย. ใน t10 (สูตร 5.2)
6. (ตัวเลือก) ทดสอบข้าวโพด↔ดีมานด์ไทยแบบหักเทรนด์ · เพิ่มกราฟเทียบบราซิล↔สต๊อก · อ่านรูปในประเทศปี 2565–2568 เพื่อให้คาดการณ์มีฤดูกาล
