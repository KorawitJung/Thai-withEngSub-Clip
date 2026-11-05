import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export const SUN = '#ffc93c', CORAL = '#ff5a5f', TEAL = '#12a594', SKY = '#7fd6f5', INK = '#23323a', CREAM = '#fffdf4', PURPLE = '#8f6fd8';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

const usePop = (delay = 0) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return spring({frame: frame - delay, fps, config: {damping: 12, stiffness: 140}});
};
export const Pop: React.FC<{x: number; y: number; delay?: number; children: React.ReactNode}> = ({x, y, delay = 0, children}) => {
	const p = usePop(delay);
	return <g transform={`translate(${x} ${y}) scale(${p})`} opacity={Math.min(1, p * 2)}>{children}</g>;
};
export const Float: React.FC<{amp?: number; speed?: number; phase?: number; children: React.ReactNode}> = ({amp = 10, speed = 0.08, phase = 0, children}) => {
	const f = useCurrentFrame();
	return <g transform={`translate(0 ${Math.sin(f * speed + phase) * amp})`}>{children}</g>;
};
export const Stage: React.FC<{top?: string; bottom?: string; floor?: string; children: React.ReactNode}> = ({top = CREAM, bottom = CREAM, floor, children}) => {
	const id = `g${top.slice(1)}${bottom.slice(1)}`;
	return (
		<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
			<defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={top} /><stop offset="1" stopColor={bottom} /></linearGradient></defs>
			<rect width={1080} height={1060} fill={`url(#${id})`} />
			{floor && <rect y={1000} width={1080} height={60} fill={floor} />}
			{children}
		</svg>
	);
};
const Sunset: React.FC<{children: React.ReactNode}> = ({children}) => <Stage top="#ff9e7a" bottom="#ffe08a" floor="#ffe9b0">{children}</Stage>;
const Night: React.FC<{children: React.ReactNode}> = ({children}) => <Stage top="#3f5fb0" bottom="#a07aa8">{children}</Stage>;
const Sky: React.FC<{children: React.ReactNode}> = ({children}) => <Stage top="#bdeaf8" bottom="#fff6dd" floor="#fff0c2">{children}</Stage>;

const PhoneBody: React.FC<{x: number; y: number; s?: number; screen?: string; children?: React.ReactNode}> = ({x, y, s = 1, screen = '#fff', children}) => (
	<g transform={`translate(${x} ${y}) scale(${s})`}>
		<rect x={-120} y={-210} width={240} height={420} rx={36} fill={INK} />
		<rect x={-104} y={-190} width={208} height={380} rx={20} fill={screen} />
		{children}
	</g>
);
export const Star = ({x, y, s = 1, fill = SUN}: {x: number; y: number; s?: number; fill?: string}) => (
	<path transform={`translate(${x} ${y}) scale(${s})`} fill={fill} d="M0-30 9-10 31-8 14 7 19 29 0 17-19 29-14 7-31-8-9-10Z" />
);
export const Coin = ({x, y, r = 34}: {x: number; y: number; r?: number}) => (
	<g transform={`translate(${x} ${y})`}><circle r={r} fill={SUN} stroke="#e0a100" strokeWidth={6} /><text textAnchor="middle" y={r * 0.38} fontSize={r * 1.1} fontWeight={700} fill="#b37e00">฿</text></g>
);
export const Rain: React.FC<{n?: number; children: (x: number, y: number, i: number) => React.ReactNode}> = ({n = 9, children}) => {
	const f = useCurrentFrame();
	return <>{Array.from({length: n}, (_, i) => children(80 + ((i * 397) % 920), ((f * (5 + (i % 3) * 2) + i * 137) % 430) + 600, i))}</>;
};
const Heart = ({x, y, s = 1}: {x: number; y: number; s?: number}) => <path transform={`translate(${x} ${y}) scale(${s})`} fill={CORAL} d="M0 26C-40-6-26-34-8-30-3-29 0-24 0-20 0-24 3-29 8-30 26-34 40-6 0 26Z" />;

