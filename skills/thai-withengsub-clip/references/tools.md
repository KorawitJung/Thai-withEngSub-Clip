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
python $SKILL/scripts/tighten.py audio/narration.wav audio/alignment.json audio/tight --max-gap 0.35
```
ฟังผลทุกครั้ง เพราะการตัดเงียบอาจกินปลายเสียงเบา ถ้าเป็นแบบนั้นให้ลด `--noise` เช่น `-45` หลีกเลี่ยงการเร่งเสียงด้วย `--speed` ถ้ายาวเกินให้ตัดบทก่อน

ถ้าเสียงชิดกันเกินไป หรืออยากตัดบางแถวโดยไม่สร้างเสียงใหม่ ใช้ `pace.py` หลัง `timing.py` โดยใส่เลขแถวตามที่ `timing.py` พิมพ์ออกมา:
```bash
python $SKILL/scripts/pace.py audio/narration.wav audio/subtitles.json audio/paced --min-gap 0.42 --pad 7=0.4 --drop 12
```
ค่า `--pad` เหมาะกับช่วงก่อนจุดพลิก หลังใช้ `--drop` เลขแถวถัดจากแถวที่ตัดจะลดลง ต้องแก้ `line=` ใน `episode.py` ให้ตรง

## เร่งเสียงตามความเร็วที่สั่ง
ใช้เมื่อผู้ใช้บอกความเร็ว เช่น 1.12 เท่า สคริปต์ปรับเวลาซับให้ตรงและวัดผลจริง:
```bash
python $SKILL/scripts/speed.py audio/narration.wav audio/subtitles.json audio/x112 --factor 1.12
```
อย่าแปลงความเร็วเป็น `retime.py --target` เพราะ `retime.py` คำนวณจากเวลาพูดกับเวลาเป้าหมาย ไม่ได้รับตัวคูณโดยตรง ความเร็วที่ได้จึงอาจไม่ตรงตามที่สั่ง

## ย่อเวลาคลิป
ใช้เมื่อผู้ใช้สั่งย่อหลังสร้างเสียงแล้ว สคริปต์เร่งเสียงและปรับเวลาซับให้ตรง ถ้าเร็วเกิน 1.25 เท่าจะเตือน ซึ่งควรเสนอให้ตัดบทแทน:
```bash
python $SKILL/scripts/retime.py audio/narration.wav audio/subtitles.json audio/fit --target 60 --hold 5 --card-line
```
`--card-line` คือแถวสุดท้ายพูดบนหน้าโลโก้ แล้วคัดลอก `audio/fit/narration.wav` ไป `video/assets/` และรัน `compose.py` ด้วย `audio/fit/subtitles.json` กับ `--hold 5`

## ข้อมูลการค้นหา
`trends.py` ดึง Google Trends และคำนวณว่า 2 คำขยับตามกันแค่ไหน วิธีอ่านผลอยู่ใน `reel-style.md`:
```bash
uv run --with pytrends --with "urllib3<2" --with pandas --with scipy $SKILL/scripts/trends.py fetch data.json "ดูดวง" "หางาน" --to 2026-10-31
```
```bash
uv run --with pandas --with scipy $SKILL/scripts/trends.py corr data.json "ดูดวง" "หางาน"
```
เว้นระยะระหว่างการดึงแต่ละรอบ เพื่อเลี่ยงการถูกจำกัดจำนวนครั้ง

## แผนที่
```bash
python $SKILL/scripts/map_route.py map_data.json --stop start,13.7567,100.5018 --stop end,13.7400,100.4985
```

## ดนตรี
ทางเลือกแรกคือ `soundscape.py pad` เพราะใช้เวลาน้อย ไม่ติดสัญญาของโมเดล อยู่ในย่านเสียงที่ลำโพงมือถือเล่นได้ และไม่มีเสียงซ่า `drone`, `rain`, `wind` เหมาะเป็นเสียงช่วงสั้น ไม่ควรใช้เป็นพื้นตลอดคลิป

ก่อนเรนเดอร์ให้ตรวจระดับดนตรี เป้าหมายคือต่ำกว่าเสียงพูดราว 13 LU สคริปต์จะบอกค่า volume ที่ควรใช้ แต่ยังต้องให้คนฟัง:
```bash
python $SKILL/scripts/audio_check.py video/assets/narration.wav video/assets/music.wav --volume 0.2
```

ถ้าต้องการดนตรีจริง ใช้ `music.py` ซึ่งรันในเครื่องด้วย MusicGen:
```bash
uv run $SKILL/scripts/music.py "dark ambient, slow, no drums" 70 video/assets/music.wav
```
- ต้องติดตั้ง uv ด้วย `winget install astral-sh.uv` และเผื่อพื้นที่ราว 4 GB
- รันอยู่เบื้องหลัง เพราะครั้งแรกต้องดาวน์โหลดนาน
- สร้างได้ครั้งละไม่เกิน 30 วินาที แล้ววนซ้ำให้ครบความยาว อาจได้ยินรอยต่อ
- โมเดลเริ่มต้นมีสัญญาห้ามใช้เชิงพาณิชย์ ตรวจสัญญาล่าสุดก่อน ถ้าคลิปหารายได้ให้ใช้เสียงอื่น

## ฟอนต์
สกิลมีคลังฟอนต์ไทยและอังกฤษ 57 แบบจาก Google Fonts ดาวน์โหลดเมื่อใช้ครั้งแรก เก็บไว้ที่ `~/.cache/thai-withengsub-clip/fonts` และคัดลอกเข้า `video/assets/fonts` ของคลิป ดูวิธีเลือกใน `references/fonts.md` ถ้าไม่มีอินเทอร์เน็ต ใช้ `--system-fonts` ซึ่งจะเลือก Leelawadee UI, Sukhumvit Set, Noto Sans Thai หรือ Tahoma ที่มีในเครื่อง

## ความดัง
`master.py` ตั้งค่าเริ่มต้นที่ -14 LUFS ซึ่งตรงกับคลิปตัวอย่างที่วัดได้ ปรับได้ด้วย `--lufs` เมื่อเสร็จจะวัดไฟล์สุดท้าย และเขียน `<ชื่อไฟล์>-review.md` พร้อมรายการที่คนต้องตรวจ

คำเตือน `timeline_track_too_dense` และ `nested_structure_needs_subcomposition` จาก HyperFrames เกิดจากการรวมคลิปไว้ในไฟล์เดียว และไม่ขัดขวางการเรนเดอร์

## ปัญหาที่พบบ่อย
| อาการ | แก้ |
|---|---|
| `not found in narration order` | `say` ไม่ตรงหรือไม่เรียงตาม `narration.txt` |
| ซับเป็นสี่เหลี่ยม | ติดตั้งฟอนต์ไทย |
| `voice_not_fine_tuned` | เสียงนั้นใช้ไม่ได้แม้เพิ่มเข้าบัญชีแล้ว ให้เลือกเสียงอื่น |
| ฉากล้นลงมาทับซับ | ตรวจฉากที่มีของตกหรือขยับ ให้อยู่เหนือ y=1060 และดูจากไฟล์ที่เรนเดอร์แล้ว |
| Remotion Studio ขึ้น `package.json` ENOENT | ต้องรันจากโฟลเดอร์โปรเจกต์ |
| โค้ด TSX ในคำสั่ง Bash เพี้ยน | เขียนไฟล์ด้วยเครื่องมือเขียนไฟล์ แทน heredoc ที่มีเครื่องหมายคำพูดปนกัน |
| ไม่รู้ตัวเลือกของ HyperFrames | รัน `npx hyperframes --help` เพราะคำสั่งอาจเปลี่ยนตามรุ่น |
