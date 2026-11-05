import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, continueRender, delayRender} from 'remotion';
import tiktokSubs from './reel-tiktok-vs-google.subs.json';
import muteluSubs from './reel-mutelu.subs.json';
import slangSubs from './reel-slang-quiz.subs.json';
import * as S from './Scenes';
import * as S2 from './Memes';
import charts from './charts.json';
import {Bubble, DeityScene, CakeForkScene, FireworkSticker, FoodScene, Mood, PapayaScene, Person, Reveal, ShockCat, Sticker, ToothScene, WishMoneyScene} from './Characters';

const INK = '#23323a', RED = '#c65a48', TEAL = '#12a594', SUN = '#ffc93c', GREY = '#6b7680';
type Sub = {show: string; sub: string; start: number; end: number; in?: number; out?: number};
type Shot = {at: number; v: React.ReactNode; mood?: Mood; low?: React.ReactNode; sfx?: string; sfx2?: string};
type Clip = {id: string; dir: string; subs: Sub[]; accent: string; who: 'host' | 'viewer' | 'mu'; shots: Shot[]};
type LogoKey = 'google' | 'tiktok' | 'shopee';

const fonts = [['Mitr', 'mitr-500', 500], ['Mitr', 'mitr-700', 700], ['Rubik', 'rubik-500', 500], ['Rubik', 'rubik-700', 700]] as const;
const handle = delayRender('fonts');
Promise.all(fonts.map(([family, file, weight]) => new FontFace(family, `url(${staticFile(`fonts/${file}.ttf`)})`, {weight: String(weight)}).load().then((f) => document.fonts.add(f)))).then(() => continueRender(handle));

const useIn = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return spring({frame, fps, config: {damping: 16, stiffness: 130}});
};
const Enter: React.FC<{children: React.ReactNode}> = ({children}) => {
	const p = useIn();
	return <div style={{position: 'absolute', left: 0, right: 0, top: 0, opacity: p, transform: `translateY(${(1 - p) * 40}px) scale(${0.96 + 0.04 * p})`}}>{children}</div>;
};
const Box: React.FC<{top?: number; bg?: string; children: React.ReactNode}> = ({top = 190, bg = '#fff', children}) => (
	<div style={{position: 'absolute', left: 70, right: 140, top, padding: '28px 44px', borderRadius: 36, background: bg, boxShadow: '0 18px 50px rgba(30,40,50,.14)'}}>{children}</div>
);
const Src = ({t, top}: {t: string; top: number}) => <div style={{position: 'absolute', left: 76, right: 144, top, fontSize: 28, color: GREY}}>{t}</div>;