export const ReviewScene = () => {
	const f = useCurrentFrame();
	const pulse = 1 + Math.sin(f * 0.2) * 0.08;
	return <Sunset><circle cx={540} cy={800} r={230} fill={SUN} /><Pop x={0} y={0}><PhoneBody x={540} y={800} s={0.82} screen="#10151a"><circle r={56} fill="#fff" transform={`scale(${pulse})`} /><path d="M-16-26 28 0-16 26Z" fill={CORAL} /><rect x={-84} y={140} width={168} height={10} rx={5} fill="#555" /><rect x={-84} y={140} width={interpolate(f, [0, 110], [0, 168], clamp)} height={10} rx={5} fill={CORAL} /></PhoneBody></Pop>{[0, 1, 2, 3, 4].map((i) => <Pop key={i} x={[190, 300, 780, 890, 540][i]} y={[800, 680, 680, 800, 1020][i]} delay={8 + i * 5}><Star x={0} y={0} s={1.5} /></Pop>)}</Sunset>;
};
export const SearchScene = () => {
	const f = useCurrentFrame();
	const text = 'รีวิวก่อนซื้อ';
	const shown = Array.from(text).slice(0, Math.floor(interpolate(f, [8, 50], [0, text.length], clamp))).join('');
	return <Sky><Pop x={540} y={800}><g><rect x={-400} y={-62} width={800} height={124} rx={62} fill="#fff" stroke="#4285F4" strokeWidth={8} /><text x={-340} y={22} fontSize={60} fill={INK}>{shown}{f % 20 < 10 ? '|' : ''}</text><circle cx={320} r={30} fill="none" stroke="#4285F4" strokeWidth={10} /><path d="M342 22 372 52" stroke="#4285F4" strokeWidth={12} strokeLinecap="round" /></g></Pop></Sky>;
};
export const PeopleScene = () => <Sky>{Array.from({length: 40}, (_, i) => <Pop key={i} x={150 + (i % 10) * 88} y={670 + Math.floor(i / 10) * 92} delay={i * 1.1}><circle cy={-22} r={15} fill={i % 3 ? TEAL : CORAL} /><path d="M-22 26C-22-8 22-8 22 26Z" fill={i % 3 ? TEAL : CORAL} /></Pop>)}</Sky>;
export const AiScene = () => {
	const f = useCurrentFrame();
	return <Night><Pop x={540} y={830}><g transform={`rotate(${Math.sin(f * 0.05) * 4})`}><circle r={150} fill={TEAL} /><circle cx={-50} cy={-20} r={24} fill="#fff" /><circle cx={50} cy={-20} r={24} fill="#fff" /><path d="M-50 50Q0 90 50 50" stroke="#fff" strokeWidth={14} fill="none" strokeLinecap="round" /></g></Pop>{[[230, 720], [850, 700], [200, 950], [880, 930]].map(([x, y], i) => <Pop key={i} x={x} y={y} delay={8 + i * 6}><Float phase={i}><Star x={0} y={0} s={1.3 + (i % 2) * 0.5} /></Float></Pop>)}</Night>;
};
export const CartScene = () => {
	const f = useCurrentFrame();
	const x = interpolate(f, [0, 40], [-200, 540], {...clamp, easing: (t) => 1 - (1 - t) ** 3});
	return <Sky><g transform={`translate(${x} 880)`}><path d="M-170-110H-120L-80 60H110L150-60H-105" fill="#fff" stroke={INK} strokeWidth={16} strokeLinejoin="round" /><circle cx={-60} cy={105} r={26} fill={INK} /><circle cx={90} cy={105} r={26} fill={INK} /></g><Pop x={780} y={720} delay={38}><circle r={62} fill={TEAL} /><text textAnchor="middle" y={22} fontSize={62} fill="#fff" fontWeight={700}>AI</text></Pop></Sky>;
};
export const TrustScene = () => <Sunset><circle cx={540} cy={800} r={220} fill={SUN} /><Pop x={380} y={830}><circle cy={-90} r={68} fill={INK} /><path d="M-100 150C-100-20 100-20 100 150Z" fill={CORAL} /></Pop><Pop x={720} y={860} delay={8}><circle r={70} fill={TEAL} opacity={0.75} /><text textAnchor="middle" y={20} fontSize={54} fill="#fff" fontWeight={700}>AI</text></Pop><Pop x={380} y={630} delay={14}><Heart x={0} y={0} s={2.2} /></Pop></Sunset>;
export const PaidScene = () => <Sky><Rain>{(x, y, i) => <Coin key={i} x={x} y={y} />}</Rain><Pop x={540} y={840}><PhoneBody x={0} y={0} s={0.8} screen="#10151a"><circle r={46} fill="#fff" /><path d="M-13-22 24 0-13 22Z" fill={CORAL} /></PhoneBody></Pop></Sky>;
export const CommentScene = () => <Sky>{['ของจริงดีไหม', 'ใช้มา 3 เดือน', 'ซื้อแล้วเป็นไง'].map((t, i) => <Pop key={t} x={i === 1 ? 640 : 420} y={690 + i * 125} delay={i * 8}><rect x={-250} y={-48} width={500} height={96} rx={48} fill={i === 1 ? TEAL : '#fff'} stroke={INK} strokeWidth={4} /><text textAnchor="middle" y={16} fontSize={44} fill={i === 1 ? '#fff' : INK}>{t}</text></Pop>)}</Sky>;

