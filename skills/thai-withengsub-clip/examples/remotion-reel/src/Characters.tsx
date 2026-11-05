import React from 'react';
import {Gif} from '@remotion/gif';
import {Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {CORAL, CREAM, Float, INK, Pop, PURPLE, Rain, Star, Stage, SUN, TEAL, Coin} from './Scenes';

const GOLD = '#f2b632', DEEP = '#c98a12', SKIN = '#f2c7a5';

const Rays = ({r = 170, color = SUN}: {r?: number; color?: string}) => {
	const f = useCurrentFrame();
	return (
		<g transform={`rotate(${f * 0.6})`} opacity={0.5}>
			{Array.from({length: 12}, (_, i) => <path key={i} transform={`rotate(${i * 30})`} d={`M-12 ${-r + 30}L0 ${-r - 26}L12 ${-r + 30}Z`} fill={color} />)}
		</g>
	);
};
const Lotus = ({w = 1}: {w?: number}) => (
	<g transform={`scale(${w})`}>
		{[-90, -45, 0, 45, 90].map((x) => <path key={x} d={`M${x} 30Q${x - 42} 0 ${x} -34Q${x + 42} 0 ${x} 30Z`} fill="#ff9fc0" stroke="#e8749e" strokeWidth={3} />)}
		<ellipse cy={32} rx={132} ry={16} fill="#3f9c6d" />
	</g>
);
const Crown = ({h = 74, w = 40}: {h?: number; w?: number}) => (
	<g>
		<path d={`M${-w} 0L${-w * 0.42} ${-h * 0.38}L0 ${-h}L${w * 0.42} ${-h * 0.38}L${w} 0Z`} fill={GOLD} stroke={DEEP} strokeWidth={3} />
		<circle cy={-14} r={7} fill={CORAL} />
	</g>
);
const CalmEyes = ({x = 20, y = 0}: {x?: number; y?: number}) => (
	<path d={`M${-x - 9} ${y}Q${-x} ${y + 8} ${-x + 9} ${y}M${x - 9} ${y}Q${x} ${y + 8} ${x + 9} ${y}`} stroke={INK} strokeWidth={4} fill="none" strokeLinecap="round" />
);

export const PhraPhrom = () => (
	<g>
		<Rays />
		<circle r={150} cy={-30} fill="#fff2bf" opacity={0.75} />
		<g transform="translate(0 120)"><Lotus /></g>
		<path d="M-96 106Q-90 44-48 30H48Q90 44 96 106Q0 128-96 106Z" fill={GOLD} stroke={DEEP} strokeWidth={3} />
		<path d="M-44 32Q-52 -18-34 -40H34Q52 -18 44 32Z" fill={GOLD} stroke={DEEP} strokeWidth={3} />
		<path d="M-38-30Q-92-34-104-84M38-30Q92-34 104-84M-40-6Q-88 8-100 54M40-6Q88 8 100 54" stroke={GOLD} strokeWidth={17} fill="none" strokeLinecap="round" />
		<circle cx={-104} cy={-92} r={13} fill={CREAM} stroke={DEEP} strokeWidth={3} />
		<circle cx={104} cy={-92} r={13} fill={CREAM} stroke={DEEP} strokeWidth={3} />
		<g transform="translate(-52 -74) scale(.78)"><circle r={36} fill={GOLD} stroke={DEEP} strokeWidth={3} /><g transform="translate(0 -28)"><Crown h={56} w={30} /></g></g>
		<g transform="translate(52 -74) scale(.78)"><circle r={36} fill={GOLD} stroke={DEEP} strokeWidth={3} /><g transform="translate(0 -28)"><Crown h={56} w={30} /></g></g>
		<circle cy={-76} r={42} fill="#f8cc58" stroke={DEEP} strokeWidth={3} />
		<CalmEyes y={-80} x={17} />
		<path d="M-10-58Q0-52 10-58" stroke={INK} strokeWidth={3.5} fill="none" strokeLinecap="round" />
		<g transform="translate(0 -110)"><Crown /></g>
	</g>
);

export const Ganesha = () => {
	const f = useCurrentFrame();
	return (
		<g>
			<Rays color="#ffb3cf" />
			<circle r={150} cy={-30} fill="#ffe6ef" opacity={0.8} />
			<g transform="translate(0 120)"><Lotus /></g>
			<path d="M-82 110Q-96 30-46 8H46Q96 30 82 110Q0 130-82 110Z" fill="#ff8fb3" stroke="#d9608b" strokeWidth={3} />
			<ellipse cy={72} rx={62} ry={44} fill="#ffa8c6" />
			<path d="M-44 16Q-92 14-104 -32M44 16Q92 14 104 -32M-52 46Q-98 66-96 92M52 46Q98 66 96 92" stroke="#ff8fb3" strokeWidth={18} fill="none" strokeLinecap="round" />
			<circle cx={-104} cy={-40} r={14} fill={GOLD} />
			<circle cx={104} cy={-40} r={14} fill={GOLD} />
			<ellipse cx={-66} cy={-62} rx={46} ry={54} fill="#ff8fb3" stroke="#d9608b" strokeWidth={3} />
			<ellipse cx={66} cy={-62} rx={46} ry={54} fill="#ff8fb3" stroke="#d9608b" strokeWidth={3} />
			<circle cy={-70} r={50} fill="#ffa8c6" stroke="#d9608b" strokeWidth={3} />
			<CalmEyes y={-80} x={22} />
			<path transform={`rotate(${Math.sin(f * 0.07) * 3} 0 -60)`} d="M0-62Q-16-18 6 2Q26 16 34-4" stroke="#ff8fb3" strokeWidth={22} fill="none" strokeLinecap="round" />
			<path d="M22-46L38-22L24-26Z" fill={CREAM} stroke="#d9608b" strokeWidth={2} />
			<g transform="translate(0 -112)"><Crown h={70} w={38} /></g>
		</g>
	);
};

export const Lakshmi = ({coins = false}: {coins?: boolean}) => {
	const f = useCurrentFrame();
	return (
		<g>
			<Rays />
			<circle r={150} cy={-30} fill="#fff2bf" opacity={0.75} />
			<g transform="translate(0 120)"><Lotus /></g>
			<path d="M-88 110Q-82 30-38 8H38Q82 30 88 110Q0 128-88 110Z" fill={CORAL} stroke="#c93b45" strokeWidth={3} />
			<path d="M-34 8Q0 66 34 8" fill="none" stroke={GOLD} strokeWidth={8} />
			<path d="M-36 14Q-82 12-98-34M36 14Q82 12 98-34M-40 40Q-74 56-58 76M40 40Q74 56 58 76" stroke={SKIN} strokeWidth={16} fill="none" strokeLinecap="round" />
			<path d="M-98-40Q-112-66-98-82Q-84-66-98-40ZM98-40Q84-66 98-82Q112-66 98-40Z" fill="#ff9fc0" />
			<path d="M-50-40Q-58-96-22-114H22Q58-96 50-40Q44-8 0-8Q-44-8-50-40Z" fill="#2c2233" />
			<circle cy={-62} r={38} fill={SKIN} />
			<circle cy={-78} r={4} fill={CORAL} />
			<CalmEyes y={-66} x={15} />
			<path d="M-9-44Q0-38 9-44" stroke="#c93b45" strokeWidth={3.5} fill="none" strokeLinecap="round" />
			<g transform="translate(0 -98)"><Crown h={66} w={34} /></g>
			{coins && Array.from({length: 4}, (_, i) => <Coin key={i} x={58 + i * 5} y={82 + ((f * 3 + i * 26) % 95)} r={14} />)}
		</g>
	);
};

export const PhraKhrueang = () => (
	<g>
		<path d="M-44-84Q0-136 44-84" fill="none" stroke={DEEP} strokeWidth={5} strokeDasharray="4 7" />
		<circle cy={-78} r={9} fill="none" stroke={DEEP} strokeWidth={5} />
		<path d="M-58 72V-22Q-58-72 0-72Q58-72 58-22V72Z" fill={GOLD} stroke={DEEP} strokeWidth={5} />
		<path d="M-44 60V-18Q-44-58 0-58Q44-58 44-18V60Z" fill="#6a5a44" />
		<circle cy={-22} r={15} fill="#d9c28a" />
		<path d="M-26 44Q-28 6 0 2Q28 6 26 44Z" fill="#d9c28a" />
	</g>
);
export const Takrut = () => (
	<g transform="rotate(-18)">
		<path d="M-78 0H78" stroke={CORAL} strokeWidth={8} />
		<rect x={-50} y={-19} width={100} height={38} rx={8} fill="#c9ced4" stroke="#8c949c" strokeWidth={4} />
		{[-28, -8, 12, 32].map((x) => <path key={x} d={`M${x}-18V18`} stroke={CORAL} strokeWidth={6} />)}
	</g>
);
export const NangKwak = () => {
	const f = useCurrentFrame();
	return (
		<g>
			<ellipse cy={64} rx={58} ry={13} fill={DEEP} />
			<path d="M-50 62Q-46 0-16-8H16Q46 0 50 62Z" fill={CORAL} stroke="#c93b45" strokeWidth={3} />
			<circle cy={-32} r={26} fill={SKIN} />
			<path d="M-26-36Q-24-66 0-66Q24-66 26-36Q0-52-26-36Z" fill="#2c2233" />
			<g transform="translate(0 -74)"><Crown h={32} w={18} /></g>
			<CalmEyes y={-30} x={10} />
			<path transform={`rotate(${Math.sin(f * 0.22) * 18} 24 4)`} d="M20 4Q46 -8 42-38" stroke={SKIN} strokeWidth={13} fill="none" strokeLinecap="round" />
		</g>
	);
};
export const Bracelet = () => (
	<g>
		{Array.from({length: 12}, (_, i) => {
			const a = (i * Math.PI) / 6;
			return <circle key={i} cx={Math.cos(a) * 54} cy={Math.sin(a) * 54} r={17} fill={[PURPLE, TEAL, SUN, CORAL][i % 4]} stroke={INK} strokeWidth={2} />;
		})}
	</g>
);
export const Omamori = () => (
	<g>
		<rect x={-44} y={-50} width={88} height={118} rx={12} fill={CORAL} stroke="#a82931" strokeWidth={4} />
		<rect x={-30} y={-36} width={60} height={90} rx={6} fill="none" stroke={GOLD} strokeWidth={4} />
		<path d="M-24-52Q0-92 24-52" fill="none" stroke={GOLD} strokeWidth={7} />
		<Star x={0} y={10} s={0.8} />
	</g>
);

export const DeityScene = () => (
	<Stage top="#3f4fa8" bottom="#d9a0b8">
		<Pop x={210} y={350}><Float phase={0} amp={8} speed={0.05}><g transform="scale(.92)"><Ganesha /></g></Float></Pop>
		<Pop x={540} y={310} delay={8}><Float phase={2} amp={8} speed={0.05}><PhraPhrom /></Float></Pop>
		<Pop x={870} y={350} delay={16}><Float phase={4} amp={8} speed={0.05}><g transform="scale(.92)"><Lakshmi /></g></Float></Pop>
		<rect y={660} width={1080} height={400} fill="#fff6dd" opacity={0.92} />
		<Pop x={160} y={850} delay={55}><PhraKhrueang /></Pop>
		<Pop x={350} y={850} delay={65}><Takrut /></Pop>
		<Pop x={540} y={850} delay={75}><NangKwak /></Pop>
		<Pop x={730} y={850} delay={85}><Bracelet /></Pop>
		<Pop x={920} y={850} delay={95}><Omamori /></Pop>
	</Stage>
);
export const WishMoneyScene = () => (
	<Stage top="#fff6dd" bottom="#ffe9b0">
		<Rain n={8}>{(x, y, i) => <Coin key={i} x={Math.min(x, 600)} y={y} r={26 + (i % 3) * 6} />}</Rain>
		<Pop x={830} y={880}><g transform="scale(.82)"><Lakshmi coins /></g></Pop>
	</Stage>
);

export type Mood = 'talk' | 'smug' | 'shock' | 'wow';
type Kind = 'host' | 'viewer' | 'mu';
const LOOK = {
	host: {hair: '#b0379c', top: '#7a3fe0', lip: '#e0246a'},
	viewer: {hair: '#2a3140', top: TEAL, lip: '#b84c50'},
	mu: {hair: '#3a2a25', top: '#ffd33d', lip: '#c9505c'},
};
export const Person: React.FC<{kind: Kind; mood: Mood; talking: boolean}> = ({kind, mood, talking}) => {
	const f = useCurrentFrame();
	const look = LOOK[kind];
	const bob = Math.sin(f * 0.1) * 6 + (mood === 'shock' ? Math.sin(f * 1.1) * 3 : 0);
	const tilt = kind === 'host' ? Math.sin(f * 0.06) * 5 - 3 : Math.sin(f * 0.05) * 2;
	const open = talking ? Math.abs(Math.sin(f * 0.75)) * 19 + 5 : 0;
	return (
		<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
			<g transform={`translate(270 ${1560 + bob})`}>
				<path d="M-170 380Q-170 150-70 120H70Q170 150 170 380Z" fill={look.top} />
				{kind === 'host' && <>{Array.from({length: 14}, (_, i) => <circle key={i} cx={-105 + (i * 67) % 210} cy={165 + (i * 37) % 170} r={5} fill="#fff" opacity={0.25 + 0.65 * Math.abs(Math.sin(f * 0.15 + i))} />)}</>}
				{kind === 'mu' && <g transform="translate(0 150) scale(.42)"><PhraKhrueang /></g>}
				<g transform={`rotate(${tilt})`}>
					{kind === 'viewer'
						? <path d="M-96-20Q-112-138 0-142Q112-138 96-20Q70-96 0-96Q-70-96-96-20Z" fill={look.hair} />
						: <path d="M-122 120Q-146-136 0-146Q146-136 122 120Q130 150 92 136L70 40H-70L-92 136Q-130 150-122 120Z" fill={look.hair} />}
					<rect x={-28} y={70} width={56} height={62} fill={SKIN} />
					<circle r={94} fill={SKIN} />
					{kind !== 'viewer' && <path d="M-94-14Q-70-92 0-98Q70-92 94-14Q40-66-8-58Q-54-52-94-14Z" fill={look.hair} />}
					{kind === 'viewer' && <path d="M-92-22Q-50-100 8-92Q72-86 92-22Q30-64-92-22Z" fill={look.hair} />}
					{kind === 'host' && <><g transform="translate(0 -84) scale(1.15)"><Crown h={50} w={40} /></g><circle cx={-94} cy={30} r={14} fill={GOLD} /><circle cx={94} cy={30} r={14} fill={GOLD} /></>}
					{mood === 'shock'
						? <><circle cx={-36} cy={-4} r={25} fill="#fff" stroke={INK} strokeWidth={4} /><circle cx={36} cy={-4} r={25} fill="#fff" stroke={INK} strokeWidth={4} /><circle cx={-36} cy={-2} r={9} fill={INK} /><circle cx={36} cy={-2} r={9} fill={INK} /></>
						: mood === 'smug'
							? <><path d="M-58-6Q-36-16-14-6" stroke={INK} strokeWidth={8} fill="none" strokeLinecap="round" /><circle cx={36} cy={-4} r={16} fill={INK} /><circle cx={41} cy={-9} r={5} fill="#fff" /><path d="M16-40Q40-58 62-36" stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" /></>
							: <><circle cx={-36} cy={-4} r={16} fill={INK} /><circle cx={36} cy={-4} r={16} fill={INK} /><circle cx={-31} cy={-9} r={5} fill="#fff" /><circle cx={41} cy={-9} r={5} fill="#fff" /></>}
					{kind === 'host' && mood !== 'shock' && <path d="M-58-16L-68-28M-46-22L-52-36M18-20L8-32M58-18L70-30" stroke={INK} strokeWidth={4} strokeLinecap="round" />}
					<ellipse cx={-58} cy={28} rx={18} ry={10} fill={CORAL} opacity={0.35} />
					<ellipse cx={58} cy={28} rx={18} ry={10} fill={CORAL} opacity={0.35} />
					{mood === 'shock'
						? <ellipse cy={48} rx={22} ry={28} fill="#7a1f2a" stroke={look.lip} strokeWidth={6} />
						: open > 0
							? <ellipse cy={48} rx={18} ry={Math.min(open, 17)} fill="#7a1f2a" stroke={look.lip} strokeWidth={4} />
							: <path d="M-30 40Q0 70 30 40" stroke={look.lip} strokeWidth={8} fill="none" strokeLinecap="round" />}
				</g>
				{kind === 'viewer' && <g transform={`translate(110 ${150 + Math.sin(f * 0.08) * 6}) rotate(8)`}><rect x={-46} y={-80} width={92} height={160} rx={16} fill={INK} /><rect x={-36} y={-68} width={72} height={134} rx={8} fill={SUN} /><path d="M-11-22 20 0-11 22Z" fill={CORAL} /></g>}
				{kind === 'mu' && <><path d="M-128 240Q-90 300-14 262M128 240Q90 300 14 262" stroke={SKIN} strokeWidth={30} fill="none" strokeLinecap="round" /><path d="M-15 282Q-18 220 0 192Q18 220 15 282Z" fill={SKIN} stroke="#d9a784" strokeWidth={3} /><path d="M0 196V280" stroke="#d9a784" strokeWidth={3} /></>}
				{kind === 'host' && <g transform={`translate(150 170) rotate(${Math.sin(f * 0.45) * 13})`}><path d="M0 0L-58-104Q0-140 58-104Z" fill={CORAL} stroke="#a82931" strokeWidth={4} />{[-30, -10, 10, 30].map((x) => <path key={x} d={`M0 0L${x}-112`} stroke="#fff" strokeWidth={3} opacity={0.7} />)}<circle r={18} fill={SKIN} /></g>}
			</g>
		</svg>
	);
};

const useSpring = (delay = 0) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	return spring({frame: f - delay, fps, config: {damping: 10, stiffness: 170}});
};
const memeText: React.CSSProperties = {fontWeight: 700, color: '#fff', WebkitTextStroke: '9px #16202a', paintOrder: 'stroke fill', textAlign: 'center'};