const LOGOS = {google: {color: '#4285F4', name: 'Google'}, tiktok: {color: '#10151a', name: 'TikTok'}, shopee: {color: '#ee4d2d', name: 'Shopee'}};
const Logo = ({k, s}: {k: LogoKey; s: number}) => {
	const url = `url(${staticFile(`logos/${k}.svg`)})`;
	return <span style={{width: s, height: s, display: 'inline-block', background: LOGOS[k].color, WebkitMaskImage: url, maskImage: url, WebkitMaskSize: 'contain', maskSize: 'contain', WebkitMaskRepeat: 'no-repeat', maskRepeat: 'no-repeat'}} />;
};
const Logos = ({keys}: {keys: LogoKey[]}) => (
	<Enter>
		<div style={{position: 'absolute', left: 60, right: 60, top: 400, display: 'flex', justifyContent: 'center', gap: 50}}>
			{keys.map((k) => (
				<div key={k} style={{width: 400, height: 420, borderRadius: 48, background: '#fff', boxShadow: '0 18px 50px rgba(30,40,50,.14)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 30}}>
					<Logo k={k} s={190} />
					<div style={{fontFamily: 'Rubik', fontWeight: 700, fontSize: 54, color: INK}}>{LOGOS[k].name}</div>
				</div>
			))}
		</div>
	</Enter>
);
const CountUp = ({text}: {text: string}) => {
	const f = useCurrentFrame();
	const m = text.match(/^(\D*)([\d,]+(?:\.\d+)?)(.*)$/);
	if (!m) return <>{text}</>;
	const target = Number(m[2].replace(/,/g, ''));
	const dec = (m[2].split('.')[1] || '').length;
	const v = target * interpolate(f, [0, 24], [0, 1], {extrapolateRight: 'clamp', easing: (x) => 1 - (1 - x) ** 3});
	return <>{m[1]}{v.toLocaleString('en-US', {minimumFractionDigits: dec, maximumFractionDigits: dec})}{m[3]}</>;
};
const Card = ({head, num, note, tr, src, logo}: {head: string; num: string; note?: string; tr?: string; src?: string; logo?: LogoKey}) => (
	<Enter>
		<Box>
			<div style={{fontSize: 38, color: INK, display: 'flex', alignItems: 'center', gap: 20}}>{logo && <Logo k={logo} s={58} />}{head}</div>
			<div style={{fontSize: 112, fontWeight: 700, color: RED, lineHeight: 1.3}}><CountUp text={num} /></div>
			{note && <div style={{fontSize: 46, color: INK, lineHeight: 1.4}}>{note}</div>}
			{tr && <div style={{fontSize: 30, color: GREY, marginTop: 6}}>{tr}</div>}
		</Box>
		{src && <div style={{position: 'absolute', left: 70, right: 140, top: 1000, fontSize: 26, color: INK, background: 'rgba(255,255,255,.8)', borderRadius: 12, padding: '4px 14px'}}>{src}</div>}
	</Enter>
);
const Photo = ({src, tag}: {src: string; tag?: string; credit?: string}) => {
	const frame = useCurrentFrame();
	const zoom = interpolate(frame, [0, 240], [1, 1.07], {extrapolateRight: 'clamp'});
	return (
		<Enter>
			<div style={{position: 'absolute', left: 60, right: 60, top: 230, height: 700, borderRadius: 32, overflow: 'hidden', boxShadow: '0 18px 50px rgba(30,40,50,.2)'}}>
				<Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />
			</div>
			{tag && <div style={{position: 'absolute', left: 90, top: 200, padding: '6px 24px', borderRadius: 14, background: SUN, fontSize: 36, fontWeight: 700, color: INK}}>{tag}</div>}
			
		</Enter>
	);
};
const Bars = ({title, rows}: {title: string; rows: [string, string, number][]}) => {
	const frame = useCurrentFrame();
	return (
		<Enter>
			<Box>
				<div style={{fontSize: 40, color: INK, marginBottom: 26}}>{title}</div>
				{rows.map(([n, v, p], i) => (
					<div key={n} style={{marginBottom: 26}}>
						<div style={{display: 'flex', justifyContent: 'space-between', fontSize: 38, color: INK}}><span>{n}</span><b>{v}</b></div>
						<div style={{height: 26, borderRadius: 13, background: '#eee', marginTop: 8}}>
							<div style={{height: 26, borderRadius: 13, background: i ? '#8f8f8a' : RED, width: `${interpolate(frame, [4 + i * 5, 28 + i * 5], [0, p], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}%`}} />
						</div>
					</div>
				))}
			</Box>
		</Enter>
	);
};
const Sign = ({t, tr, color = RED}: {t: string; tr: string; color?: string}) => (
	<Enter>
		<Box top={230}>
			<div style={{fontSize: 84, fontWeight: 700, color, lineHeight: 1.4, textAlign: 'center'}}>{t}</div>
			<div style={{fontSize: 40, color: GREY, textAlign: 'center'}}>{tr}</div>
		</Box>
	</Enter>
);
const Word = ({no, t, r}: {no: string; t: string; r: string}) => (
	<Enter>
		<Box top={190}>
			<div style={{textAlign: 'center'}}>
				<div style={{fontSize: 42, color: GREY}}>{no}</div>
				<div style={{fontSize: 104, fontWeight: 700, color: '#ff5a5f', lineHeight: 1.4}}>{t}</div>
				<div style={{fontFamily: 'Rubik', fontSize: 38, color: INK}}>{r}</div>
			</div>
		</Box>
	</Enter>
);
const Answer = ({t, tr}: {t: string; tr: string}) => (
	<Enter>
		<Box top={230} bg={TEAL}>
			<div style={{textAlign: 'center', color: '#fff'}}>
				<div style={{fontSize: 42}}>เฉลย · Answer</div>
				<div style={{fontSize: 74, fontWeight: 700, lineHeight: 1.45}}>{t}</div>
				<div style={{fontSize: 38}}>{tr}</div>
			</div>
		</Box>
	</Enter>
);
const End = () => <Img src={staticFile('logo.png')} style={{position: 'absolute', left: 150, top: 340, width: 780}} />;
const PromptCard = () => (
	<Enter>
		<Box top={230}>
			<div style={{fontSize: 38, color: GREY}}>พรอมต์ · Prompt</div>
			<div style={{marginTop: 20, fontSize: 50, lineHeight: 1.55, color: INK}}>"คลิปนี้ไม่พูดถึงข้อเสียอะไร<br />จุดไหนเหมือนโฆษณา"</div>
		</Box>
	</Enter>
);

const NOTE_TRENDS = 'Google Trends ไทย ม.ค. 2562–ต.ค. 2569 · ดัชนีเปรียบเทียบ';
const ALL_TIKTOK: Shot[] = [
	{at: 0, v: <S.CartIntro />, mood: 'wow'},
	{at: 1, v: <><S.ReviewScene /><Card logo="tiktok" head="ก่อนซื้อ · Before buying" num="66.9%" note="ดูรีวิววิดีโอบน TikTok และโซเชียล" tr="ผลสำรวจ Gen Z ไทย 2,066 คน · JCTU, ABM Connect, YouGov" /></>, mood: 'wow', sfx: 'ding'},
	{at: 2, v: <><S.SearchScene /><Card logo="google" head="ก่อนซื้อ · Before buying" num="21.9%" note="ค้นผ่าน Google" tr="Search on Google" /></>, mood: 'talk'},
	{at: 3, v: <S2.SnoopScene />, mood: 'smug', low: <S2.MemeCat mode="detective" text="ส่องซิ..." />},
	{at: 4, v: <S2.DownLine v={charts.reviewLine} title="คนค้นคำว่า “รีวิว” บน Google" note={NOTE_TRENDS} />, mood: 'shock', low: <ShockCat text="ลดฮวบ!" />, sfx: 'buzzer'},
	{at: 5, v: <S2.DualLine a={charts.reviewPromo.a} b={charts.reviewPromo.b} labelA="รีวิว" labelB="โปรโมชั่น" title="ขยับตามกันระดับอ่อนถึงปานกลาง" note="การเปลี่ยนแปลงรายเดือน ทำให้เรียบ 3 เดือน · Google Trends" />, mood: 'talk', low: <S2.MemeCat mode="detective" text="เอ๊ะ!" />},
	{at: 6, v: <S2.DualLine a={charts.reviewShopee.a} b={charts.reviewShopee.b} colorB="#ee4d2d" labelA="รีวิว" labelB="Shopee" title="แทบไม่ขยับตามกัน" icon={<Logo k="shopee" s={58} />} note="การเปลี่ยนแปลงรายเดือน ทำให้เรียบ 3 เดือน · Google Trends" />, mood: 'smug', low: <S2.MemeCat mode="shrug" text="ไม่รู้ดิ" />},
	{at: 7, v: <><S2.CausationScene /><Sign t="ไปด้วยกัน ≠ สาเหตุ" tr="Correlation isn't causation" color={TEAL} /></>, mood: 'talk'},
	{at: 8, v: <><S.CartScene /><Card head="ซื้อตาม AI บ่อยๆ · Often buy on AI" num="12.1%" note="43.2% ใช้ AI ช่วยหาไอเดีย" /></>, mood: 'smug', low: <Sticker src="gifs/orangecat.gif" text="จริงดิ?" />},
	{at: 9, v: <><S.PaidScene /><Sign t="รีวิวนี้ได้เงินไหม?" tr="Was this review paid?" /></>, mood: 'shock', low: <Bubble t="จ่ายมาเท่าไหร่?" />, sfx: 'buzzer'},
	{at: 10, v: <><S.AiScene /><PromptCard /></>, mood: 'talk'},
	{at: 11, v: <><S.CommentScene /><Sign t="อ่านคอมเมนต์คนซื้อจริง" tr="Read real buyers' comments" color={TEAL} /></>, mood: 'wow', sfx: 'ding'},
	{at: 12, v: <End />},
];
const ALL_MU: Shot[] = [
	{at: 0, v: <S.WishIntro />, mood: 'wow'},
	{at: 1, v: <S2.SnoopScene />, mood: 'smug', low: <S2.MemeCat mode="detective" text="ลุ้น..." />},
	{at: 2, v: <><S.MoneyScene /><Bars title="เรื่องที่ขอ · Top wishes" rows={[['การเงิน · Money', '36.4%', 100], ['ความรัก · Love', '25.3%', 70], ['โชคลาภ · Fortune', '17.2%', 47]]} /></>, mood: 'shock', low: <S2.MemeCat mode="coin" text="เงิน!" />, sfx: 'ding'},
	{at: 3, v: <><S.HalfScene /><Card head="กรุงศรี · สำรวจ 1,213 คน ก.ย.–ต.ค. 2567" num="ราวครึ่ง" note="หันมามูเมื่อมีปัญหาการเงิน" tr="About half turn to it in money trouble" /></>, mood: 'talk'},
	{at: 4, v: <><S2.FortuneScene /><S2.StatBadge num="42.1%" t="Gen Z นิยมดูดวง · กรุงศรี" /></>, mood: 'wow', sfx: 'ding'},
	{at: 5, v: <S2.SnoopScene />, mood: 'smug', low: <S2.MemeCat mode="detective" text="ส่องซิ..." />},
	{at: 6, v: <S2.MonthBars v={charts.fortuneMonths} note={NOTE_TRENDS} />, mood: 'wow', low: <Bubble t="พุ่งมาก!" />, sfx: 'ding'},
	{at: 7, v: <S2.DualLine a={charts.jobFortune.a} b={charts.jobFortune.b} labelA="หางาน" labelB="ดูดวง" title="ไปทางเดียวกันระดับปานกลาง" note="เทียบปีก่อน ทำให้เรียบ 3 เดือน · Google Trends" />, mood: 'talk', low: <S2.MemeCat mode="detective" text="เอ๊ะ!" />},
	{at: 8, v: <><S2.CausationScene /><Sign t="ไปด้วยกัน ≠ สาเหตุ" tr="Correlation isn't causation" color={TEAL} /></>, mood: 'talk'},
	{at: 9, v: <DeityScene />, mood: 'wow', sfx: 'ding'},
	{at: 10, v: <><S.ShirtScene /><Card head="ของมูที่พูดถึงมากสุด · Dataset" num="38.2%" note="เสื้อสีมงคล" tr="Lucky-colour shirts" /></>, mood: 'wow'},
	{at: 11, v: <><S.TransferScene /><Sign t="อย่าเพิ่งโอน" tr="Don't transfer yet" /></>, mood: 'shock', low: <Bubble t="ใจเย็นนะแม่" />, sfx: 'buzzer'},
	{at: 12, v: <><S.AskScene /><Sign t="คุณมูเรื่องอะไร" tr="Tell us below" color={TEAL} /></>, mood: 'talk', low: <Sticker src="gifs/orangecat.gif" text="บอกมา!" />},
	{at: 13, v: <End />},
];
const quizRound = (at: number, no: string, word: string, roman: string, ask: React.ReactNode, askLow: React.ReactNode, decoy: React.ReactNode, decoyLow: React.ReactNode, stamp: string, answer: string, tr: string, scene: React.ReactNode, bubble: string): Shot[] => [
	{at, v: <>{ask}<Word no={no} t={word} r={roman} /></>, mood: 'talk', low: askLow, sfx: 'pop'},
	{at: at + 1, v: decoy, mood: 'smug', low: decoyLow},
	{at: at + 2, v: <>{scene}<Reveal stamp={stamp}><Answer t={answer} tr={tr} /></Reveal></>, mood: 'shock', low: <Bubble t={bubble} />, sfx: 'buzzer', sfx2: 'ding'},
];
const ALL_QUIZ: Shot[] = [
	{at: 0, v: <S.FourIntro />, mood: 'smug'},
	...quizRound(1, 'ข้อ 1', 'เม็ดเยอะ', 'met yoe', <S.SeedsScene />, null, <PapayaScene />, <Sticker src="gifs/orangecat.gif" text="ผลไม้เหรอ?" />, 'ผิดค่ะ!', 'เรื่องมาก', 'Fussy, or unfinished gossip', <S.GossipScene />, 'ไม่ใช่ย่ะแม่!'),
	...quizRound(4, 'ข้อ 2', 'จริงหรือเค้ก', 'jing rue cake', <S.CakeScene />, null, <CakeForkScene />, <ShockCat text="กินเลย?" />, 'ไม่ใช่ย่ะ!', 'จริงหรือเฟก', 'True or fake?', <S.FakeScene />, 'เฟกจ้าแม่!'),
	...quizRound(7, 'ข้อ 3', 'เหยิน', 'yoen', <S.QuestionScene />, null, <ToothScene />, <Sticker src="gifs/funnycat.gif" text="หมอฟันไหม?" />, 'ว้าย!', 'เขินจนยิ้มไม่หุบ', "Can't stop smiling", <S.HeartScene />, 'เขินย่ะ!'),
	...quizRound(10, 'ข้อสุดท้าย', 'ชีเสิร์ฟ', 'she serve', <S.TrayScene />, null, <FoodScene />, <Sticker src="gifs/orangecat.gif" text="ออเดอร์ไหน?" tilt={-5} />, 'ตายแล้ว!', 'ทำได้ปังมาก', 'She nailed it', <><S.SparkleScene /><FireworkSticker /></>, 'เริ่ดมากแม่!'),
	{at: 13, v: <><S.QuestionScene /><Sign t="ได้กี่ข้อแม่?" tr="How many did you get?" color={TEAL} /></>, mood: 'wow', low: <Bubble t="คอมเมนต์มา!" />, sfx: 'ding'},
	{at: 14, v: <End />},
];

export const clips: Clip[] = [
	{id: 'tiktok-vs-google', dir: 'reel-tiktok-vs-google', subs: tiktokSubs as Sub[], accent: TEAL, who: 'viewer', shots: ALL_TIKTOK},
	{id: 'mutelu', dir: 'reel-mutelu', subs: muteluSubs as Sub[], accent: '#b57edc', who: 'mu', shots: ALL_MU},
	{id: 'slang-quiz', dir: 'reel-slang-quiz', subs: slangSubs as Sub[], accent: '#ff5a5f', who: 'host', shots: ALL_QUIZ},
];

const IntroLogo = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const p = spring({frame, fps, config: {damping: 13, stiffness: 130}});
	const out = interpolate(frame, [110, 120], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<div style={{position: 'absolute', left: 530, top: 1400, width: 390, padding: 22, borderRadius: 28, background: '#fff', boxShadow: '0 14px 36px rgba(0,0,0,.18)', opacity: out, transform: `scale(${p})`}}>
			<Img src={staticFile('logo.png')} style={{width: '100%', display: 'block'}} />
		</div>
	);
};

const FPS = 30;
export const durationFrames = (c: Clip) => Math.ceil((c.subs[c.subs.length - 1].start + 5) * FPS);

const Caption = ({s}: {s: Sub}) => {
	const frame = useCurrentFrame();
	const a = (s.in ?? s.start) - s.start, b = (s.out ?? s.end) - s.start;
	const parts = s.show.replace(/\|/g, ' ¶ ').split(/(\*[^*]+\*)/).filter(Boolean);
	const words = parts.flatMap((x) => (x.startsWith('*') ? [{w: x.slice(1, -1), hot: true}] : x.trim().split(/\s+/).filter(Boolean).map((w) => ({w, hot: false}))));
	const at = interpolate(frame / FPS, [a, Math.max(a + 0.1, b)], [0, words.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<div style={{position: 'absolute', left: 60, right: 120, top: 1090, textAlign: 'center'}}>
			<div style={{fontSize: 56, fontWeight: 700, color: '#16202a', lineHeight: 1.45}}>
				{words.map((x, i) => <span key={i} style={{color: x.hot ? RED : '#16202a', opacity: interpolate(at - i, [0, 0.7], [0.28, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>{x.w === '¶' ? <br /> : x.w}{' '}</span>)}
			</div>
			<div style={{fontFamily: 'Rubik', fontSize: 34, color: GREY, marginTop: 8, lineHeight: 1.35}}>{s.sub}</div>
		</div>
	);
};

export const Reel: React.FC<{clipId: string}> = ({clipId}) => {
	const c = clips.find((x) => x.id === clipId)!;
	const total = durationFrames(c);
	const fr = (i: number) => (i === 0 ? 0 : Math.round(c.subs[i].start * FPS));
	const last = c.subs.length - 1;
	const frame = useCurrentFrame();
	const now = frame / FPS;
	return (
		<AbsoluteFill style={{background: '#fffdf4', fontFamily: 'Mitr, Rubik', fontWeight: 500}}>
			<Audio src={staticFile(`${c.dir}/narration.wav`)} />
			<Audio src={staticFile(`${c.dir}/pad.wav`)} volume={0.11} />
			{c.shots.map((s, n) => {
				const start = fr(s.at);
				const end = n + 1 < c.shots.length ? fr(c.shots[n + 1].at) : total;
				return (
					<Sequence key={s.at} from={start} durationInFrames={end - start} layout="none">
						<AbsoluteFill>
							{s.at !== last && (
								<svg width={1080} height={1920} style={{position: 'absolute'}}>
									<circle cx={950} cy={1750} r={260} fill={SUN} opacity={0.3} />
									<circle cx={110} cy={1620} r={150} fill={c.accent} opacity={0.2} />
								</svg>
							)}
							{s.v}
						</AbsoluteFill>
					</Sequence>
				);
			})}
			{c.shots.filter((s) => s.mood).map((s) => {
				const start = fr(s.at);
				const end = s.at < last ? fr(s.at + 1) : total;
				const sub = c.subs[s.at];
				const talking = now >= (sub.in ?? sub.start) && now <= (sub.out ?? sub.end);
				return (
					<Sequence key={`p${s.at}`} from={start} durationInFrames={end - start} layout="none">
						<Person kind={c.who} mood={s.mood!} talking={talking} />
						{s.low}
						{s.sfx && <Audio src={staticFile(`sfx/${s.sfx}.wav`)} volume={0.45} />}
						{s.sfx2 && <Sequence from={20} layout="none"><Audio src={staticFile(`sfx/${s.sfx2}.wav`)} volume={0.45} /></Sequence>}
					</Sequence>
				);
			})}
			<Sequence from={0} durationInFrames={120} layout="none"><IntroLogo /></Sequence>
			{c.subs.map((s, i) => (
				<Sequence key={i} from={fr(i)} durationInFrames={(i < last ? fr(i + 1) : total) - fr(i)} layout="none">
					<Caption s={s} />
				</Sequence>
			))}
		</AbsoluteFill>
	);
};

const COVERS: Record<string, {who: 'host' | 'viewer' | 'mu'; mood: Mood; art: React.ReactNode; kicker: string; title: string; hot: string; sub: string; stamp?: string}> = {
	'cover-mutelu': {who: 'mu', mood: 'wow', art: <DeityScene />, kicker: 'สายมู · Gen Z', title: 'คนไทยขอพรเรื่องไหน', hot: 'มากที่สุด?', sub: 'คำตอบอาจไม่ใช่เรื่องที่คุณคิด'},
	'cover-buy': {who: 'viewer', mood: 'shock', art: <S.CartIntro />, kicker: 'ส่องการค้นหาย้อน 8 ปี', title: 'ของในตะกร้าคุณ', hot: 'มาจากคลิปเดียว?', sub: 'ดูจนจบแล้วรู้ทันรีวิว'},
	'cover-quiz': {who: 'host', mood: 'smug', art: <S.FourIntro />, kicker: 'ควิซศัพท์วัยรุ่น', title: 'แค่สี่คำนี้', hot: 'รู้ไหมแม่?', sub: 'ตอบผิดไม่ว่า แต่อายนะ', stamp: 'ผิดค่ะ!'},
};
export const coverIds = Object.keys(COVERS);
export const Cover: React.FC<{id: string}> = ({id}) => {
	const c = COVERS[id];
	return (
		<AbsoluteFill style={{background: '#fffdf4', fontFamily: 'Mitr, Rubik', fontWeight: 500}}>
			<svg width={1080} height={1920} style={{position: 'absolute'}}>
				<circle cx={950} cy={1750} r={260} fill={SUN} opacity={0.3} />
				<circle cx={110} cy={1620} r={150} fill={TEAL} opacity={0.2} />
			</svg>
			{c.art}
			{c.stamp && <div style={{position: 'absolute', left: 280, top: 420, padding: '14px 44px', border: '14px solid #e0263a', borderRadius: 30, background: 'rgba(255,255,255,.96)', fontSize: 118, fontWeight: 700, color: '#e0263a', transform: 'rotate(-8deg)'}}>{c.stamp}</div>}
			<div style={{position: 'absolute', left: 50, right: 50, top: 950, padding: '20px 30px', borderRadius: 40, background: '#fff', textAlign: 'center', boxShadow: '0 18px 50px rgba(30,40,50,.2)'}}>
				<div style={{display: 'inline-block', padding: '4px 26px', borderRadius: 30, background: SUN, fontSize: 38, fontWeight: 700, color: INK}}>{c.kicker}</div>
				<div style={{fontSize: 92, fontWeight: 700, color: '#16202a', lineHeight: 1.3, marginTop: 8}}>{c.title}</div>
				<div style={{fontSize: 108, fontWeight: 700, color: RED, lineHeight: 1.25}}>{c.hot}</div>
				<div style={{fontSize: 40, color: GREY, marginTop: 6}}>{c.sub}</div>
			</div>
			<Person kind={c.who} mood={c.mood} talking={false} />
			<div style={{position: 'absolute', left: 530, top: 1480, width: 390, padding: 22, borderRadius: 28, background: '#fff', boxShadow: '0 14px 36px rgba(0,0,0,.18)'}}>
				<Img src={staticFile('logo.png')} style={{width: '100%', display: 'block'}} />
			</div>
		</AbsoluteFill>
	);
};