const Shirt = ({color, x, delay}: {color: string; x: number; delay: number}) => {
	const f = useCurrentFrame();
	return <Pop x={x} y={825} delay={delay}><g transform={`rotate(${Math.sin(f * 0.07 + x) * 6})`}><path d="M0-30V-60Q25-85 30-60" stroke={INK} strokeWidth={8} fill="none" /><path d="M-60-20 0-34 60-20 110 40 70 75 50 50V170H-50V50L-70 75-110 40Z" fill={color} /></g></Pop>;
};
export const ShirtScene = () => <Sky><rect x={60} y={762} width={960} height={10} fill={INK} />{[['#ffd33d', 220], [CORAL, 540], ['#3aa76d', 860]].map(([c, x], i) => <Shirt key={i} color={String(c)} x={Number(x)} delay={i * 7} />)}</Sky>;
export const WindmillScene = () => {
	const f = useCurrentFrame();
	const colors = [CORAL, SUN, TEAL, PURPLE, SKY, '#ff9e7a', CORAL, SUN];
	return <Sky><rect x={530} y={800} width={20} height={230} fill={INK} /><Pop x={540} y={800}><g transform={`rotate(${f * 3})`}>{colors.map((c, i) => <path key={i} transform={`rotate(${i * 45})`} d="M0 0L55-175Q0-210-55-175Z" fill={c} />)}<circle r={22} fill="#fff" stroke={INK} strokeWidth={6} /></g></Pop></Sky>;
};
export const MoneyScene = () => <Stage top="#fff6dd" bottom="#ffe9b0"><Rain n={12}>{(x, y, i) => <Coin key={i} x={x} y={y} r={30 + (i % 3) * 8} />}</Rain></Stage>;
export const GenZScene = () => <Sunset><circle cx={540} cy={830} r={210} fill={SUN} /><Pop x={540} y={820}><PhoneBody x={0} y={0} s={0.9} screen="#fff"><Heart x={0} y={-60} s={1.6} /><Star x={0} y={70} s={1.8} fill={PURPLE} /></PhoneBody></Pop></Sunset>;
export const HalfScene = () => {
	const f = useCurrentFrame();
	const a = interpolate(f, [4, 40], [0, 180], clamp);
	const r = (a * Math.PI) / 180;
	return <Sky><circle cx={540} cy={820} r={190} fill="#e9e4d5" /><path d={`M540 820V630A190 190 0 ${a >= 180 ? 0 : 0} 1 ${540 + 190 * Math.sin(r)} ${820 - 190 * Math.cos(r)}Z`} fill={CORAL} /><Pop x={540} y={820} delay={36}><text textAnchor="middle" y={22} x={90} fontSize={64} fontWeight={700} fill="#fff">50%</text></Pop></Sky>;
};
export const ScamScene = () => {
	const f = useCurrentFrame();
	return <Night><Pop x={540} y={830}><g transform={`rotate(${Math.sin(f * 0.8) * interpolate(f, [0, 30], [8, 2], clamp)})`}><path d="M0-170 190 140H-190Z" fill={SUN} stroke={INK} strokeWidth={14} strokeLinejoin="round" /><rect x={-16} y={-70} width={32} height={120} rx={14} fill={INK} /><circle cy={95} r={20} fill={INK} /></g></Pop></Night>;
};
export const TransferScene = () => <Sky><Pop x={540} y={830}><PhoneBody x={0} y={0} s={0.9} screen="#fff"><Coin x={0} y={-30} r={62} /><rect x={-70} y={70} width={140} height={46} rx={23} fill={TEAL} /></PhoneBody></Pop><Pop x={540} y={830} delay={16}><path d="M-170-170 170 170M170-170-170 170" stroke={CORAL} strokeWidth={34} strokeLinecap="round" /></Pop></Sky>;
export const AskScene = () => <Sunset><circle cx={540} cy={800} r={210} fill={SUN} />{[['ความรัก', 300, 700], ['การเงิน', 770, 760], ['โชคลาภ', 420, 920]].map(([t, x, y], i) => <Pop key={String(t)} x={Number(x)} y={Number(y)} delay={i * 8}><Float phase={i}><rect x={-140} y={-50} width={280} height={100} rx={50} fill="#fff" /><text textAnchor="middle" y={17} fontSize={46} fill={INK}>{t}</text></Float></Pop>)}</Sunset>;

