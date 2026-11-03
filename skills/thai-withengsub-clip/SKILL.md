---
name: thai-withengsub-clip
description: Create vertical 9:16 narrated animated shorts for TikTok, Reels and YouTube Shorts in Thai, English, or both in one clip, with bilingual subtitles. Handles stories, survival, horror, folklore, explainers, tutorials, news and data briefs, and local promos, from script and fact checking to voiceover, code-drawn scenes, sound and MP4. Use when the user wants a short vertical video, a reel, a series episode, or says ทำคลิปสั้น ทำรีลส์ คลิปสองภาษา คลิปเอาชีวิตรอด เรื่องผี คลิปอธิบาย สรุปข่าว ทำตอนต่อ.
---

# คลิปแนวตั้ง ไทย อังกฤษ และสองภาษา

ตอบตามภาษาที่ผู้ใช้พิมพ์ ใช้คำเข้าใจง่าย เอกสารงานใช้ภาษาเดียวกับผู้ใช้ `$SKILL` คือโฟลเดอร์ของสกิลนี้
ใช้ `python` บน Windows และ `python3` บนแมค/ลินุกซ์

## อ่านเมื่อถึงขั้นนั้น
- `references/formats.md`: โหมดภาษา สไตล์ และแนวคลิป อ่านก่อนวางเรื่องเสมอ
- `references/story-structure.md`: เขียนบท และรูปแบบไฟล์บท
- `references/visual-guide.md`: วางช็อต วาดฉาก
- `references/series.md`: วางซีรีส์ แม่แบบ `story-notes.md` และการทำตอนต่อ
- `references/clip-research.md`: สิ่งที่พบจากคลิปตัวอย่าง อ่านเมื่อเลือกสไตล์หรือวิเคราะห์ช่อง
- `references/fonts.md`: คลังฟอนต์ไทย/อังกฤษ และคู่ฟอนต์ตามแนวคลิป
- `references/tools.md`: ติดตั้ง เสียง ดนตรี เรนเดอร์ ปัญหาที่พบบ่อย
- `references/delivery.md`: ภาพจริงและเครดิต ปก แคปชันโพสต์
- `templates/`: `brief.md` แบบฟอร์มเริ่มงาน และ `channel.json` ค่าประจำช่อง

## หลักประหยัดเวลา
ตัดสินใจทุกอย่างที่เปลี่ยนแล้วต้องเรนเดอร์ใหม่ด้วยภาพนิ่งก่อน รวบคำขอแก้แล้วเรนเดอร์รอบเดียว และเรนเดอร์ทุกภาษาพร้อมกัน แก้ที่ `episode.py` หรือ `channel.json` ก่อนแก้สคริปต์ของสกิล
- `examples/`: `demo` (เรื่องเล่าสองภาษา มีไฟล์ครบหนึ่งตอน), `explainer-en` (อธิบายอังกฤษ), `data-mixed` (ข้อมูลไทยปนอังกฤษ)

## โฟลเดอร์งาน
```
<ซีรีส์>/story-notes.md
<ซีรีส์>-ep<N>/
  script.md  narration.txt  lines.json  episode.py  sound-cues.md  credits.md
  audio/     video/index.html  video/assets/  <ซีรีส์>-ep<N>.mp4  <ซีรีส์>-ep<N>-review.md
```

## ขั้นตอน

1. **ตรวจเครื่อง**: รัน `python $SKILL/scripts/check_env.py --network` แจ้งสิ่งที่ขาดและบริการที่เข้าไม่ได้ในรอบเดียว
2. **สรุปโจทย์**: ถ้ามี `channel.json` ในโฟลเดอร์งานให้อ่านก่อน ถามสิ่งที่ยังขาดรวดเดียวตาม `templates/brief.md` ถ้าผู้ใช้จะทำหลายคลิป เสนอสร้าง `channel.json` จากแม่แบบ ยืนยันแนวคลิป โหมดภาษา สไตล์ และฟอนต์ เลือกค่าที่เหมาะให้จากคำขอ แล้วบอกผู้ใช้ ถามเฉพาะสิ่งที่เดาไม่ได้ ถ้ายังไม่มีไอเดีย เสนอ 3 ไอเดีย ถ้าเป็นซีรีส์ให้เขียน `story-notes.md` ตาม `series.md`
3. **เขียนบท**: เขียน `script.md`, `narration.txt`, `lines.json` ค้นเว็บยืนยันทุกข้อเท็จจริงและใส่แหล่งที่มา รวมถึงหน้าตาจริงของสถานที่หรือสิ่งที่พูดถึง ถ้าแหล่งขัดกันให้บอกผู้ใช้ เรื่องที่มีแต่ในบล็อกให้ใช้คำว่า "เชื่อกันว่า" และตัดตัวเลขที่ยืนยันไม่ได้ ถ้าทำสองภาษา ให้บทอังกฤษมีจำนวนแถวเท่าบทไทยเพื่อใช้ช็อตเดิมได้ ตรวจจำนวนตัวอักษรด้วย `narrate.py --dry-run`
4. **ขออนุมัติบท** ทุกภาษาก่อนสร้างเสียงเสมอ เพราะใช้เครดิต
5. **สร้างเสียง**: ถ้าผู้ใช้ไม่มีคีย์ ให้สร้าง `.env` เปล่าให้ผู้ใช้วางคีย์เอง ห้ามขอคีย์ในแชต ห้ามสร้างบัญชีแทน แล้วรัน:
   ```bash
   python $SKILL/scripts/narrate.py narration.txt audio --voice <VOICE_ID> --env-file .env
   ```
   ฟังตัวอย่างสั้นก่อนเมื่อเปลี่ยนเสียงหรือภาษา ถ้าอยากดูภาพก่อนจ่ายเครดิต ใช้ `timing.py --estimate` สร้างเวลาคร่าวๆ แทน ถ้าเสียงยาวเกินเป้า ใช้ `tighten.py` ก่อนทำซับ แล้วใช้ไฟล์จาก `audio/tight` ในขั้นถัดไป