export const Sticker: React.FC<{src: string; text?: string; w?: number; h?: number; rate?: number; tilt?: number}> = ({src, text, w = 380, h = 380, rate = 1, tilt = 5}) => {
	const p = useSpring();
	return (
		<div style={{position: 'absolute', left: 520, top: 1370, width: w, height: h, transform: `scale(${p}) rotate(${tilt}deg)`, background: '#fff', padding: 12, borderRadius: 22, boxShadow: '0 16px 40px rgba(0,0,0,.28)', overflow: 'hidden'}}>
			<Gif src={staticFile(src)} width={w - 24} height={h - 24} fit="cover" playbackRate={rate} style={{borderRadius: 12}} />
			{text && <div style={{...memeText, position: 'absolute', left: 10, right: 10, bottom: 18, fontSize: 56}}>{text}</div>}
		</div>
	);
};
export const ShockCat = ({text = 'เฮ้ย!'}: {text?: string}) => {
	const p = useSpring();
	const f = useCurrentFrame();
	return (
		<svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
			<g transform={`translate(710 ${1570 + Math.sin(f * 1.2) * 4}) scale(${p})`}>
				<path d="M-115-60L-130-170L-40-112ZM115-60L130-170L40-112Z" fill="#f2994a" stroke={INK} strokeWidth={7} strokeLinejoin="round" />
				<ellipse rx={138} ry={120} fill="#f2994a" stroke={INK} strokeWidth={7} />
				<circle cx={-50} cy={-16} r={38} fill="#fff" stroke={INK} strokeWidth={6} /><circle cx={50} cy={-16} r={38} fill="#fff" stroke={INK} strokeWidth={6} />
				<circle cx={-50} cy={-12} r={10} fill={INK} /><circle cx={50} cy={-12} r={10} fill={INK} />
				<ellipse cy={62} rx={24} ry={32} fill="#7a1f2a" stroke={INK} strokeWidth={6} />
				<path d="M-100 28L-170 16M-100 48L-170 56M100 28L170 16M100 48L170 56" stroke={INK} strokeWidth={6} strokeLinecap="round" />
				<text textAnchor="middle" y={-145} fontSize={70} fontWeight={700} fill={CORAL} stroke="#fff" strokeWidth={10} paintOrder="stroke">{text}</text>
			</g>
		</svg>
	);
};
export const Bubble = ({t}: {t: string}) => {
	const p = useSpring();
	return <div style={{position: 'absolute', left: 500, top: 1430, maxWidth: 420, padding: '26px 40px', borderRadius: 50, background: '#fff', border: '6px solid #16202a', fontSize: 54, whiteSpace: 'nowrap', fontWeight: 700, color: '#e0246a', transform: `scale(${p}) rotate(-3deg)`}}>{t}</div>;
};
export const Reveal: React.FC<{stamp: string; children: React.ReactNode}> = ({stamp, children}) => {
	const f = useCurrentFrame();
	const scale = 3.2 - 2.2 * Math.min(1, f / 7);
	const shake = f < 22 ? Math.sin(f * 2.4) * (22 - f) * 0.9 : 0;
	return (
		<>
			<div style={{position: 'absolute', inset: 0, transform: `translate(${shake}px,${-shake / 2}px)`}}>
				<Sequence from={20} layout="none">{children}</Sequence>
			</div>
			{f < 24 && <div style={{position: 'absolute', left: 0, right: 0, top: 380, display: 'flex', justifyContent: 'center', opacity: f > 19 ? (24 - f) / 5 : 1}}><div style={{padding: '18px 48px', border: '14px solid #e0263a', borderRadius: 30, background: 'rgba(255,255,255,.95)', fontSize: 130, fontWeight: 700, color: '#e0263a', transform: `scale(${scale}) rotate(-8deg)`}}>{stamp}</div></div>}
		</>
	);
};