export const SeedsScene = () => {
	const f = useCurrentFrame();
	return <Sky>{Array.from({length: 26}, (_, i) => {
		const y = Math.min(640 + ((i * 23) % 60) + f * (6 + (i % 4)), 980 - (i % 4) * 22);
		return <ellipse key={i} cx={110 + i * 34} cy={y} rx={22} ry={13} fill={i % 2 ? '#7a4a22' : '#a86b34'} transform={`rotate(${i * 40} ${110 + i * 34} ${y})`} />;
	})}</Sky>;
};
export const GossipScene = () => <Sky><Pop x={360} y={800}><path d="M-210-90H210V90H-70L-130 160-120 90H-210Z" fill="#fff" stroke={INK} strokeWidth={8} strokeLinejoin="round" /><circle cx={-70} r={20} fill={CORAL} /><circle r={20} fill={CORAL} /><circle cx={70} r={20} fill={CORAL} /></Pop><Pop x={800} y={760} delay={10}><text textAnchor="middle" fontSize={170} fontWeight={700} fill={TEAL}>?</text></Pop></Sky>;
const Cake = () => <g><rect x={-170} y={-40} width={340} height={150} rx={22} fill="#ffc9d6" /><rect x={-170} y={-40} width={340} height={46} rx={20} fill="#fff" /><rect x={-10} y={-120} width={20} height={80} fill={CORAL} /><path d="M0-160Q22-125 0-115-22-125 0-160Z" fill={SUN} /></g>;
export const CakeScene = () => <Sunset><circle cx={540} cy={790} r={220} fill={SUN} /><Pop x={540} y={860}><Cake /></Pop></Sunset>;
export const FakeScene = () => <Sky><Pop x={320} y={830}><g transform="scale(.75)"><Cake /></g><circle cx={0} cy={-20} r={170} fill="none" stroke={TEAL} strokeWidth={18} /></Pop><Pop x={760} y={830} delay={12}><g transform="scale(.75)"><Cake /></g><path d="M-120-140 120 100M120-140-120 100" stroke={CORAL} strokeWidth={24} strokeLinecap="round" /></Pop></Sky>;
const Face = () => <g><circle r={170} fill={SUN} /><ellipse cx={-85} cy={35} rx={40} ry={24} fill={CORAL} opacity={0.55} /><ellipse cx={85} cy={35} rx={40} ry={24} fill={CORAL} opacity={0.55} /><path d="M-90-40Q-65-70-40-40M40-40Q65-70 90-40" stroke={INK} strokeWidth={13} fill="none" strokeLinecap="round" /><path d="M-90 45Q0 125 90 45Z" fill="#fff" stroke={INK} strokeWidth={10} strokeLinejoin="round" /></g>;
export const BlushScene = () => <Sunset><Pop x={540} y={810}><Float><Face /></Float></Pop></Sunset>;
export const HeartScene = () => {
	const f = useCurrentFrame();
	return <Sky><Pop x={540} y={830}><Face /></Pop>{Array.from({length: 7}, (_, i) => <Heart key={i} x={170 + i * 123} y={1000 - ((f * 5 + i * 90) % 400)} s={0.9 + (i % 3) * 0.4} />)}</Sky>;
};
export const TrayScene = () => <Night><Pop x={540} y={860}><g><ellipse cy={60} rx={260} ry={34} fill="#d7dde2" /><path d="M-190 40Q0-260 190 40Z" fill="#eef1f3" /><circle cy={-115} r={22} fill="#d7dde2" /></g></Pop></Night>;
export const SparkleScene = () => <Sunset><circle cx={540} cy={810} r={220} fill={SUN} />{[[540, 790, 4], [270, 680, 1.8], [810, 690, 2.2], [270, 950, 1.5], [820, 930, 1.8]].map(([x, y, s], i) => <Pop key={i} x={x} y={y} delay={i * 5}><Float phase={i}><Star x={0} y={0} s={s} fill={i ? '#fff' : CORAL} /></Float></Pop>)}</Sunset>;
export const QuestionScene = () => <Sky>{['ก', 'ข', 'ค', 'ง', '?', '!', 'จ'].map((t, i) => <Pop key={i} x={170 + i * 123} y={720 + (i % 3) * 110} delay={i * 4}><Float phase={i}><circle r={54} fill={[CORAL, TEAL, SUN, PURPLE][i % 4]} /><text textAnchor="middle" y={21} fontSize={58} fontWeight={700} fill="#fff">{t}</text></Float></Pop>)}</Sky>;
export const SkyBg = () => <Sky><></></Sky>;
export const CartIntro = () => {
	const f = useCurrentFrame();
	return <Sunset><circle cx={540} cy={560} r={300} fill={SUN} /><Pop x={380} y={560}><PhoneBody x={0} y={0} s={1.05} screen="#10151a"><circle r={54} fill="#fff" /><path d="M-16-26 28 0-16 26Z" fill={CORAL} /></PhoneBody></Pop><g transform={`translate(${interpolate(f, [8, 40], [1250, 780], clamp)} 690)`}><path d="M-150-100H-105L-70 55H100L135-55H-92" fill="#fff" stroke={INK} strokeWidth={15} strokeLinejoin="round" /><circle cx={-50} cy={95} r={24} fill={INK} /><circle cx={80} cy={95} r={24} fill={INK} /></g></Sunset>;
};
export const WishIntro = () => <Night><Pop x={540} y={560} delay={2}><circle r={210} fill={SUN} /><text textAnchor="middle" y={80} fontSize={230} fontWeight={700} fill={INK}>?</text></Pop>{[[190, 340], [890, 300], [170, 800], [900, 790], [540, 180]].map(([x, y], i) => <Pop key={i} x={x} y={y} delay={6 + i * 4}><Float phase={i}><Star x={0} y={0} s={1.6} /></Float></Pop>)}</Night>;
export const FourIntro = () => <Sky>{['1', '2', '3', '4'].map((t, i) => <Pop key={t} x={[320, 760, 320, 760][i]} y={[370, 370, 760, 760][i]} delay={i * 6}><Float phase={i}><circle r={150} fill={[CORAL, TEAL, SUN, PURPLE][i]} /><text textAnchor="middle" y={58} fontSize={165} fontWeight={700} fill="#fff">{t}</text></Float></Pop>)}</Sky>;
