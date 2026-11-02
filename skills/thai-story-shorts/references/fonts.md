# การเลือกฟอนต์

ดูรายการด้วย `python $SKILL/scripts/fonts.py list --lang th` หรือค้นตามอารมณ์ด้วย `--mood horror` สร้างหน้าตัวอย่างด้วย `python $SKILL/scripts/fonts.py preview fonts.html`

แต่ละ preset มีฟอนต์เริ่มต้น เปลี่ยนได้ทีละบทบาท:

```bash
python $SKILL/scripts/compose.py episode.py video audio/subtitles.json --preset story-night --font-th trirong --font-en special-elite --font-accent srisakdi
```

| บทบาท | ใช้กับ | หลักการเลือก |
|---|---|---|
| `--font-th` | ซับและการ์ดภาษาไทย | ต้องอ่านทันบนมือถือ |
| `--font-en` | ซับและการ์ดภาษาอังกฤษ | น้ำหนักใกล้เคียงกับฟอนต์ไทยที่คู่กัน |
| `--font-accent` | คำเน้น `*คำ*` ในสไตล์ `explainer-paper` และ `data-clean` | ต่างจากฟอนต์หลักชัดเจน |

## คู่ฟอนต์แนะนำ
| แนว | ไทย | อังกฤษ | เน้น |
|---|---|---|---|
| เอาชีวิตรอด ภัยพิบัติ | `chakra-petch` | `oswald` | `black-ops` |
| เรื่องเล่า ตำนาน | `trirong` | `playfair` | `srisakdi` |
| สยอง | `kanit` | `special-elite` | `creepster` |
| อธิบาย ธุรกิจ | `prompt` | `inter` | `playfair` |
| ข่าว ข้อมูล | `ibm-thai` | `inter` | `archivo-black` |
| ไลฟ์สไตล์ โปรโมต | `mitr` | `poppins` | `pattaya` |
| น่ารัก ครอบครัว | `mali` | `rubik` | `itim` |
| เกม เทคโนโลยี | `bai-jamjuree` | `russo` | `rubik-glitch` |

## ข้อควรระวัง
- ฟอนต์ตกแต่ง ลายมือ และสยอง ใช้กับคำสั้นๆ ไม่ใช้เป็นซับทั้งคลิป เพราะอ่านช้า
- ฟอนต์อังกฤษในคลังไม่มีตัวไทย ถ้าใช้เป็น accent กับคำไทย คำนั้นจะแสดงด้วยฟอนต์ไทยแทน
- ฟอนต์ไม่มีตัวเอียงจริง ตัวเน้นจึงเป็นการเอียงที่เบราว์เซอร์สร้างให้ ตรวจภาพจริงกับภาษาไทยเสมอ
- ดูว่าวรรณยุกต์และสระไม่ทับกัน โดยเฉพาะคำอย่าง "น้ำ" และ "ที่นี่"
- ก่อนใช้เชิงพาณิชย์ ตรวจสัญญาอนุญาตของฟอนต์ที่หน้า Google Fonts