6. **ทำซับ**:
   ```bash
   python $SKILL/scripts/timing.py lines.json audio/alignment.json audio/subtitles.json --audio audio/narration.wav
   ```
   ถ้าเสียงชิดเกิน หรือต้องตัดบางแถว ใช้ `pace.py` แทนการสร้างเสียงใหม่ แล้วใช้ไฟล์จาก `audio/paced` ต่อ
7. **ทำเสียงประกอบ**: เริ่มจาก `soundscape.py pad` ตรวจระดับด้วย `audio_check.py` ใช้ `sfx.py` เมื่อต้องการเสียงจริง และใช้ `music.py` เมื่อผู้ใช้ต้องการดนตรีและคลิปไม่ใช้เชิงพาณิชย์ โดยรันอยู่เบื้องหลังระหว่างทำขั้นอื่น วางไว้ใน `video/assets/` พร้อมคัดลอก `narration.wav` และเขียนคิวลง `sound-cues.md`
8. **เขียน `episode.py`** ตาม `visual-guide.md` แล้วสร้างคลิป:
   ```bash
   python $SKILL/scripts/compose.py episode.py video audio/subtitles.json --preset <สไตล์> --subs <both|primary|secondary> [--channel channel.json] [--still] [--font-th <id>] [--font-en <id>] [--font-accent <id>]
   ```
9. **ตรวจและอนุมัติภาพนิ่ง**: ในโฟลเดอร์ `video` รัน `npx hyperframes check --json` และ `npx hyperframes snapshot --review` เพื่อดูภาพจริงทุกช็อตจาก `review-beats.jpg` ตรวจซับทับของสำคัญ ตัวอักษรในพื้นที่ปลอดภัย และทั้งสองภาษาแสดงถูกต้อง ส่งภาพให้ผู้ใช้อนุมัติโทน ฟอนต์ และตัวละครก่อนเรนเดอร์เต็ม
10. **เรนเดอร์**:
    ```bash
    npx hyperframes render -o ../render.mp4
    ```
    ```bash
    python $SKILL/scripts/master.py ../render.mp4 ../final.mp4
    ```
    คำสั่งนี้เขียน `final-review.md` ให้ด้วย ตั้งชื่อไฟล์ตามตอนจริง แก้ปัญหาที่รายงานก่อนส่ง
11. **ส่งงาน**: ทำปกและแคปชันตาม `delivery.md` เมื่อผู้ใช้ต้องการ บอกตรงๆ ว่าวัดเสียงได้แต่ไม่ได้ฟัง ให้ผู้ใช้ฟังเอง พร้อมรายการแหล่งข้อมูล เครดิต และจุดที่ควรเช็ก
12. **หลังจบตอน**: ถ้าเป็นซีรีส์ อัปเดต `story-notes.md` แล้วเสนอหัวข้อตอนถัดไป

## ตอนต่อและเวอร์ชันอื่น
- ตอนต่อ: อ่าน `story-notes.md` ข้ามขั้นที่ 1 ถ้าใช้เครื่องเดิม ใช้ตัวละคร ชุดสี ฟอนต์ เสียง และชิ้นส่วนเดิม
- เวอร์ชันภาษาอื่น: แปลบทให้เป็นธรรมชาติ สร้างเสียงและซับใหม่ แล้วใช้ `episode.py` เดิม ตรวจว่าช็อตยังเริ่มตรงกับแถวที่ถูกต้อง

## ขอบเขต
ใช้เรื่อง ตัวละคร และภาพของผู้ใช้เอง คลิปตัวอย่างที่ผู้ใช้ส่งมาใช้เรียนรู้แนวทางเท่านั้น ห้ามลอกตัวละคร โลโก้ หรือบท คำแนะนำที่อาจเป็นอันตรายถ้าผิด ห้ามใส่โดยไม่มีแหล่งยืนยัน
