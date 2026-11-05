# แม่แบบ Remotion สำหรับรีลแนวเล่าสนุก

ตัวอย่างจาก 3 คลิปจริง ไม่ได้รวมเสียง GIF ฟอนต์ หรือโลโก้ ต้องเตรียมตามนี้ ตัวเลขและข้อความในตัวอย่างเป็นของเรื่องเดิม ให้แทนด้วยบทและแหล่งข้อมูลของงานใหม่

ข้อควรรู้:
- Remotion มีสัญญาของตัวเอง สัญญา MIT ของ repo นี้ไม่ครอบคลุม ตรวจเงื่อนไขล่าสุดก่อนใช้ โดยเฉพาะในองค์กร
- ภาพเทพและเครื่องรางเป็นภาพวาดตัวอย่างแบบเรียบง่าย ยังไม่ได้ตรวจกับผู้รู้ ควรให้คนที่นับถือตรวจก่อนเผยแพร่
- ตัวละครผู้เล่าในควิซเป็นตัวอย่างลีลาการเล่า ควรให้ชุมชน LGBTQ+ ฟีดแบ็กก่อนเผยแพร่

## ไฟล์
- `src/Reel.tsx`: รายการช็อต ซับ โลโก้ และปก
- `src/Scenes.tsx`: ฉากทั่วไป เช่น ท้องฟ้า เหรียญตก ค้นหา และคนหลายคน
- `src/Characters.tsx`: ผู้เล่า เทพ เครื่องราง ป้ายผิด และ GIF
- `src/Memes.tsx`: กราฟจากข้อมูล ฉากดูดวง และแมวมีมที่วาดเอง
- `research/make_charts.py`: แปลงผล Trends เป็น `src/charts.json`

## เตรียมงาน
1. คัดลอกโฟลเดอร์นี้ไปที่โฟลเดอร์งาน แล้วรัน `npm install`
2. วางไฟล์ใน `public/<คลิป>/` คือ `narration.wav` และ `pad.wav` วางซับเป็น `src/<คลิป>.subs.json`
3. วางฟอนต์ใน `public/fonts/` โดยคัดลอกจาก `~/.cache/thai-withengsub-clip/fonts/` และโลโก้เป็น `public/logo.png`
4. วางโลโก้แพลตฟอร์มใน `public/logos/` จาก `https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/<ชื่อ>.svg`
5. แก้ `clips` และรายการช็อตใน `src/Reel.tsx` โดย `at` คือเลขแถวของซับ

## ตรวจและเรนเดอร์
รันทุกคำสั่งจากโฟลเดอร์โปรเจกต์:
```bash
npx remotion studio src/index.ts
```
```bash
npx remotion render src/index.ts <คลิป> out/<คลิป> --frames=30,90,150 --image-format=jpeg
```
```bash
npx remotion render src/index.ts <คลิป> render.mp4 --codec=h264
```
```bash
python $SKILL/scripts/master.py render.mp4 final.mp4
```
```bash
npx remotion still src/index.ts cover-<คลิป> cover.png --frame=125
```
เลือกเฟรมที่ฉากขึ้นครบแล้ว เพราะฉากจำนวนมากค่อยๆ เด้งเข้ามา