export const PapayaScene = () => (
	<Stage top="#bdeaf8" bottom="#fff6dd" floor="#fff0c2">
		<Pop x={540} y={560}><g transform="rotate(-18)"><ellipse rx={150} ry={240} fill="#ff9446" stroke="#c96a23" strokeWidth={8} /><ellipse rx={70} ry={150} fill="#7a2b16" />{Array.from({length: 24}, (_, i) => <circle key={i} cx={Math.sin(i * 2.4) * (12 + (i % 5) * 9)} cy={-126 + i * 10.6} r={9} fill="#16120e" />)}</g></Pop>
		<Pop x={830} y={300} delay={6}><text textAnchor="middle" fontSize={190} fontWeight={700} fill={CORAL}>?</text></Pop>
	</Stage>
);
export const CakeForkScene = () => {
	const f = useCurrentFrame();
	return (
		<Stage top="#ff9e7a" bottom="#ffe08a" floor="#ffe9b0">
			<Pop x={540} y={640}><g transform="scale(1.6)"><rect x={-170} y={-40} width={340} height={150} rx={22} fill="#ffc9d6" /><rect x={-170} y={-40} width={340} height={46} rx={20} fill="#fff" /><rect x={-10} y={-120} width={20} height={80} fill={CORAL} /><path d="M0-160Q22-125 0-115-22-125 0-160Z" fill={SUN} /></g></Pop>
			<g transform={`translate(${880 - Math.min(f, 18) * 7} ${330 + Math.min(f, 18) * 9}) rotate(35)`}><rect x={-13} y={-20} width={26} height={250} rx={13} fill="#d7dde2" stroke={INK} strokeWidth={5} /><path d="M-40-110H40V-20H-40Z" fill="#d7dde2" stroke={INK} strokeWidth={5} /></g>
		</Stage>
	);
};
export const ToothScene = () => {
	const f = useCurrentFrame();
	return (
		<Stage top="#bdeaf8" bottom="#fff6dd" floor="#fff0c2">
			<Pop x={540} y={590}><g transform={`rotate(${Math.sin(f * 0.8) * 5}) scale(1.5)`}><path d="M-120-130Q-60-178 0-140Q60-178 120-130Q170-70 112 28Q86 170 46 150Q22 62 0 60Q-22 62-46 150Q-86 170-112 28Q-170-70-120-130Z" fill="#fff" stroke={INK} strokeWidth={9} /><circle cx={-42} cy={-44} r={13} fill={INK} /><circle cx={42} cy={-44} r={13} fill={INK} /><path d="M-30 0Q0-24 30 0" stroke={INK} strokeWidth={8} fill="none" strokeLinecap="round" /></g></Pop>
		</Stage>
	);
};
export const FoodScene = () => (
	<Stage top="#3f5fb0" bottom="#a07aa8">
		<Pop x={540} y={720}><g><ellipse cy={60} rx={330} ry={46} fill="#eef1f3" /><ellipse cy={22} rx={190} ry={70} fill="#ffcf6b" /><circle cx={-70} cy={-20} r={42} fill={CORAL} /><circle cx={60} cy={-30} r={50} fill="#3aa76d" /></g></Pop>
		<Pop x={830} y={420} delay={6}><text textAnchor="middle" fontSize={190} fontWeight={700} fill={SUN}>?</text></Pop>
	</Stage>
);
export const FireworkSticker = () => (
	<div style={{position: 'absolute', left: 70, right: 70, top: 640, height: 400, display: 'flex', justifyContent: 'center'}}>
		<div style={{width: 510, height: 400, borderRadius: 40, overflow: 'hidden', background: '#0a9bf0'}}><Gif src={staticFile('gifs/fireworks.gif')} width={510} height={400} fit="cover" /></div>
	</div>
);
