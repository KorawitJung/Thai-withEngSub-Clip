# thai-story-shorts

สกิล Claude Code สำหรับทำคลิปแอนิเมชันแนวตั้ง ภาษาไทย อังกฤษ หรือสองภาษาในคลิปเดียว ตั้งแต่บท เสียงพากย์ ซับ ภาพ ไปจนถึงไฟล์ MP4

- **ภาษา:** ไทย, อังกฤษ, ซับสองภาษา, พูดปนสองภาษา หรือแยกสองเวอร์ชัน
- **สไตล์:** `story-night`, `story-warm`, `horror-rules`, `explainer-paper`, `data-clean`
- **แนว:** เรื่องลุ้น สยอง ตำนาน สอนเป็นขั้นตอน อธิบายธุรกิจ สรุปข่าว โปรโมตสถานที่

## ติดตั้ง
คัดลอกโฟลเดอร์ `skills/thai-story-shorts` ไปไว้ที่ `~/.claude/skills/thai-story-shorts`

ต้องมี Python 3.10+, ffmpeg, Node.js และคีย์ ElevenLabs สำหรับเสียงพากย์จริง

## ใช้งาน
เปิดโฟลเดอร์งานใน Claude Code แล้วพิมพ์ เช่น:
- `ทำคลิปเรื่องผีภาคอีสาน พากย์ไทย ซับไทยอังกฤษ`
- `Make an English explainer reel about why short videos lose viewers`
- `สรุปข่าวนี้เป็นคลิป 45 วินาที แยกเวอร์ชันไทยกับอังกฤษ`

## ทดสอบ
```bash
python -m unittest discover -s tests
```

## สัญญาอนุญาต
MIT ดู `LICENSE` และบริการภายนอกที่ใช้ใน `THIRD_PARTY.md`
