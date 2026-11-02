# thai-story-shorts

สกิล Claude Code สำหรับทำคลิปแอนิเมชันแนวตั้งเล่าเรื่องภาษาไทย ตั้งแต่บท เสียงพากย์ ซับ ภาพ ไปจนถึงไฟล์ MP4

## ติดตั้ง
คัดลอกโฟลเดอร์ `skills/thai-story-shorts` ไปไว้ที่ `~/.claude/skills/thai-story-shorts`

ต้องมี Python 3.10+, ffmpeg, Node.js และคีย์ ElevenLabs สำหรับเสียงพากย์จริง

## ใช้งาน
เปิดโฟลเดอร์งานใน Claude Code แล้วพิมพ์ เช่น `ทำคลิปเอาชีวิตรอด ติดในลิฟต์ตอนไฟดับ กับหมาหนึ่งตัว`

## ทดสอบ
```bash
python -m unittest discover -s tests
```

## สัญญาอนุญาต
MIT ดู `LICENSE` และบริการภายนอกที่ใช้ใน `THIRD_PARTY.md`
