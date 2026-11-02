# เครื่องมือ

| เครื่องมือ | ใช้ทำ | ติดตั้งบน Windows |
|---|---|---|
| Python 3.10+ | สคริปต์ | `winget install Python.Python.3.12` |
| ffmpeg | เสียงและความดัง | `winget install Gyan.FFmpeg` |
| Node.js | HyperFrames | `winget install OpenJS.NodeJS.LTS` |

## เสียงพากย์
ต้องมีคีย์ ElevenLabs ที่เปิดสิทธิ์ Text to Speech เก็บใน `.env` บรรทัด `ELEVENLABS_API_KEY=` และห้าม commit ตรวจราคาและสิทธิ์เชิงพาณิชย์ของแพ็กที่ใช้จากเว็บผู้ให้บริการก่อนหารายได้

## เสียงประกอบ
`soundscape.py` สร้างเสียงขึ้นจากคณิตศาสตร์ ไม่มีไฟล์ของบุคคลที่สาม:
```bash
python $SKILL/scripts/soundscape.py drone 70 video/assets/drone.wav
```
```bash
python $SKILL/scripts/soundscape.py hit video/assets/hit.wav
```
มีชนิด `drone`, `hit`, `tick`, `rush` ถ้าใช้ไฟล์จากภายนอก ต้องบันทึกที่มาและสัญญาอนุญาตในโปรเจกต์

## ฟอนต์
สกิลมีคลังฟอนต์ไทยและอังกฤษ 57 แบบจาก Google Fonts ดาวน์โหลดเมื่อใช้ครั้งแรก เก็บไว้ที่ `~/.cache/thai-story-shorts/fonts` และคัดลอกเข้า `video/assets/fonts` ของคลิป ดูวิธีเลือกใน `references/fonts.md` ถ้าไม่มีอินเทอร์เน็ต ใช้ `--system-fonts` ซึ่งจะเลือก Leelawadee UI, Sukhumvit Set, Noto Sans Thai หรือ Tahoma ที่มีในเครื่อง

## ความดัง
`master.py` ตั้งค่าเริ่มต้นที่ -14 LUFS ซึ่งตรงกับคลิปตัวอย่างที่วัดได้ ปรับได้ด้วย `--lufs`

คำเตือน `timeline_track_too_dense` และ `nested_structure_needs_subcomposition` จาก HyperFrames เกิดจากการรวมคลิปไว้ในไฟล์เดียว และไม่ขัดขวางการเรนเดอร์

## ปัญหาที่พบบ่อย
| อาการ | แก้ |
|---|---|
| `not found in narration order` | `say` ไม่ตรงหรือไม่เรียงตาม `narration.txt` |
| ซับเป็นสี่เหลี่ยม | ติดตั้งฟอนต์ไทย |
| ไม่รู้ตัวเลือกของ HyperFrames | รัน `npx hyperframes --help` เพราะคำสั่งอาจเปลี่ยนตามรุ่น |
