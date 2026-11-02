---
name: thai-story-shorts
description: Create vertical 9:16 Thai narrated animated story shorts for TikTok, Reels and YouTube Shorts, with fact-checked tips, code-drawn scenes, synced Thai subtitles, sound and MP4 rendering. Use when the user wants a Thai survival, disaster, safety or suspense clip, a series episode, or says ทำคลิปสั้น เล่าเรื่องลุ้นระทึก คลิปเอาชีวิตรอด คลิปความรู้ความปลอดภัย ทำตอนต่อ.
---

# คลิปเรื่องเล่าแนวตั้งภาษาไทย

คุยกับผู้ใช้เป็นภาษาไทยแบบเข้าใจง่าย เอกสารงานเป็นภาษาไทย `$SKILL` คือโฟลเดอร์ของสกิลนี้
ใช้ `python` บน Windows และ `python3` บนแมค/ลินุกซ์

## อ่านเมื่อถึงขั้นนั้น
- `references/story-structure.md`: วางเรื่อง เขียนบท
- `references/visual-guide.md`: วางช็อต วาดฉาก
- `references/tools.md`: ติดตั้ง เสียง เรนเดอร์ ปัญหาที่พบบ่อย
- `examples/demo/`: ตัวอย่างไฟล์ครบชุดแบบสั้น

## โฟลเดอร์งาน
```
<ซีรีส์>/story-notes.md
<ซีรีส์>-ep<N>/
  script.md  narration.txt  lines.json  episode.py
  audio/     video/index.html  video/assets/  <ซีรีส์>-ep<N>.mp4
```

## ขั้นตอน

1. **ตรวจเครื่อง**: รัน `python $SKILL/scripts/check_env.py` แจ้งเฉพาะสิ่งที่ขาด
2. **วางเรื่อง**: ถามภัย สถานที่ และตัวละครที่ผู้ใช้ต้องการ ถ้ายังไม่มี เสนอ 3 ไอเดีย ตอนแรกของซีรีส์ให้เขียน `story-notes.md`
3. **เขียนบท**: เขียน `script.md`, `narration.txt`, `lines.json` ค้นเว็บยืนยันทุกข้อเท็จจริงด้านความปลอดภัยและใส่แหล่งที่มา ถ้าแหล่งขัดกันให้บอกผู้ใช้ ตรวจจำนวนตัวอักษรด้วย `narrate.py --dry-run`
4. **ขออนุมัติบท** ก่อนสร้างเสียงเสมอ เพราะใช้เครดิต
5. **สร้างเสียง**: ถ้าผู้ใช้ไม่มีคีย์ ให้สร้าง `.env` เปล่าให้ผู้ใช้วางคีย์เอง ห้ามขอคีย์ในแชต ห้ามสร้างบัญชีแทน แล้วรัน:
   ```bash
   python $SKILL/scripts/narrate.py narration.txt audio --voice <VOICE_ID> --env-file .env
   ```
   ถ้าอยากดูภาพก่อนจ่ายเครดิต ใช้ `timing.py --estimate` สร้างเวลาคร่าวๆ แทน
6. **ทำซับ**:
   ```bash
   python $SKILL/scripts/timing.py lines.json audio/alignment.json audio/subtitles.json
   ```
7. **ทำเสียงประกอบ**: สร้างด้วย `soundscape.py` วางไว้ใน `video/assets/` พร้อมคัดลอก `narration.wav`
8. **เขียน `episode.py`** ตาม `visual-guide.md` แล้วสร้างคลิป:
   ```bash
   python $SKILL/scripts/compose.py episode.py video audio/subtitles.json
   ```
9. **ตรวจ**: ในโฟลเดอร์ `video` รัน `npx hyperframes check --json` และ `npx hyperframes snapshot --review` เพื่อดูภาพจริงทุกช็อต ตรวจซับทับของสำคัญ ตัวอักษรในพื้นที่ปลอดภัย และภาษาไทยไม่เพี้ยน
10. **เรนเดอร์**:
    ```bash
    npx hyperframes render -o ../render.mp4
    ```
    ```bash
    python $SKILL/scripts/master.py ../render.mp4 ../final.mp4
    ```
11. **ส่งงาน**: บอกตรงๆ ว่าวัดเสียงได้แต่ไม่ได้ฟัง ให้ผู้ใช้ฟังเอง พร้อมรายการแหล่งข้อมูลและจุดที่ควรเช็ก

## ตอนต่อ
อ่าน `story-notes.md` ก่อน ใช้ตัวละครและธีมเดิม เปิดตอนจากปมที่ค้างไว้ และอัปเดตบันทึกเมื่อจบตอน

## ขอบเขต
ใช้เรื่อง ตัวละคร และภาพของผู้ใช้เอง ห้ามลอกคลิปหรือช่องอื่น คำแนะนำที่อาจเป็นอันตรายถ้าผิด ห้ามใส่โดยไม่มีแหล่งยืนยัน
