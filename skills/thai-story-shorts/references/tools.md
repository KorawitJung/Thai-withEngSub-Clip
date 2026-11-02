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
มีชนิด `drone`, `rain`, `wind`, `hit`, `tick`, `rush`, `bubbles`

เสียงจาก Openverse ค้นด้วย `sfx.py` ซึ่งกรองเฉพาะสัญญาที่ใช้เชิงพาณิชย์ได้ และบันทึกที่มาลง `credits.md` เมื่อโหลด ควรเปิดหน้าต้นทางตรวจอีกครั้งก่อนเผยแพร่:
```bash
python $SKILL/scripts/sfx.py search "rain on roof"
```
```bash
python $SKILL/scripts/sfx.py get <AUDIO_ID> video/assets/
```

## ปรับเสียงพากย์
`tighten.py` ตัดช่วงเงียบที่ยาวเกินและปรับเวลาใน alignment ให้ตรงกับเสียงใหม่ ใช้เมื่อเสียงยาวเกินเป้าหรือเว้นจังหวะนานเกินไป โดยรันก่อน `timing.py`:
```bash
python $SKILL/scripts/tighten.py audio/narration.wav audio/alignment.json audio/tight --max-gap 0.35 --speed 1.05
```
ฟังผลทุกครั้ง เพราะการตัดเงียบอาจกินปลายเสียงเบา ถ้าเป็นแบบนั้นให้ลด `--noise` เช่น `-45`

## ดนตรี
ทางเลือกแรกคือ `soundscape.py drone` เพราะใช้เวลาน้อยและไม่ติดสัญญาของโมเดล ถ้าต้องการดนตรีจริง ใช้ `music.py` ซึ่งรันในเครื่องด้วย MusicGen:
```bash
uv run $SKILL/scripts/music.py "dark ambient, slow, no drums" 70 video/assets/music.wav
```
- ต้องติดตั้ง uv ด้วย `winget install astral-sh.uv` และเผื่อพื้นที่ราว 4 GB
- รันอยู่เบื้องหลัง เพราะครั้งแรกต้องดาวน์โหลดนาน
- สร้างได้ครั้งละไม่เกิน 30 วินาที แล้ววนซ้ำให้ครบความยาว อาจได้ยินรอยต่อ
- โมเดลเริ่มต้นมีสัญญาห้ามใช้เชิงพาณิชย์ ตรวจสัญญาล่าสุดก่อน ถ้าคลิปหารายได้ให้ใช้เสียงอื่น

## ฟอนต์
สกิลมีคลังฟอนต์ไทยและอังกฤษ 57 แบบจาก Google Fonts ดาวน์โหลดเมื่อใช้ครั้งแรก เก็บไว้ที่ `~/.cache/thai-story-shorts/fonts` และคัดลอกเข้า `video/assets/fonts` ของคลิป ดูวิธีเลือกใน `references/fonts.md` ถ้าไม่มีอินเทอร์เน็ต ใช้ `--system-fonts` ซึ่งจะเลือก Leelawadee UI, Sukhumvit Set, Noto Sans Thai หรือ Tahoma ที่มีในเครื่อง

## ความดัง
`master.py` ตั้งค่าเริ่มต้นที่ -14 LUFS ซึ่งตรงกับคลิปตัวอย่างที่วัดได้ ปรับได้ด้วย `--lufs` เมื่อเสร็จจะวัดไฟล์สุดท้าย และเขียน `<ชื่อไฟล์>-review.md` พร้อมรายการที่คนต้องตรวจ

คำเตือน `timeline_track_too_dense` และ `nested_structure_needs_subcomposition` จาก HyperFrames เกิดจากการรวมคลิปไว้ในไฟล์เดียว และไม่ขัดขวางการเรนเดอร์

## ปัญหาที่พบบ่อย
| อาการ | แก้ |
|---|---|
| `not found in narration order` | `say` ไม่ตรงหรือไม่เรียงตาม `narration.txt` |
| ซับเป็นสี่เหลี่ยม | ติดตั้งฟอนต์ไทย |
| ไม่รู้ตัวเลือกของ HyperFrames | รัน `npx hyperframes --help` เพราะคำสั่งอาจเปลี่ยนตามรุ่น |
